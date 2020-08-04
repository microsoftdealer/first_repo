from netmiko import Netmiko
import os
from sys import argv
import yaml
import json
from jinja2 import Template, Environment, FileSystemLoader


def return_fw_list(path):
    with open(path) as f:
        if path.split('.')[-1] == 'yaml':
            fws_list = yaml.safe_load(f)
        elif path.split('.')[-1] == 'json':
            file_text = f.read()
            fws_list = json.loads(file_text)
        else:
            raise Exception('WRONG FILE AS SOURCE')
    return fws_list


def get_Netmiko(dev):
    conn = Netmiko(host=dev['host'], username=dev['username'], password=dev['password'], device_type='cisco_asa')
    return conn


def get_objects(conn):
    object_groups = conn.send_command('show runn object-g network', use_textfsm=True)
    objects = conn.send_command('show runn object network', use_textfsm=True)
    return (object_groups, objects)


def get_unknown_hosts(object_groups, objects):
    obj_host_list = [(obj['name'], obj['host']) for obj in object_groups if obj['host']]
    return obj_host_list


def get_unknown_nets(object_groups, objects):
    obj_net_list = [(obj['name'], obj['network'], obj['mask']) for obj in object_groups if obj['network']]
    return obj_net_list


def get_obj_name(obj, current_objects):
    for curr_obj in current_objects:
        if curr_obj['type'] == 'subnet':
            if curr_obj['network'] == obj[1] and curr_obj['mask'] == obj[2]:
                check = input("We've decide to choose name for your network " + obj[1] + '/' + obj[2] + ' - ' + curr_obj['name'] + ' but you may put another one: ')
                if check:
                    curr_obj['name'] = check
                return curr_obj['name']
        elif curr_obj['type'] == 'host':
            if curr_obj['host'] == obj[1]:
                check = input("We've decide to choose name for your host " + obj[1] + ' - ' + curr_obj['name'] + ' but you may put another one: ')
                return curr_obj['name']
    name = None
    return name

    
def conf_remove_nets(nets):
    conf_template = Template('''
{% for obj_gr in obj_groups.keys() %}
object-group network {{obj_gr}}
{% for val in obj_groups[obj_gr] %}
  no network-object {{ val['net'] }} {{ val['mask'] }}
{% endfor %}
{% endfor %}
''')
    obj_groups = {}
    for net in nets:
        if not obj_groups.get(net[0]):
            obj_groups[net[0]] = [{'net': net[1], 'mask': net[2]}]
        else:
            obj_groups[net[0]].append({'net': net[1], 'mask': net[2]})
            obj_grouped = {'obj_groups': obj_groups}
    conf = (conf_template.render(obj_grouped))
    return conf


def conf_remove_hosts(hosts):
    conf_template = Template('''
{% for obj_gr in obj_groups.keys() %}
object-group network {{obj_gr}}
{% for val in obj_groups[obj_gr] %}
  no network-object host {{ val['host'] }}
{% endfor %}
{% endfor %}
''')
    obj_groups = {}
    for host in hosts:
        if not obj_groups.get(host[0]):
            obj_groups[host[0]] = [{'host': host[1]}]
        else:
            obj_groups[host[0]].append({'host': host[1]})
            obj_grouped = {'obj_groups': obj_groups}
    conf = (conf_template.render(obj_grouped))
    return conf

def conf_add_objects(objects, curr_objects):
    conf_template = Template('''
{% for obj in objects.keys() %}
object-group network {{ obj }}
{% for subj in objects[obj] %}
{% if subj['exists'] %}
  network-object object {{ subj['exists'] }}
{% else %}
  network-object object {{ subj['obj_name'] }}
{% endif %}
{% endfor %}
{% endfor %}
''')
    obj_template = Template('''
{% for obj in objects.keys() %}
{% for subj in objects[obj] %}
{% if not subj['exists'] %}
object network {{ subj['obj_name'] }}
{% if subj|length == 3 %}
  host {{ subj['host'] }}
{% else %}
  subnet {{ subj['network'] }} {{ subj['mask'] }}
{% endif %}
{% endif %}
{% endfor %}
{% endfor %}
''')

    obj_groups = {}
    for obj in objects:
        exists = get_obj_name(obj, curr_objects)
        if len(obj) == 2:
            if not obj_groups.get(obj[0]):
                obj_groups[obj[0]] = [{'host': obj[1], 'obj_name': obj[0] + '_' + obj[1], 'exists': exists}]
            else:
                obj_groups[obj[0]].append({'host': obj[1], 'obj_name': obj[0] + '_' + obj[1], 'exists': exists})
        else:
            if not obj_groups.get(obj[0]):
                obj_groups[obj[0]] = [{'network': obj[1], 'mask': obj[2], 'obj_name': obj[0] + '_' + obj[1] + '_' + obj[2], 'exists': exists}]
            else:
                obj_groups[obj[0]].append({'network': obj[1], 'mask': obj[2], 'obj_name': obj[0] + '_' + obj[1] + '_' + obj[2], 'exists': exists})
    obj_grouped = {'objects': obj_groups}
    conf = (obj_template.render(obj_grouped))
    conf += (conf_template.render(obj_grouped))

    return conf


def merge_config(conf_list):
    out_conf = ''
    for conf in conf_list:
        out_conf += conf
    out_conf = out_conf.split('\n')
    out_conf = [line for line in out_conf if line] 
    return out_conf


def send_config(conf, netmiko_conn, print_check=True):
    if print_check:
        print('Sending config for ' + netmiko_conn.host)
    netmiko_conn.send_config_set(conf)
    if print_check:
        print('Done!\n****************\n')

if __name__ == "__main__":
    if not 'NET_TEXTFSM' in os.environ:
        textfsm = input('Please, put path for TEXTFSM templates, you may just put enter to use default path: ')
        if not textfsm:
            print("You've decided to choose default path.")
            os.environ["NET_TEXTFSM"] = "/home/garin/reps/ntc-templates/templates/"
            print(os.environ["NET_TEXTFSM"] + ' as NET_TEXTFSM variable was set')
        else:
            os.environ["NET_TEXTFSM"] = textfsm

    if len(argv) > 1:
        fw_list_file = argv[1]
    else:
        fw_list_file = './fws.yaml'
    
    fw_list = return_fw_list(fw_list_file)
    for fw in fw_list:
        print('Working with FW ' + fw['host'] + '\n')
        conn = get_Netmiko(fw)
        print('Getting objects lists and object groups...\n')
        object_groups, objects = get_objects(conn)
        obj_host_list = get_unknown_hosts(object_groups, objects)
        obj_net_list = get_unknown_nets(object_groups, objects)
        #for obj in obj_host_list:
        #    name =  get_obj_name(obj, objects)
        conf1 = conf_remove_hosts(obj_host_list)
        conf2 = conf_remove_nets(obj_net_list)
        conf3 = conf_add_objects(obj_host_list+obj_net_list, objects)
        fin_conf = merge_config([conf1,conf2,conf3])
        print('\n\n\nCONF IS HERE:\n\n\n' + '\n'.join(fin_conf) + '\n\n\n-----------------\n')
        send = ''
        while not send:
            send = input('\n\n\************\nDo you want to send upper config to the device? Y/n')
            if send == 'y' or send =='Y':
                send_config(fin_conf, conn)
            elif send == 'n' or send == 'N':
                break
            else:
                print("Seemed that nothing has been put =( Let's try again")
        print('FW ' + fw['host'] + ' done.\n\n----------------------------------\n\n')



