from dahua.rpc import RPC


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dahua.client import DahuaRpc


class ConsoleRPC(RPC):
    def __init__(self, client: "DahuaRpc") -> None:
        super().__init__(client=client, parent="console")

    def run_cmd(self, command: str) -> dict:
        return self._send(function="runCmd", params={"command": command})
