# multi-vendor-python

Messing around with Python and Multi-vendor deployments

## CLI Output... :) 

### Netmiko

```bash
(myvenv) juliopdx:~/git/multi-vendor-python$ python3 ospf_netmiko.py
{
    'host_list': [
        {
            'name': 'vIOS',
            'platform': 'ios',
            'mgmt': '192.168.10.122',
            'username': 'cisco',
            'password': 'cisco'
        },
        {
            'name': 'ArubaCX',
            'platform': 'aoscx',
            'mgmt': '192.168.10.142',
            'username': 'admin',
            'password': 'aruba'
        },
        {
            'name': 'vEOS',
            'platform': 'eos',
            'mgmt': '192.168.10.151',
            'username': 'admin',
            'password': 'arista'
        }
    ]
}

Configuration to be loaded on vIOS:

router ospf 1
    router-id 3.3.3.3
    passive-interface default
    no passive-interface GigabitEthernet0/0
interface GigabitEthernet0/0
    no shutdown
    ip address 10.0.0.3 255.255.255.0
    ip ospf 1 area 0
interface Loopback0
    ip address 192.168.3.1 255.255.255.0
    ip ospf 1 area 1
do wr

#### Logged into vIOS#, woohoo! ####

configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
vIOS(config)#router ospf 1
vIOS(config-router)#    router-id 3.3.3.3
vIOS(config-router)#    passive-interface default
vIOS(config-router)#    no passive-interface GigabitEthernet0/0
vIOS(config-router)#interface GigabitEthernet0/0
vIOS(config-if)#    no shutdown
vIOS(config-if)#    ip address 10.0.0.3 255.255.255.0
vIOS(config-if)#    ip ospf 1 area 0
vIOS(config-if)#interface Loopback0
vIOS(config-if)#    ip address 192.168.3.1 255.255.255.0
vIOS(config-if)#    ip ospf 1 area 1
vIOS(config-if)#do wr
Building configuration...

  [OK]
vIOS(config-if)#end
vIOS#

Configuration to be loaded on ArubaCX:

router ospf 1
    router-id 1.1.1.1
    passive-interface default
    area 0.0.0.0
    area 0.0.0.1
interface 1/1/1
    no shutdown
    ip address 10.0.0.1/24
    ip ospf 1 area 0.0.0.0
    no ip ospf passive
interface loopback 0
    ip address 192.168.1.1/24
    ip ospf 1 area 0.0.0.1
copy running-config startup-config

#### Logged into ArubaCX#, woohoo! ####

configure terminal
ArubaCX(config)# router ospf 1
ArubaCX(config-ospf-1)#     router-id 1.1.1.1
ArubaCX(config-ospf-1)#     passive-interface default
ArubaCX(config-ospf-1)#     area 0.0.0.0
ArubaCX(config-ospf-1)#     area 0.0.0.1
ArubaCX(config-ospf-1)# interface 1/1/1
ArubaCX(config-if)#     no shutdown
ArubaCX(config-if)#     ip address 10.0.0.1/24
ArubaCX(config-if)#     ip ospf 1 area 0.0.0.0
ArubaCX(config-if)#     no ip ospf passive
ArubaCX(config-if)# interface loopback 0
ArubaCX(config-loopback-if)#     ip address 192.168.1.1/24
ArubaCX(config-loopback-if)#     ip ospf 1 area 0.0.0.1
ArubaCX(config-loopback-if)# copy running-config startup-config

Copying configuration: [\] 
Copying configuration: [|] 
Copying configuration: [/] 
Copying configuration: [-] 
Copying configuration: [\] 
Copying configuration: [|] 
Copying configuration: [/] 
Copying configuration: [Success]
ArubaCX(config-loopback-if)# end
ArubaCX# 

Configuration to be loaded on vEOS:

ip routing
router ospf 1
    router-id 2.2.2.2
    passive-interface default
    no passive-interface Ethernet1
interface Ethernet1
    no switchport
    no shutdown
    ip address 10.0.0.2/24
    ip ospf area 0.0.0.0
interface Loopback0
    ip address 192.168.2.1/24
    ip ospf area 0.0.0.1
do wr

#### Logged into vEOS#, woohoo! ####

configure terminal
vEOS(config)#ip routing
vEOS(config)#router ospf 1
vEOS(config-router-ospf)#    router-id 2.2.2.2
vEOS(config-router-ospf)#    passive-interface default
vEOS(config-router-ospf)#    no passive-interface Ethernet1
vEOS(config-router-ospf)#interface Ethernet1
vEOS(config-if-Et1)#    no switchport
vEOS(config-if-Et1)#    no shutdown
vEOS(config-if-Et1)#    ip address 10.0.0.2/24
vEOS(config-if-Et1)#    ip ospf area 0.0.0.0
vEOS(config-if-Et1)#interface Loopback0
vEOS(config-if-Lo0)#    ip address 192.168.2.1/24
vEOS(config-if-Lo0)#    ip ospf area 0.0.0.1
vEOS(config-if-Lo0)#do wr
Copy completed successfully.
vEOS(config-if-Lo0)#end
vEOS#
(myvenv) juliopdx:~/git/multi-vendor-python$
```

