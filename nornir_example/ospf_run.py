#!/usr/bin/env python

import logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli, napalm_configure
from nornir_netmiko.tasks import netmiko_send_command
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from rich import print
from netaddr import IPNetwork
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# functions to be used in jinja templates for IP management
def address(a):
    a = str(IPNetwork(a).ip)
    return a


def mask(b):
    b = str(IPNetwork(b).netmask)
    return b


def main():
    
    
