#!/usr/bin/env python

"""
Script used for OSPF deployment using Netmiko
"""

# Import requirements
from yaml import safe_load
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
from rich import print
from rich.markup import escape
from network_utils import address, mask


def main():
    """
    Main execution
    """

    # Open hosts file as variable for future use
    with open("hosts.yaml", "r") as handle:
        host_root = safe_load(handle)
    print(host_root)

    # Set platform map to match netmiko
    platform_map = {"ios": "cisco_ios", "eos": "arista_eos", "aoscx": "hp_procurve"}

    # Assigning platform variable to each host
    for host in host_root["host_list"]:
        platform = platform_map[host["platform"]]

        # Load in the host specific vars
        with open(f"vars/{host['name']}.yaml", "r") as handle:
            ospf = safe_load(handle)

        # This portion is essentially configuring our jinja environment
        j2_env = Environment(
            loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )
        # https://www.kite.com/python/answers/how-to-call-a-function-in-a-jinja2-template-in-python
        j2_env.globals["address"] = address
        j2_env.globals["mask"] = mask

        template = j2_env.get_template(f"templates/netmiko/{platform}.j2")
        new_ospf_config = template.render(data=ospf)
        print(f"\n[blue]Configuration to be loaded on {host['name']}:[/]\n")
        print(new_ospf_config)

        conn = Netmiko(
            host=host["mgmt"],
            username=host["username"],
            password=host["password"],
            device_type=platform,
        )

        print(f"\n[green]#### Logged into {conn.find_prompt()}, woohoo! ####[/]\n")

        result = conn.send_config_set(new_ospf_config.split("\n"))

        print(escape(result))

        # with open(f"netmiko_backups/{host['name']}.conf", "w") as writer:
        #     result = conn.send_command("show run")
        #     writer.writelines(result)

        conn.disconnect()


if __name__ == "__main__":
    main()
