from napalm import get_network_driver
from yaml import safe_load
from rich import print
from getpass import getpass

username = input("Please enter username: ")
password = getpass()

checks = [
    "8C:36:7A",
    "94:56:41",
    "08:03:42",
    "EC:68:81",
    "E4:A7:49",
    "D4:1D:71",
    "78:6D:94",
    "58:49:3B",
    "08:66:1F",
    "08:30:6B",
    "00:86:9C",
    "00:1B:17",
    "84:D4:12",
    "7C:89:C1",
    "34:E5:EC",
    "C4:24:56",
    "E8:98:6D",
    "D4:9C:F4",
    "24:0B:0A",
    "D4:F4:BE",
    "B4:0C:25",
]


def main():
    """
    Main execution of program
    """

    with open("hosts.yaml", "r") as handle:
        host_root = safe_load(handle)

    for host in host_root["my_list"]:
        driver = get_network_driver("ios")
        conn = driver(
            hostname=host["name"], username=username, password=password
        )
        print(f"Checking {host['name']}")
        conn.open()
        macs = conn.get_mac_address_table()
        for mac in macs:
            for check in checks:
                if check in mac["mac"]:
                    print(
                        f"Found Palo with mac {mac['mac']} on {host['name']} interface {mac['interface']}"
                    )

        conn.close()


if __name__ == "__main__":
    main()
