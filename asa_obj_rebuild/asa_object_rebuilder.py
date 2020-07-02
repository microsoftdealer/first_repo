from netmiko import Netmiko 


asa11 = Netmiko(host='46.61.148.178', username='admin', password='y$|1XiHSkdZL4Z_p11', device_type='cisco_asa')
asa12 = Netmiko(host='212.12.12.53', username='admin', password='y$|1XiHSkdZL4Z_p12', device_type='cisco_asa')
asa13 = Netmiko(host='92.101.254.34', username='admin', password='y$|1XiHSkdZL4Z_p13', device_type='cisco_asa')
asa16 = Netmiko(host='95.167.151.178', username='admin', password='y$|1XiHSkdZL4Z_p16', device_type='cisco_asa')
asa17 = Netmiko(host='109.195.49.113', username='admin', password='y$|1XiHSkdZL4Z_p17', device_type='cisco_asa')
gw['RU11']['obj-gr'] = asa11.send_command('show runn object-g network', use_textfsm=True)
gw['RU11']['obj-net'] = asa11.send_command('show runn object network', use_textfsm=True)
gw['RU12']['obj-gr'] = asa12.send_command('show runn object-g network', use_textfsm=True)
gw['RU12']['obj-net'] = asa12.send_command('show runn object network', use_textfsm=True)
gw['RU13']['obj-gr'] = asa13.send_command('show runn object-g network', use_textfsm=True)
gw['RU13']['obj-net'] = asa13.send_command('show runn object network', use_textfsm=True)
gw['RU16']['obj-gr'] = asa16.send_command('show runn object-g network', use_textfsm=True)
gw['RU16']['obj-net'] = asa16.send_command('show runn object network', use_textfsm=True)
gw['RU17']['obj-gr'] = asa17.send_command('show runn object-g network', use_textfsm=True)
gw['RU17']['obj-net'] = asa17.send_command('show runn object network', use_textfsm=True)

obj_host_list = [(obj['host'], obj['name']) for obj in gw['RU12']['obj-gr'] if obj['host']]
obj_net_list = [(obj['network'], obj['mask'], obj['name']) for obj in gw['RU12']['obj-gr'] if obj['network']]

gw = {'RU11': {'obj-gr': [], 'obj-net': []}, 'RU12': {'obj-gr': [], 'obj-net': []}, 'RU13': {'obj-gr': [], 'obj-net': []}, 'RU16': {'obj-gr': [], 'obj-net': []}, 'RU17': {'obj-gr': [], 'obj-net': []}}

def make_dev_jobs(dev):
    conf = get_dev_config(ip, pw, username='admin')
    config = []
    config += prepare_networks()


def get_dev_config(ip, pw, username):
    conn = Netmiko(host=ip, username=admin, password=pw, device_type='cisco_asa')
    obj_gr = conn.send_command('show runn object-g network', use_textfsm=True)
    obj_net = conn.send_command('show runn object network', use_textfsm=True)
    res = (obj_gr, obj_net)
    return res


def remove_extra_nets(new_obj, old_obj):
    clear_list = []
    fin_list = []
    for elem, num in zip(new_obj, range(0, len(new_obj))):
        mark = False
        marked_obj_name = False
        inter_elem = False
        for obj in old_obj:
            if elem[0] in obj['network']:
                mark = True
                marked_obj_name = obj['name']
                inter_elem = (elem
            else:
                pass
        if mark:
            clear_list.append(inter_elem)
        else:
            fin_list.append(elem)
    return (clear_list, fin_list)


def remove_extra_hosts(new_obj, old_obj):
    clear_list = []
    fin_list = []
    for elem, num in zip(new_obj, range(0, len(new_obj))):
        mark = False
        for obj in old_obj:
            if elem[0] in obj['host']:
                mark = True
            else:
                pass
        if mark:
            clear_list.append(elem)
        else:
            fin_list.append(elem)
    return (clear_list, fin_list)


def prepare_networks(nets_list):
    config = []
    for obj in nets_list:
        line = []
        print(f'How should we name a new object(Object - {obj[0]} {obj[1]} - {obj[2]})?')
        net_name = input()
        if not net_name:
            net_name = f'{obj[2]}_{obj[0]}'
        line.append(f'object network {net_name}')
        line.append(f'subnet {obj[0]} {obj[1]}')
        line.append(f'object-group network {obj[2]}')
        line.append(f'no network-object {obj[0]} {obj[1]}')
        line.append(f'network-object object {net_name}')
        line.append(f'!')
        config += line
    for single_line in config:
        print(single_line)
    return config


def prepare_hosts(hosts_list):
    config = []
    for obj in hosts_list:
        line = []
        print(f'How should we name a new object(Object - {obj[0]} - {obj[1]})?')
        host_name = input()
        if not host_name:
            host_name = f'{obj[1]}_{obj[0]}'
        line.append(f'object network {host_name}')
        line.append(f'host {obj[0]}')
        line.append(f'object-group network {obj[1]}')
        line.append(f'no network-object host {obj[0]}')
        line.append(f'network-object object {host_name}')
        line.append(f'!')
        config += line
    for single_line in config:
        print(single_line)
    return config

if __name__ == "__main__":