### NAPALM

```bash
(myvenv) juliopdx:~/git/multi-vendor-python$ python3 basic_napalm.py 
Getting ios driver:

{
    'uptime': 133680,
    'vendor': 'Cisco',
    'os_version': 'IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.8(3)M2, RELEASE SOFTWARE (fc2)',
    'serial_number': '9IZCLMBEFRM1XWURZBBOJ',
    'model': 'IOSv',
    'hostname': 'vIOS',
    'fqdn': 'vIOS.lab.com',
    'interface_list': ['GigabitEthernet0/0', 'GigabitEthernet0/1', 'GigabitEthernet0/2', 'GigabitEthernet0/3', 'Loopback0']
}

vIOS model type: IOSv

Configuration to be loaded on vIOS:

router ospf 1
 router-id 3.3.3.3
 passive-interface default
 no passive-interface GigabitEthernet0/0
!
interface GigabitEthernet0/0
 ip address 10.0.0.3 255.255.255.0
 ip ospf 1 area 0
!
interface Loopback0
 ip address 192.168.3.1 255.255.255.0
 ip ospf 1 area 1
!

No diff on vIOS; config up to date


Saving backup for vIOS ...

Backup saved for vIOS

Job complete

Getting aoscx driver:

{
    'uptime': 1617386.104,
    'vendor': 'Aruba',
    'os_version': 'ArubaOS-CX:Virtual.10.06.0001:55dffa340d0f:202011101926',
    'serial_number': 'OVAB35E2F',
    'model': 'ArubaOS-CX_OVA',
    'hostname': 'ArubaCX',
    'fqdn': 'ArubaCX',
    'interface_list': ['1/1/9', '1/1/8', '1/1/4', '1/1/6', '1/1/7', '1/1/1', '1/1/5', '1/1/3', '1/1/2', 'loopback0']
}

ArubaCX model type: ArubaOS-CX_OVA

Feature not yet supported


Job complete

Getting eos driver:

{
    'hostname': 'vEOS',
    'fqdn': 'vEOS',
    'vendor': 'Arista',
    'model': 'vEOS',
    'serial_number': '',
    'os_version': '4.24.0F-16276801.4240F',
    'uptime': 145781,
    'interface_list': ['Ethernet1', 'Ethernet2', 'Ethernet3', 'Ethernet4', 'Ethernet5', 'Ethernet6', 'Ethernet7', 'Ethernet8', 'Loopback0', 'Management1']
}

vEOS model type: vEOS

Configuration to be loaded on vEOS:

ip routing
router ospf 1
    router-id 2.2.2.2
    passive-interface default
    no passive-interface Ethernet1
interface Ethernet1
    no switchport
    no shutdown
    ip address 10.0.0.2/24
    ip ospf area 0.0.0.0
interface Loopback0
    ip address 192.168.2.1/24
    ip ospf area 0.0.0.1

No diff on vEOS; config up to date


Saving backup for vEOS ...

Backup saved for vEOS

Job complete

(myvenv) juliopdx:~/git/multi-vendor-python$
```

### Nornir

