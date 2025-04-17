from typing import Any
from dahua.rpc import RPC


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dahua.client import DahuaRpc


class UserManagerRPC(RPC):
    def __init__(self, client: "DahuaRpc"):
        super().__init__(client=client, parent="userManager")

    def get_user_info_all(self) -> dict[str, Any]:
        """
        TODO: add type annotations to return value
        {
            "Anonymous": false,
            "AuthorityList": [
                "AuthUserMag",
                "Monitor_01",
            ],
            "Group": "admin",
            "Id": 1,
            "Memo": "admin 's account",
            "Name": "admin",
            "Password": "******",
            "PasswordModifiedTime": "2000-01-01 00:00:48",
            "PwdScore": 0,
            "Reserved": true,
            "Sharable": true
        }
        """
        return self._send(function="getUserInfoAll").get("params", {}).get("users", {})

    def get_active_user_info_all(self) -> dict[str, Any]:
        return (
            self._send(function="getActiveUserInfoAll")
            .get("params", {})
            .get("users", {})
        )

    def delete_user(self, name: str) -> None:
        self._send(function="deleteUser", params={"name": name})
