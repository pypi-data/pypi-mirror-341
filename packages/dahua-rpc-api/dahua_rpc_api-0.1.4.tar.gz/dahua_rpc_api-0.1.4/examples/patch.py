import os
import json
import argparse
import re
from typing import TypedDict
import requests
import zipfile
from time import sleep

from dahua.client import DahuaRpc
from dahua.utils.upgrade import Upgrade
from dahua.utils.cve import bypass_cve2021_33044
from dahua.exceptions import DahuaInvalidCredentials


def get_downloadable_firmware(model: str) -> str | None:
    """Get the downloadable firmware URL for the given model.

    Tested models:
      - IPC-HDBW2431R-ZS
      - IPC-HFW2431T-ZS
    """

    firmwares = {
        r"^IPC-H.*2.*3.*": "https://materialfile.dahuasecurity.com/uploads/cpq/SWR/2054889/M/DH_IPC-HX2X3X-Rhea_MultiLang_PN_Stream2_V2.800.0000029.0.R.221220.zip"
    }

    for pattern, url in firmwares.items():
        if re.match(pattern, model):
            return url


def update_firmware(
    dahua: DahuaRpc, device_model: str, firmware_file: str | None = None, **kwargs
) -> bool:
    if not firmware_file:
        if firmware_url := get_downloadable_firmware(device_model):
            print(f"Downloading firmware from URL: {firmware_url}")
            firmware_file = extract_patch(firmware_url)
        else:
            print(f"No downloadable firmware found for model: {device_model}")
            raise Exception("No downloadable firmware found")

    firmware_success = Upgrade(dahua).upgrade(firmware_file, **kwargs)
    return firmware_success


def extract_patch(patch_url: str, download_path: str = "/tmp") -> str:
    file_name = os.path.basename(patch_url)
    save_path = os.path.join(download_path, file_name)
    unzip_dir = os.path.join(download_path, file_name.replace(".zip", ""))

    response = requests.get(patch_url)
    if response.status_code != 200:
        print(f"Failed to download patch from {patch_url}")
        raise Exception("Failed to download patch")

    print("Patch downloaded successfully.")
    with open(save_path, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(save_path, "r") as zip_ref:
        zip_ref.extractall(unzip_dir)
    print("Patch extracted successfully.")

    files = os.listdir(unzip_dir)
    bin_files = [f for f in files if f.endswith(".bin")]
    largest_file = max(
        bin_files, key=lambda f: os.path.getsize(os.path.join(unzip_dir, f))
    )

    return os.path.join(unzip_dir, largest_file)


def is_bypass_fixed(host: str, port: int) -> bool:
    temp_client = DahuaRpc(host, port)
    try:
        bypass_cve2021_33044(temp_client)
        temp_client.logout()
    except DahuaInvalidCredentials:
        return True

    return False


class PatchReport(TypedDict):
    host: str
    port: int
    model: str | None
    firmware_before: str | None
    firmware_after: str | None
    is_firmware_updated: bool
    is_bypass_fixed: bool
    errors: list[str]


def main(args) -> None:
    print(f"Processing camera: {args.host}:{args.port}")
    errors: list[str] = []
    model: str | None = None
    firmware_before: str | None = None
    firmware_after: str | None = None
    is_firmware_updated: bool = False
    bypass_fixed: bool = False

    report: PatchReport = {
        "host": args.host,
        "port": args.port,
        "model": model,
        "firmware_before": firmware_before,
        "firmware_after": firmware_after,
        "is_firmware_updated": is_firmware_updated,
        "is_bypass_fixed": bypass_fixed,
        "errors": errors,
    }

    try:
        dahua = DahuaRpc(args.host, args.port)
        dahua.login(args.username, args.password)

        report["model"] = dahua.magic_box.get_device_type()
        print(f"Device model: {report['model']}")

        report["firmware_before"] = dahua.magic_box.get_software_version().get(
            "Version"
        )
        print(f"Current Firmware: {report['firmware_before']}")

        print(f"Updating firmware for model: {report['model']}")
        report["is_firmware_updated"] = update_firmware(
            dahua,
            report["model"],
            args.firmware_file,
            backup_settings=args.backup_camera_config,
            backup_path=args.backup_camera_config_path,
        )
        if not report["is_firmware_updated"]:
            print("Firmware update failed.")
            raise Exception("Firmware update failed")

        print(
            f"Firmware updated successfully for {args.host}, waiting for {args.reconnect_wait} seconds to stabilize..."
        )
        sleep(args.reconnect_wait)

        print("Checking if bypass is fixed...")
        report["is_bypass_fixed"] = is_bypass_fixed(args.host, args.port)
        print(f"Bypass fixed: {report["is_bypass_fixed"]}")

        # Must login again
        dahua = DahuaRpc(args.host, args.port)
        dahua.login(args.username, args.password)

        print("Checking firmware version after update...")
        report["firmware_after"] = dahua.magic_box.get_software_version().get("Version")
        print(f"Firmware after update: {report['firmware_after']}")

        dahua.logout()
        print(f"Finished processing camera: {args.host}:{args.port}")

    except Exception as e:
        print(f"Error occurred: {e}")
        errors.append(str(e))
    finally:
        output_file = (
            args.output_file or f"/tmp/patch_report_{args.host}_{args.port}.json"
        )
        with open(output_file, "w") as output_file:
            json.dump(report, output_file, indent=4)


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Dahua Firmware Upgrade")
    argparse.add_argument(
        "-u", "--username", type=str, required=True, help="Username for authentication"
    )
    argparse.add_argument(
        "-p", "--password", type=str, required=True, help="Password for authentication"
    )
    argparse.add_argument(
        "--host", type=str, required=True, help="Host address of the device"
    )
    argparse.add_argument(
        "--port", type=int, default=80, help="Port number of the device"
    )
    argparse.add_argument(
        "--backup-camera-config",
        type=bool,
        default=True,
        help="Backup settings before upgrade",
    )
    argparse.add_argument(
        "--backup-camera-config-path",
        type=str,
        help="Path to save the backup file",
    )
    argparse.add_argument(
        "-f",
        "--firmware-file",
        type=str,
        help="Path to the firmware file (only if not using automatic patch)",
    )
    argparse.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Path to save the patch report",
    )
    argparse.add_argument(
        "--reconnect-wait",
        type=int,
        default=180,
        metavar="SECONDS",
        help="How long to wait before reconnecting to the camera after upgrade",
    )

    args = argparse.parse_args()

    main(args)
