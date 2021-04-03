from netaddr import IPNetwork

# functions to be used in jinja templates for IP management
def address(a):
    a = str(IPNetwork(a).ip)
    return a


def mask(b):
    b = str(IPNetwork(b).netmask)
    return b
