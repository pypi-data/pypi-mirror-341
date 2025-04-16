from dahua.rpc import RPC
from typing import TypedDict


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dahua.client import DahuaRpc


class GetStateResponse(TypedDict):
    File: str
    Progress: int
    State: str
    NoReboot: list[str] | None


class UpgraderRPC(RPC):
    def __init__(self, client: "DahuaRpc") -> None:
        super().__init__(client=client, parent="upgrader")

    def get_state(self) -> GetStateResponse:
        """Get the state of the Upgrader."""
        return self._send(function="getState").get("params", {})
