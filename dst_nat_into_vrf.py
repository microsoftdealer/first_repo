import getpass
from netmiko import ConnectionHandler

def dst_nat_into_vrf():
	***
	This script made for making dst-nat from main routing table
	to VRF in KRAUD-DC-ROUTER
	***
	
    device_params = {
            'device_type': 'mikrotik_routeros',
            'port': '11209',
            'username': 'admin'}
    		
    device_params['ip'] = input('IP Address of managed device: ')
    nd_port = input('SSH port. Blank, if default(11209): ')
    if nd_port:
        device_params['port'] = nd_port
    nd_user = input('Username. Blank, if default (admin): ')
    if nd_user:
        device_params['username'] = nd_user
    device_params['password'] = getpass.getpass()
    outside_address = input('Put outside address for dstnat(default - 93.189.145.82): ')
    if not outside_address:
        outside_address = '93.189.145.82'
    #outside_int = input('Put outside interface (default - ether2(DC Kraud outside int)): ')
    #if not outside_port:
    #    outside_port = 'ether2'
    outside_port_dstnat = input('Put outside port for dstnat(Public port): ')
	inside_port = input('Put destination port(only port):') 
    inside_address = input('Put inside address for dstnat (Inside adress): ')
    commands = []
	commands.append(f'/ip firewall mangle add action=mark-connection chain=prerouting connection-state=new dst-address={outside_address} dst-port={outside_port_dstnat} in-interface={outside_int} new-connection-mark=into-vrf passthrough=yes protocol=tcp comment="DST_NAT_MANGLE_RULE_BY_SCRIPT FOR LEAKING FROM VRF"')
    commands.append(f'/ip firewall nat add action=dst-nat chain=dstnat comment="DST_NAT_MANGLE_RULE_BY_SCRIPT FOR LEAKING FROM VRF" dst-address={outside_address} dst-port={outside_port_dstnat} in-interface={outside_int} protocol=tcp to-addresses={inside_address} to-ports={inside_port}')
    
    with ConnectionHandler(**device_params) as ssh:
        ssh.send_commands(commands)
    return print(f'"{commands[0]}" and "{commands[1]}" are sent to device')
	
if __name__ == "__main__":
    dst_nat_into_vrf()
