'''
Base script for setting configs.
Takes:
1) Directory of the template
2) file with template as second argument
3) json with template defined vars
4) asks to send config or hust to generate file with commands. Works with cisco ios as default. 
And it is alpha - no support of enable secrets that differs from main password
'''
from sys import argv
from netmiko import ConnectHandler
import json
import jinja2
from jinja2 import Environment, FileSystemLoader
env = jinja2.Environment()
env.globals.update(zip=zip)

template_dir = argv[1]
template_txt = argv[2]
template_dict = argv[3]

send_config = input('Should I send the config to the device? yes/no: ').lower()
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(template_txt)

with open(template_dict) as js:
   data = json.load(f)
conf_name = data['src_addr'] + template_txt.replace('.txt', '_config.txt')

with open(conf_name, 'w') as f:
    f.write(template.render(data))
	
device_params = {
        'device_type': 'cisco_ios',
        'ip': data['src_addr'],
        'username': data['login'],
        'password': data['password'],
        'secret': data['password']
    }
	
if 'y' in send_config:
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        ssh.send_config_from_file(conf_name)
		print('Do not forget to save config on device!')
else:
    print(f'{conf_name} was generated'