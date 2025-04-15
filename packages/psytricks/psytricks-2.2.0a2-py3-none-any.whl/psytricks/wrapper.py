"""PowerShell Python Citrix Tricks."""

import subprocess
import json
import os
import time

from os.path import dirname
from pathlib import Path
from sys import platform

import requests
from loguru import logger as log

from . import __version__
from .decoder import parse_powershell_json
from .literals import Action, RequestName, MsgStyle


class ResTricksWrapper:
    """Wrapper performing REST requests and processing the responses.

    Parameters
    ----------
    base_url : str, optional
        The base URL where to find the ResTricks service. Will default to
        `http://localhost:8080/` if nothing is specified.
    verify : bool, optional
        Validate the server version as soon as a connection is established. Set
        to `False` to disable the version check and ignore potential problems
        during the connection check.
    lazy : bool, optional
        By default the constructor will try to establish a connection to the
        ResTricks service. If this is set to `True`, the connection will only be
        established once a request has to be sent to the server but not during
        instantiation.

    Attributes
    ----------
    base_url : str
        See the constructor for details.
    timeout : int
        The timeout in seconds to use for `requests.get` and `requests.post`
        calls, defaulting to 5.
    server_version : list
        The server version as a list of version components, where the first
        three components are of type `int` (representing `major.minor.patch`),
        whereas the last component may be a `str` as well.
    headers : dict
        A dict of headers to be sent along the requests.
    """

    def __init__(self, base_url: str = "", verify: bool = True, lazy: bool = False):
        self.base_url = "http://localhost:8080/" if not base_url else base_url
        self.timeout = 5
        self.server_version = [0, 0, 0, 0]

        # FIXME: currently "localhost" is hardcoded here as this is what the
        # service expects (see `Listener.Prefixes` in `restricks-server.ps1` for
        # the details) - this should be made configurable!
        self.headers = {"Host": "localhost"}

        self._connected = False
        self._verify = verify
        self._read_only = False

        if not lazy:
            self.connect()

        log.debug(f"Initialized {self.__class__.__name__}({base_url}) ✨")

    @property
    def read_only(self) -> bool:
        """Mode of operation (default is `False`, meaning read / write).

        In case `read_only` is set to `True`, any request that would potentially
        result in a changed state of the Citrix environment (currently this is
        exclusively done by `POST` requests) will not be executed. Instead, a
        log message (level `WARNING`) will be issued, documenting the
        intercepted request.

        This is particularly useful when testing changes to software using this
        library without having a Citrix test environment available, or for
        making sure a tool is running in *monitoring-only* mode.
        """
        return self._read_only

    @read_only.setter
    def read_only(self, value: bool) -> None:
        verb = "Enabling" if value else "Disabling"
        log.debug(f"{verb}'read-only' mode.")
        self._read_only = value

    def connect(self):
        """Connect to the ResTricks service unless already connected.

        Raises
        ------
        ValueError
            Raised in case the server version doesn't match the local version.
        ConnectionError
            Raised in case the initial connection check failed.
        """
        if self._connected:
            log.trace("Connection 🔌 established previously, not reconnecting.")
            return

        log.debug(f"Trying to connect 🔌 to the ResTricks server: {self.base_url}")

        try:
            status = self.send_get_request("version", auto_conn=False)["Status"]
            log.trace(f"Server status: [{status}]")
            server_version = status["PSyTricksVersion"]

            log.debug("Successfully connected 🔌 to ResTricks server 🆗")
            if self._verify:
                version_matching = self.validate_version(server_version)
                if not version_matching:
                    raise ValueError(f"Unexpected server version: {server_version}")
            else:
                log.warning(f"Skipping version check (server: {server_version})")
            self._connected = True

        except Exception as ex:  # pylint: disable-msg=broad-except
            if self._verify:
                raise ConnectionError(
                    f"Connecting to {self.base_url} failed: {ex}"
                ) from ex

    def validate_version(self, server_ver):
        """Validate the server version against the local module.

        Parse the version strings of the local module and the server response
        and compare them for equality (ignoring the 4th component, which may
        denote a pre- or development-release).

        If the 3rd component (PATCH level) is differing a message will be issued
        to the debug log but the method will still return True.

        Parameters
        ----------
        server_ver : dict
            The dict parsed from the JSON response when sending a `version` GET
            request to the server.

        Returns
        -------
        bool
            True in case the versions are matching (at least MAJOR and MINOR
            levels), False otherwise.
        """

        def parse_ver(ver):
            log.trace(f"Parsing version string: [{ver}]")
            # pre / alpha versions are separated by a dash "-" char according to
            # semantic versioning rules (use "0" if no dash is present):
            pre = 0
            if "-" in ver:
                ver, pre = ver.split("-")

            version = [int(x) for x in ver.split(".")]
            version.append(pre)
            log.trace(f"Parsed version: {version}")
            return version

        try:
            self.server_version = parse_ver(server_ver)
            log.debug(f"Server version: {self.server_version} 🪪")
        except Exception as ex:  # pylint: disable-msg=broad-except
            log.warning(f"Unable to parse server version [{server_ver}]: {ex}")
            return False

        client_version = parse_ver(__version__)
        log.debug(f"Client version: {client_version} 🪪")

        # compare versions, ignoring the 4th component (dev/pre/alpha/...)
        if client_version[:3] == self.server_version[:3]:
            log.debug("Versions are matching! 🏅")
            return True

        # be lenient on patch-level mismatches (but issue an debug message)
        if client_version[:2] == self.server_version[:2]:
            log.debug("Versions are differing in PATCH level! 🔍")
            return True

        log.error("Version mismatch! 🧨")
        return False

    @staticmethod
    def _check_response(response):
        """Check the HTTP response code and JSON status attributes."""
        if response.status_code == 200:
            return

        log.warning(f"Response code {response.status_code} indicates a problem!")

        payload = response.json()
        try:
            status = payload["Status"]
            log.warning(
                "Status details:\n"
                f"['Timestamp']: {status['Timestamp']}\n"
                f"['PSyTricksVersion']: {status['PSyTricksVersion']}\n"
                f"['ExecutionStatus']: {status['ExecutionStatus']}\n"
                f"['ErrorMessage']: {status['ErrorMessage']}\n"
            )
        except Exception as ex:  # pylint: disable-msg=broad-except
            log.error(f"Error fetching response payload status: {ex}")
            log.warning(response.text)
            raise ValueError(f"Malformed response: {response.text}") from ex

    def send_get_request(self, raw_url: str, auto_conn: bool = True):
        """Perform a `GET` request and process the response.

        Parameters
        ----------
        raw_url : str
            The part of the URL that will be appended to `self.base_url`.
        auto_conn: bool, optional
            If set to `True` (default), `self.connect()` will be called before
            sending the request. Can be disabled to avoid a recursive loop as
            this method itself is also called by `connect()`.

        Returns
        -------
        list or dict or None
            The parsed `JSON` of the response, often a dict or a list of dict.
            Will be an empty list in case something went wrong performing the
            GET request or processing the response.
        """
        if auto_conn:
            self.connect()

        try:
            response = requests.get(
                self.base_url + raw_url, timeout=self.timeout, headers=self.headers
            )
        except Exception as ex:  # pylint: disable-msg=broad-except
            log.error(f"GET request [{raw_url}] failed: {ex}")
            raise ex

        try:
            data = response.json(object_hook=parse_powershell_json)
        except json.JSONDecodeError as ex:
            msg = (
                f"Decoding JSON failed at pos {ex.pos}\n"
                f"Response text (lim. to 500 chars):\n--\n{response.text[:500]}\n--\n"
            )
            log.error(msg)
            raise json.JSONDecodeError(msg, doc=ex.doc, pos=ex.pos) from ex
        except Exception as ex:  # pylint: disable-msg=broad-except
            msg = (
                f"Exception processing response from GET request [{raw_url}]: {ex}\n"
                f"Response text (lim. to 500 chars):\n--\n{response.text[:500]}\n--\n"
            )
            log.error(f"{msg}\n== STATUS CODE:{response.status_code}")
            raise json.JSONDecodeError(msg, doc=response.text, pos=0)

        ResTricksWrapper._check_response(response)

        return data

    def send_post_request(self, raw_url: str, payload: dict, no_json: bool = False):
        """Perform a `POST` request and process the response.

        The response will be checked for a valid HTTP status code and will be
        parsed into a `JSON` object.

        Respects the `read_only` instance attribute, see note below for details.

        Parameters
        ----------
        raw_url : str
            The part of the URL that will be appended to `self.base_url`.
        payload : dict
            The parameters to pass as `JSON` payload to the POST request.
        no_json : bool
            If set to `True` the response is expected to contain no `JSON` and
            an empty list will be returned.

        Returns
        -------
        list or dict or None
            The parsed `JSON` of the response, often a dict or a list of dict.
            Will be an empty list in case something went wrong performing the
            POST request or processing the response (or in case the `no_json`
            parameter was set to `True`).

        Note
        ----
        In case the object's instance attribute `read_only` is set to `True`,
        this method will **NOT perform an actual `POST` request** (as this would
        potentially lead to a state-change in the Citrix platform) but rather
        issue a `WARNING` level log message and return an empty list.
        """
        self.connect()

        if self.read_only:
            log.warning(
                f"{self.__class__.__name__} is running in READ-ONLY mode, the "
                f"following request has **NOT** been performed:\n"
                f"> raw_url: [{raw_url}]\n"
                f"> payload:\n------\n{payload}\n------\n"
            )
            return []

        try:
            response = requests.post(
                self.base_url + raw_url,
                json=payload,
                timeout=self.timeout,
                headers=self.headers,
            )
        except Exception as ex:  # pylint: disable-msg=broad-except
            log.error(f"POST request [{raw_url}] failed: {ex}")
            raise ex

        ResTricksWrapper._check_response(response)

        if no_json:
            log.debug(f"No-payload response status code: {response.status_code}")
            return []

        return response.json(object_hook=parse_powershell_json)

    def get_machine_status(self) -> list:
        """Send a `GET` request with `GetMachineStatus`.

        Returns
        -------
        list(dict)
            The `Data` dicts parsed from the JSON returned by the REST service.
        """
        log.debug("Requesting current status of machines...")
        return self.send_get_request("GetMachineStatus")["Data"]

    def get_sessions(self) -> list:
        """Send a `GET` request with `GetSessions`.

        Returns
        -------
        list(dict)
            The `Data` dicts parsed from the JSON returned by the REST service,
            containing details about the currently existing sessions.
        """
        log.debug("Requesting current sessions...")
        return self.send_get_request("GetSessions")["Data"]

    def get_access_users(self, group: str) -> list:
        """Send a `GET` request with `GetAccessUsers`.

        Parameters
        ----------
        group : str
            The name of the Delivery Group to request users having access.

        Returns
        -------
        list(dict)
            The `Data` dicts parsed from the JSON returned by the REST service,
            containing the user objects having access to the given group.
        """
        log.debug(f"Requesting users having access to group [{group}]...")
        return self.send_get_request(f"GetAccessUsers/{group}")["Data"]

    def disconnect_session(self, machine: str) -> dict:
        """Send a `POST` request with `DisconnectSession`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to disconnect the session on.

        Returns
        -------
        dict
            The `Data` dict parsed from the JSON returned by the REST service,
            containing details on the affected session. In case the JSON
            contains an empty `Data` object, an empty dict will be returned.
            Please note that sending a disconnect request for a session that is
            already disconnected will not change the session state but still
            return the session details.
        """
        log.debug(f"Requesting session on [{machine}] to be disconnected...")
        payload = {"DNSName": machine}
        session = self.send_post_request("DisconnectSession", payload)["Data"]
        if session is None:
            log.debug(f"No data received, probably [{machine}] has no session.")
            return {}

        return session

    def set_access_users(self, group: str, users: str, disable: bool) -> list:
        """Send a `POST` request with `SetAccessUsers`.

        Parameters
        ----------
        group : str
            The name of the Delivery Group to request users having access.
        users : str
            A string with one or more (comma-separated) usernames (prefixed with
            the domain name) whose access permissions to the given group should
            be adapted.
        disable : bool
            A flag requesting the permissions for the given username(s) to be
            removed (if True) instead of being added (if False).

        Returns
        -------
        list(dict)
            The `Data` dicts parsed from the JSON returned by the REST service,
            containing the user objects having access to the given group *after*
            the operation has been performed.
        """
        verb = "Removing" if disable else "Adding"
        log.debug(f"{verb} access to group [{group}] for user(s) [{users}]...")
        payload = {
            "Group": group,
            "UserNames": users,
            "RemoveAccess": disable,
        }
        return self.send_post_request("SetAccessUsers", payload)["Data"]

    def set_maintenance(self, machine: str, disable: bool) -> dict:
        """Send a `POST` request with `SetMaintenanceMode`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to modify maintenance mode on.
        disable : bool
            A flag requesting maintenance mode for the given machine(s) to be
            turned off (if True) instead of being turned on (if False).

        Returns
        -------
        dict
            The `Data` dict parsed from the JSON returned by the REST service.
        """
        verb = "Disabling" if disable else "Enabling"
        log.debug(f"{verb} maintenance mode on [{machine}]...")
        payload = {
            "DNSName": machine,
            "Disable": disable,
        }
        return self.send_post_request("SetMaintenanceMode", payload)["Data"]

    def send_message(self, machine: str, message: str, title: str, style: MsgStyle):
        """Send a `POST` request with `SendSessionMessage`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to send the message to.
        message : str
            The message body.
        title : str
            The message title.
        style : str
            The message style defining the icon shown in the pop-up message as
            defined in `psytricks.literals.MsgStyle`.
        """
        log.debug(f'Sending a pop-up message ("{title}") to [{machine}]...')
        payload = {
            "DNSName": machine,
            "Text": message,
            "Title": title,
            "MessageStyle": style,
        }
        self.send_post_request("SendSessionMessage", payload, no_json=True)

    def perform_poweraction(self, machine: str, action: Action) -> dict:
        """Send a `POST` request with `MachinePowerAction`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to disconnect the session on.
        action : str
            The power action to perform, one of `psytricks.literals.Action`.

        Returns
        -------
        dict
            The `Data` dict parsed from the JSON returned by the REST service
            containing details on the power action status of the machine.
        """
        log.debug(f"Requesting action [{action}] for machine [{machine}]...")
        payload = {
            "DNSName": machine,
            "Action": action,
        }
        return self.send_post_request("MachinePowerAction", payload)["Data"]


