#!/usr/bin/env python

"""
Source from Nick Russo Automating Networks with Python 
Course on Pluralsight.
"""

from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load
from rich import print
import urllib3
from network_utils import address, mask

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    """
    Main execution of program
    """

    with open("hosts.yaml", "r") as handle:
        host_root = safe_load(handle)

    for host in host_root["host_list"]:

        print(f"Getting {host['platform']} driver:\n")
        driver = get_network_driver(host["platform"])
        conn = driver(
            hostname=host["mgmt"], username=host["username"], password=host["password"]
        )

        conn.open()
        facts = conn.get_facts()
        print(facts)
        print(f"\n{host['name']} model type: {facts['model']}")

        # aoscx does not support config change in current napalm driver
        if host["platform"] != "aoscx":
            with open(f"vars/{host['name']}.yaml", "r") as handle:
                ospf = safe_load(handle)

            j2_env = Environment(
                loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
            )
            # https://www.kite.com/python/answers/how-to-call-a-function-in-a-jinja2-template-in-python
            j2_env.globals["address"] = address
            j2_env.globals["mask"] = mask
            template = j2_env.get_template(
                f"templates/basic/{host['platform']}_ospf.j2"
            )
            new_ospf_config = template.render(data=ospf)

            print(f"\n[blue]Configuration to be loaded on {host['name']}:[/]\n")
            print(new_ospf_config)

            conn.load_merge_candidate(config=new_ospf_config)
            diff = conn.compare_config()

            if diff:
                print(f"\n[red]The following diff was found on {host['name']}[/]\n")
                print(diff)
            else:
                print(f"[green]No diff on {host['name']}; config up to date[/]\n")

            # NAPALM backup config option
            print(f"\nSaving backup for {host['name']} ...")

            with open(f"napalm_backups/{host['name']}.conf", "w") as writer:
                backup = conn.get_config("running")
                writer.writelines(backup["running"])

            print(f"\nBackup saved for {host['name']}")

        else:
            print("\n[red]Feature not yet supported[/]\n")

        conn.close()
        print("\n[green]Job complete[/]\n")


if __name__ == "__main__":
    main()
