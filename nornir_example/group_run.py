#!/usr/bin/env python

"""
Source from Nick Russo Course
on Pluralsight
"""

import json
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from rich import print
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def write_facts(task):

    # Task 1, Gather facts using NAPALM to get model
    task1_result = task.run(name="GET FACTS!", task=napalm_get, getters=["get_facts"])

    # Task 2, write data to file
    task.run(
        task=write_file,
        content=json.dumps(task1_result[0].result["get_facts"], indent=2),
        filename=f"facts/{task.host.name}_facts.json",
    )

    task2_result = task.run(name="GET Interface IP Addresses!", task=napalm_get, getters=["get_interfaces_ip"])

    task.run(
        task=write_file,
        content=json.dumps(task2_result[0].result["get_interfaces_ip"], indent=2),
        filename=f"facts/{task.host.name}_interfaces_ip.json",
    )

def main():

    nornir = InitNornir(config_file="config.yaml")
    result = nornir.run(task=write_facts)

    print_result(result)


if __name__ == "__main__":
    main()
