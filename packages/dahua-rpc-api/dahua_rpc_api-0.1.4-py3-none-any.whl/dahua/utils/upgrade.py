import os
from time import sleep
from dataclasses import dataclass

from dahua.client import DahuaRpc
from dahua.utils.logger import logger
from dahua.exceptions import DahuaRequestError


@dataclass
class Upgrade:
    client: "DahuaRpc"

    def upgrade(
        self,
        firmware_path: str,
        backup_settings=True,
        backup_path: str | None = None,
    ) -> bool:
        """Upgrade the firmware of the device."""
        logger.info("Starting firmware upgrade...")

        if not backup_path:
            backup_path = f"/tmp/dahua/{self.client.host}_{self.client.port}_configFileExport.backup"

        if backup_settings:
            # Backup settings before upgrade
            logger.info("Backing up settings...")
            if not self._backup_settings(backup_path):
                logger.error("Failed to backup settings.")
                return False

        # Upload the firmware
        logger.info("Uploading firmware")
        if not self._upload_firmware(firmware_path):
            logger.error("Failed to upload firmware.")
            return False

        # Check upgrade progress
        if not self._check_progress():
            logger.error("Upgrade failed")
            return False

        logger.info("Firmware upgrade completed successfully.")
        return True

    def _backup_settings(self, export_path: str) -> bool:
        """Backup settings before upgrade."""
        logger.info(f"Saving settings to {export_path}")
        file_bytes = self.client.cgi_bin.config_file_export(action="All")
        if file_bytes:
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            with open(export_path, "wb") as f:
                f.write(file_bytes)
            logger.info(f"Settings saved to {export_path}")
            return True

        logger.error("Failed to backup settings.")
        return False

    def _upload_firmware(self, firmware_path: str) -> bool:
        assert self.client.session_id, "Session ID is not set. Please login first."
        cookies = {"DWebClientSessionID": self.client.session_id}

        with open(firmware_path, "rb") as f:
            files = {"fileupload": f}
            response = self.client.request(
                endpoint="RPC2_Upgrade", files=files, cookies=cookies
            )
            logger.debug(f"Firmware upload response: {response.text}")
            return "sonia upgrade successfully" in response.text

    def _check_progress(self, max_checks=100) -> bool:
        state = "Upgrading"
        checks = 0

        while state == "Upgrading" and checks < max_checks:
            try:
                # Check upgrade progress
                logger.debug("Checking upgrade progress...")
                update = self.client.upgrader.get_state()
                state = update.get("State")

                logger.info(f"Upgrade progress: {update.get('Progress')}%")
                logger.debug(f"Upgrade state: {update}")
                sleep(5)
            except DahuaRequestError as e:
                logger.error(f"Error checking upgrade progress: {e}")

            checks += 1
            if checks >= max_checks:
                logger.error("Max checks reached. Upgrade may be stuck.")
                return False

        return state != "Invalid"
