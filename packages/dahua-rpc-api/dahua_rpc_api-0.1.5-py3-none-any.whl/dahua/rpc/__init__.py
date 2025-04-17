from typing import Any

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dahua.client import DahuaRpc


class RPC:
    def __init__(self, client: "DahuaRpc", parent: str):
        self.client = client
        self.parent = parent

    def _send(self, function: str, **kwargs) -> dict[str, Any]:
        """Send a request to the camera."""
        return self.client.request_json(method=f"{self.parent}.{function}", **kwargs)

    # ========================================
    # Common Methods
    # ========================================

    def list_method(self) -> list[str]:
        """Lists all methods of RPC function"""
        return self._send(function="listMethod").get("params", {}).get("method")
