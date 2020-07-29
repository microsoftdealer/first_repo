from netmiko import Netmiko
import os
from sys import argv
import yaml
import json
from jinja2 import Template, Environment, FileSystemLoader


def return_fw_list(path):
    with open(fw_list_file) as f:
        file_text = f.read()
        if path.split('.')[-1] == 'yaml':
            fws_list = yaml.safe_load(f)
        elif path.split('.')[-1] == 'json':
            fws_list = json.loads(file_text)
        else:
            raise Exception('WRONG FILE AS SOURCE')
    return fws_list


def get_Netmiko(dev):
    conn = Netmiko(host=dev['host'], username=dev['username'], password=dev['password'], device_type='cisco_asa')
    return conn


def get_objects(conn):
    object_groups = conn.send_command('show runn object-g network', use_textfsm=True)
    objects = conn.send('show runn object network', use_textfsm=True)
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
                return curr_obj['name']
        elif curr_obj['type'] == 'host':
            if curr_obj['host'] == obj[1]:
                return curr_obj['name']
    name = '_'.join(obj)
    return name

    
def conf_remove_net(nets):
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

def conf_add_objects(objects):
    conf_template = Template('''
    {% for obj in objects.keys() %}
    object-group network {{ obj }}
    {% for subj in objects[obj] %}
      network-object object {{subj['obj_name']}}
    {% endfor %}
    {% endfor %}
      ''')
    obj_template = Template('''
    {% for obj in objects.keys() %}
    {% for subj in in objects[obj] %}
    object network {{ subj['obj_name'] }}
    {% if len(subj) == 2 %}
    host {{ subj['host']}}
    {% else %}
    subnet {{ subj['network'] }} {{ subj['mask'] }}
    {% endif %}
    {% endfor %}
    {% endfor %}
            ''')

    obj_groups = {}
    for obj in objects:
        if len(obj) == 2:
            if not objects.get(obj[0]):
                objects[obj[0]] = [{'host': obj[1], 'obj_name': obj[0] + obj[1]}]
            else:
                objects[obj[0]].append({'host': obj[1], 'obj_name': obj[0] + obj[1]]})
        else:
            if not objects.get(obj[0]):
                objects[obj[0]] = [{'network': obj[1], 'mask': obj[2], 'obj_name': obj[0] + obj[1] + obj[2]}]
            else:
                objects[obj[0]].append({'network': obj[1], 'mask': obj[2], 'obj_name': obj[0] + obj[1] + obj[2]})
        obj_grouped = {'obj_groups': objects}

    conf = (conf_template.render(obj_grouped))

    return conf


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
        fw_list_file = './routers.yaml'



