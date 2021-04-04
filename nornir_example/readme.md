# Network Automation with Nornir

```bash
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
                 'uptime': 1617386.103,
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
                 'uptime': 144592,
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
                 'uptime': 132540,
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
```