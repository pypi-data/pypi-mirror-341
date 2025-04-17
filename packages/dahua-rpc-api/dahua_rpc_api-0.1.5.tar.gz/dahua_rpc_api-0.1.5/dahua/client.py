from typing import Any
from dataclasses import dataclass, field

import requests

from dahua.util import generate_password_hash
from dahua.utils.logger import logger
from dahua.exceptions import DahuaRequestError, code_to_exception
from dahua.rpc._global import GlobalRPC
from dahua.rpc.magic_box import MagicBoxRPC
from dahua.rpc.user_manager import UserManagerRPC
from dahua.rpc.upgrader import UpgraderRPC
from dahua.rpc.console import ConsoleRPC
from dahua.cgi_bin import CGIBin


@dataclass
class DahuaRpc:
    host: str
    port: int = 80

    # Methods
    _global: GlobalRPC = field(init=False)
    magic_box: MagicBoxRPC = field(init=False)
    user_manager: UserManagerRPC = field(init=False)
    upgrader: UpgraderRPC = field(init=False)
    console: ConsoleRPC = field(init=False)

    cgi_bin: CGIBin = field(init=False)

    def __post_init__(self) -> None:
        self.session: requests.Session = requests.Session()
        self.session_id: str | None = None
        self.request_id: int = 0
        self.base_url: str = f"http://{self.host}:{self.port}"

        # Initialize RPC classes
        self._global = GlobalRPC(client=self)
        self.magic_box = MagicBoxRPC(client=self)
        self.user_manager = UserManagerRPC(client=self)
        self.upgrader = UpgraderRPC(client=self)
        self.console = ConsoleRPC(client=self)

        self.cgi_bin = CGIBin(client=self)

    def request(
        self,
        endpoint: str = "RPC2",
        **kwargs: Any,
    ) -> requests.Response:
        """Send an RPC request."""
        self.request_id += 1
        return self.session.post(f"{self.base_url}/{endpoint}", **kwargs)

    def request_json(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        verify: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        json_params: dict[str, Any] = {"method": method, "id": self.request_id}
        if params is not None:
            json_params["params"] = params
        if self.session_id:
            json_params["session"] = self.session_id

        response = self.request(json=json_params, **kwargs)
        json_response = response.json()

        if verify:
            if error := json_response.get("error"):
                raise code_to_exception(error.get("code"))(error.get("message"))
            if not json_response.get("result"):
                raise DahuaRequestError(f"Request failed: {json_response}")

        return json_response

    def login(self, username: str, password: str) -> None:
        """Login to the camera using the provided username and password."""
        if self.is_logged_in():
            logger.warning("Already logged in. Skipping login.")
            return

        initial_request = self._global.login(
            params={"userName": username, "password": password, "clientType": "Web3.0"},
            verify=False,  # Can't verify first request, as it doesn't have a session yet.
        )

        self.session_id = initial_request.get("session")
        realm = initial_request.get("params", {}).get("realm", "")
        random_value = initial_request.get("params", {}).get("random", "")
        pass_hash = generate_password_hash(username, password, realm, random_value)

        self._global.login(
            params={
                "userName": username,
                "password": pass_hash,
                "clientType": "Web3.0",
                "authorityType": "Default",
                "passwordType": "Default",
            }
        )

    def logout(self):
        """Logout from the camera."""
        self._global.logout()
        self.session.close()
        self.session_id = None
        self.request_id = 0

    def is_logged_in(self) -> bool:
        """Check if the user is logged in."""
        return self.session_id is not None