class PSyTricksWrapper:
    """Wrapper handling PowerShell calls and processing of returned data.

    Parameters
    ----------
    deliverycontroller : str
        The address (IP or FQDN) of the Citrix Delivery Controller to
        connect to.

    Attributes
    ----------
    pswrapper : pathlib.Path
        The path to the PowerShell wrapper script (class variable!).
    ps_exe : pathlib.Path
        Path to the PowerShell executable itself (i.e. the *interpreter*).
    add_flags : list(str)
        A list of additional flags to add to the call of the wrapper script.
    deliverycontroller : str
        The address of the Delivery Controller.

    Raises
    ------
    RuntimeError
        Raised in case the PowerShell call was producing output on `stderr`
        (indicating something went wrong) or returned with a non-zero exit code.
    ValueError
        Raised in case decoding the string produced by the PowerShell call on
        `stdout` could not be decoded using "cp850" (indicating it contains
        characters not supported by "code page 850" like e.g. the Euro currency
        symbol "€") or in case parsing it via `json.loads()` failed.
    """

    pswrapper = Path(dirname(__file__)) / "__ps1__" / "psytricks-wrapper.ps1"

    def __init__(self, deliverycontroller: str):
        # FIXME: this platform-specific conditional below is a hack while
        # implementing the package, remove for production!
        self.add_flags = []
        if platform.startswith("linux"):
            self.ps_exe = Path("/snap/bin/pwsh")
            self.add_flags = ["-Dummy", "-NoSnapIn"]
        else:
            self.ps_exe = (
                Path(os.environ["SYSTEMROOT"])
                / "System32"
                / "WindowsPowerShell"
                / "v1.0"
                / "powershell.exe"
            )

        self.deliverycontroller = deliverycontroller
        log.debug(f"Using PowerShell script [{self.pswrapper}].")
        log.debug(f"Using Delivery Controller [{self.deliverycontroller}].")

    def run_ps1_script(self, request: RequestName, extra_params: list = None) -> list:
        """Call the PowerShell wrapper to retrieve information from Citrix.

        Parameters
        ----------
        request : str
            The request name, one of `psytricks.literals.RequestName`.
        extra_params : list(str)
            A list of strings that should be added as extra parameters to the
            PowerShell command that is run as a subprocess.

        Returns
        -------
        list(str)
            The "Data" section of the JSON parsed from the output returned by
            the PS1 wrapper script.

        Raises
        ------
        RuntimeError
            Raised in case the PS1 wrapper script pushed anything to STDERR or
            the Python `subprocess` call returned a non-zero exit code or a
            non-zero return code was passed on in the parsed JSON (indicating
            something went wrong on the lowest level when interacting with the
            Citrix toolstack).
        ValueError
            Raised in case parsing the JSON returned by the PS1 wrapper failed
            or it doesn't conform to the expected format (e.g. missing the
            `Data` or `Status` items).
        """
        if extra_params is None:
            extra_params = []

        try:
            tstart = time.time()
            command = [
                self.ps_exe,
                "-NonInteractive",
                "-NoProfile",
                "-File",
                self.pswrapper,
                "-AdminAddress",
                self.deliverycontroller,
                "-CommandName",
                request,
            ]
            command = command + self.add_flags + extra_params
            log.debug(f"Command for subprocess call: {command}")
            completed = subprocess.run(
                command,
                capture_output=True,
                check=True,
            )
            elapsed = time.time() - tstart
            log.debug(f"[PROFILING] PowerShell call: {elapsed:.3}s.")
            if completed.stderr:
                raise RuntimeError(
                    "Wrapper returned data on STDERR, this is not expected:"
                    f"\n============\n{completed.stderr}\n============\n"
                )
        except subprocess.CalledProcessError as ex:
            raise RuntimeError(
                f"Call returned a non-zero state: {ex.returncode} {ex.stderr}"
            ) from ex

        try:
            tstart = time.time()
            stdout = completed.stdout.decode(encoding="cp850")
            elapsed = time.time() - tstart
            log.debug(f"[PROFILING] Decoding stdout: {elapsed:.5}s.")

            tstart = time.time()
            parsed = json.loads(stdout, object_hook=parse_powershell_json)
            elapsed = time.time() - tstart
            log.debug(f"[PROFILING] Parsing JSON: {elapsed:.5}s.")
        except Exception as ex:
            raise ValueError(f"Error decoding / parsing output:\n{stdout}") from ex

        if "Status" not in parsed or "Data" not in parsed:
            raise ValueError(f"Received malformed JSON from PS1 script: {parsed}")

        data = parsed["Data"]
        status = parsed["Status"]

        exec_status = int(status["ExecutionStatus"])
        if exec_status > 0:
            msg = (
                f"JSON returned by the PS1 wrapper contains execution status "
                f"{exec_status} for command [{request}]:\n--------\n"
                f"{status['ErrorMessage']}\n--------\n"
                "This indicates something went wrong talking to the Citrix toolstack."
            )
            log.error(msg)
            raise RuntimeError(msg)

        log.debug(f"Parsed 'Data' section contains {len(data)} items.")
        return data

    def get_machine_status(self) -> list:
        """Call the wrapper with command `GetMachineStatus`.

        Returns
        -------
        list(str)
            The parsed JSON.
        """
        return self.run_ps1_script(request="GetMachineStatus")

    def get_sessions(self) -> list:
        """Call the wrapper with command `GetSessions`.

        Returns
        -------
        list(str)
            The parsed JSON.
        """
        return self.run_ps1_script(request="GetSessions")

    def disconnect_session(self, machine: str) -> list:
        """Call the wrapper with command `DisconnectSession`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to disconnect the session on.

        Returns
        -------
        list(str)
            The parsed JSON as returned by the wrapper script.
        """
        return self.run_ps1_script(
            request="DisconnectSession",
            extra_params=["-DNSName", machine],
        )

    def get_access_users(self, group: str) -> list:
        """Call the wrapper with command `GetAccessUsers`.

        Parameters
        ----------
        group : str
            The name of the Delivery Group to request users having access.

        Returns
        -------
        list(str)
            The parsed JSON as returned by the wrapper script.
        """
        return self.run_ps1_script(
            request="GetAccessUsers",
            extra_params=["-Group", group],
        )

    def set_access_users(self, group: str, users: str, disable: bool) -> list:
        """Call the wrapper with command `SetAccessUsers`.

        Parameters
        ----------
        group : str
            The name of the Delivery Group to request users having access.
        users : str
            A string with one or more (comma-separated) usernames whose access
            permissions to the given group should be adapted.
        disable : bool
            A flag requesting the permissions for the given username(s) to be
            removed (if True) instead of being added (if False).

        Returns
        -------
        list(str)
            The parsed JSON as returned by the wrapper script.
        """
        extra_params = [
            "-Group",
            group,
            "-UserNames",
            users,
        ]
        if disable:
            extra_params.append("-Disable")

        return self.run_ps1_script(request="SetAccessUsers", extra_params=extra_params)

    def set_maintenance(self, machine: str, disable: bool) -> list:
        """Call the wrapper with command `SetMaintenanceMode`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to modify maintenance mode on.
        disable : bool
            A flag requesting maintenance mode for the given machine(s) to be
            turned off (if True) instead of being turned on (if False).

        Returns
        -------
        list(str)
            The parsed JSON as returned by the wrapper script.
        """
        extra_params = ["-DNSName", machine]
        if disable:
            extra_params.append("-Disable")

        return self.run_ps1_script(
            request="SetMaintenanceMode", extra_params=extra_params
        )

    def send_message(self, machine: str, message: str, title: str, style: MsgStyle):
        """Call the wrapper with command `SendSessionMessage`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to disconnect the session on.
        message : str
            The message body.
        title : str
            The message title.
        style : str
            The message style defining the icon shown in the pop-up message as
            defined in `psytricks.literals.MsgStyle`.
        """
        extra_params = [
            "-DNSName",
            machine,
            "-Title",
            title,
            "-Text",
            message,
            "-MessageStyle",
            style,
        ]

        self.run_ps1_script(request="SendSessionMessage", extra_params=extra_params)

    def perform_poweraction(self, machine: str, action: Action) -> None:
        """Call the wrapper with command `MachinePowerAction`.

        Parameters
        ----------
        machine : str
            The FQDN of the machine to disconnect the session on.
        action : str
            The power action to perform, one of `psytricks.literals.Action`.
        """
        extra_params = ["-DNSName", machine, "-Action", action]
        return self.run_ps1_script(
            request="MachinePowerAction", extra_params=extra_params
        )
