from dahua.client import DahuaRpc


dahua = DahuaRpc(host="192.168.1.12")

dahua.login(username="admin", password="mypassword")

print("Serial Number: " + dahua.magic_box.get_serial_number())

dahua.logout()
