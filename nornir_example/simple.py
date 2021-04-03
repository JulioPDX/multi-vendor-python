#!/usr/bin/env python

"""
Source from Nick Russo Course
on Pluralsight
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from rich import print
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():

    nornir = InitNornir(config_file="config.yaml")
    result = nornir.run(name="GET FACTS", task=napalm_get, getters=["get_facts"])

    print_result(result)


if __name__ == "__main__":
    main()