```bash
(myvenv) juliopdx:~/git/multi-vendor-python/nornir_example$ python3 ospf_run.py 
Nornir initialized with the following hosts:

ArubaCX

vEOS

vIOS

deploy_ospf*********************************************************************
* ArubaCX ** changed : False ***************************************************
vvvv deploy_ospf ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- ArubaCX: Gathering Facts ** changed : False ------------------------------- INFO
{ 'get_facts': { 'fqdn': 'ArubaCX',
                 'hostname': 'ArubaCX',
                 'interface_list': [ '1/1/9',
                                     '1/1/8',
                                     '1/1/4',
                                     '1/1/6',
                                     '1/1/7',
                                     '1/1/1',
                                     '1/1/5',
                                     '1/1/3',
                                     '1/1/2',
                                     'loopback0'],
                 'model': 'ArubaOS-CX_OVA',
                 'os_version': 'ArubaOS-CX:Virtual.10.06.0001:55dffa340d0f:202011101926',
                 'serial_number': 'OVAB35E2F',
                 'uptime': 1617386.104,
                 'vendor': 'Aruba'}}
---- ArubaCX: show ip interface brief ** changed : False ----------------------- INFO
Interface         IP Address             Interface Status
                                           link/admin
1/1/1            10.0.0.1/24               up/up

1/1/2            No Address                down/down

1/1/3            No Address                down/down

1/1/4            No Address                down/down

1/1/5            No Address                down/down

1/1/6            No Address                down/down

1/1/7            No Address                down/down

1/1/8            No Address                down/down

1/1/9            No Address                down/down

loopback0        192.168.1.1/24            up/up


---- ArubaCX: Creating Configuration ** changed : False ------------------------ INFO
router ospf 1
    router-id 1.1.1.1
    passive-interface default
    area 0.0.0.0
    area 0.0.0.1
interface 1/1/1
    no shutdown
    ip address 10.0.0.1/24
    ip ospf 1 area 0.0.0.0
    no ip ospf passive
interface loopback 0
    ip address 192.168.1.1/24
    ip ospf 1 area 0.0.0.1

^^^^ END deploy_ospf ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* vEOS ** changed : False ******************************************************
vvvv deploy_ospf ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- vEOS: Gathering Facts ** changed : False ---------------------------------- INFO
{ 'get_facts': { 'fqdn': 'vEOS',
                 'hostname': 'vEOS',
                 'interface_list': [ 'Ethernet1',
                                     'Ethernet2',
                                     'Ethernet3',
                                     'Ethernet4',
                                     'Ethernet5',
                                     'Ethernet6',
                                     'Ethernet7',
                                     'Ethernet8',
                                     'Loopback0',
                                     'Management1'],
                 'model': 'vEOS',
                 'os_version': '4.24.0F-16276801.4240F',
                 'serial_number': '',
                 'uptime': 145845,
                 'vendor': 'Arista'}}
---- vEOS: show ip interface brief ** changed : False -------------------------- INFO
                                                                                  Address 
Interface         IP Address              Status       Protocol            MTU    Owner   
----------------- ----------------------- ------------ -------------- ----------- ------- 
Ethernet1         10.0.0.2/24             up           up                 1500            
Loopback0         192.168.2.1/24          up           up                65535            
Management1       192.168.10.151/24       up           up                 1500            

---- vEOS: Creating Configuration ** changed : False --------------------------- INFO
ip routing
router ospf 1
    router-id 2.2.2.2
    passive-interface default
    no passive-interface Ethernet1
interface Ethernet1
    no switchport
    no shutdown
    ip address 10.0.0.2/24
    ip ospf area 0.0.0.0
interface Loopback0
    ip address 192.168.2.1/24
    ip ospf area 0.0.0.1

---- vEOS: Configuring with NAPALM ** changed : False -------------------------- INFO
^^^^ END deploy_ospf ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* vIOS ** changed : False ******************************************************
vvvv deploy_ospf ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- vIOS: Gathering Facts ** changed : False ---------------------------------- INFO
{ 'get_facts': { 'fqdn': 'vIOS.lab.com',
                 'hostname': 'vIOS',
                 'interface_list': [ 'GigabitEthernet0/0',
                                     'GigabitEthernet0/1',
                                     'GigabitEthernet0/2',
                                     'GigabitEthernet0/3',
                                     'Loopback0'],
                 'model': 'IOSv',
                 'os_version': 'IOSv Software (VIOS-ADVENTERPRISEK9-M), '
                               'Version 15.8(3)M2, RELEASE SOFTWARE (fc2)',
                 'serial_number': '9IZCLMBEFRM1XWURZBBOJ',
                 'uptime': 133740,
                 'vendor': 'Cisco'}}
---- vIOS: show ip interface brief ** changed : False -------------------------- INFO

Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         10.0.0.3        YES NVRAM  up                    up      
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/2         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/3         192.168.10.122  YES DHCP   up                    up      
Loopback0                  192.168.3.1     YES NVRAM  up                    up      
---- vIOS: Creating Configuration ** changed : False --------------------------- INFO
router ospf 1
 router-id 3.3.3.3
 passive-interface default
 no passive-interface GigabitEthernet0/0
!
interface GigabitEthernet0/0
 ip address 10.0.0.3 255.255.255.0
 ip ospf 1 area 0
!
interface Loopback0
 ip address 192.168.3.1 255.255.255.0
 ip ospf 1 area 1
!

---- vIOS: Configuring with NAPALM ** changed : False -------------------------- INFO
^^^^ END deploy_ospf ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(myvenv) juliopdx:~/git/multi-vendor-python/nornir_example$ 
```
