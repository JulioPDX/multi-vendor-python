#!/usr/bin/env python

import logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure
from nornir_netmiko.tasks import netmiko_send_command
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from network_utils import address, mask
from rich import print
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# If running into ArubaCX sessions full error,
# run the following at the CLI "https-server session close all"

def deploy_ospf(task):

    # Task 1, Gathering facts
    task1_result = task.run(task=napalm_get, getters=["get_facts"])
    model = task1_result[0].result["get_facts"]["model"]

    # Task 2, sending same command on all devices
    task2_result = task.run(
        task=netmiko_send_command, command_string="show ip interface brief"
    )
    cmd_output = task2_result[0].result
    print(f"\n\n[green]{task.host.name}: connected as model type {model}[/]\n")
    print(cmd_output)

    # Task 3, Create configurations from templates
    # task2_result = task.run(
    #     task=template_file,
    #     template=f"{task.host.platform}_ios.j2",
    #     path="templates/",
    #     data=
    # )


def main():

    nornir = InitNornir(config_file="config.yaml")
    print("Nornir initialized with the following hosts:\n")
    for host in nornir.inventory.hosts.keys():
        print(f"{host}\n")

    result = nornir.run(task=deploy_ospf)

    print_result(result, severity_level=logging.WARNING)


if __name__ == "__main__":
    main()
