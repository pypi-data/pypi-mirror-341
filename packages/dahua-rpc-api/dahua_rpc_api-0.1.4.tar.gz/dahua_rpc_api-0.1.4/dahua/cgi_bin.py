from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dahua.client import DahuaRpc


@dataclass
class CGIBin:
    client: "DahuaRpc"

    def config_file_export(self, action: str = "All") -> bytes:
        """Export the configuration file."""
        assert self.client.is_logged_in(), "Please login first."

        response = self.client.session.get(
            f"{self.client.base_url}/cgi-bin/configFileExport.backup",
            params={
                "action": action,
                "sessionId": self.client.session_id,
            },
        )
        return response.content
