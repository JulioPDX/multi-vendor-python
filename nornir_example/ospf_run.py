#!/usr/bin/env python

import logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
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
    task1_result = task.run(
        name=f"{task.host.name}: Gathering Facts",
        task=napalm_get,
        getters=["get_facts"],
    )
    model = task1_result[0].result["get_facts"]["model"]
    # print(model)

    # Task 2, sending same command on all devices
    task2_result = task.run(
        name=f"{task.host.name}: show ip interface brief",
        task=netmiko_send_command,
        command_string="show ip interface brief",
    )
    cmd_output = task2_result[0].result
    # print(f"\n\n[green]{task.host.name}: connected as model type {model}[/]\n")
    # print(cmd_output)
    # print(task.host.data)

    # Task 3, Create configurations from templates
    task3_result = task.run(
        name=f"{task.host.name}: Creating Configuration",
        task=template_file,
        template=f"{task.host.platform}_ospf.j2",
        path="templates/",
        data=task.host.data,
        address=address,
        mask=mask,
    )
    ospf_config = task3_result[0].result
    # print(f"\n{ospf_config}")

    # Task 4, Configure devices using NAPALM
    if task.host.platform == "aoscx":
        task4_result = task.run(
            name=f"{task.host.name}: Configuring with Netmiko",
            task=netmiko_send_config,
            config_commands=ospf_config.split("\n"),
        )
    #     if task4_result[0].diff:
    #         print(f"\n[red]{task.host.name}: diff below\n{task4_result[0].diff}[/]\n")
    #     else:
    #         print(f"\n[green]{task.host.name}: no diff, configuration in sync![/]\n")
    else:
        task4_result = task.run(
            name=f"{task.host.name}: Configuring with NAPALM",
            task=napalm_configure,
            configuration=ospf_config,
        )


def main():

    nornir = InitNornir(config_file="config.yaml")
    print("Nornir initialized with the following hosts:\n")
    for host in nornir.inventory.hosts.keys():
        print(f"{host}\n")

    result = nornir.run(task=deploy_ospf)

    print_result(result)


if __name__ == "__main__":
    main()
