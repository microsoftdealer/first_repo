from pythonping import ping
import datetime
import time
from sys import argv
import csv
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

try:
    output = argv[1]
except IndexError:
    output = 'result.csv'    

ip_addresses = []
hosts = []

while True:
    input1, input2 = '', ''
    input1 = input(
            'Please, put IP address to count statistics(leave clear to close list for checks): ')
    if input1:
        input2 = input('Now put hostname: ')
    if input1 and input2:
        ip_addresses.append(input1)
        hosts.append(input2)
    elif not len(ip_addresses):
        continue
    else:
        break

counter = 0
overall_count = 0
out_data = [['time'],]

for host in hosts:
    out_data[0].append(host)

'''
Just to re/create file with output
'''
with open(output, 'w') as f:
    writer = csv.writer(f)
    for row in out_data:
        writer.writerow(row)
start = datetime.datetime.today()
counter_tup = {'success_pings': 0, 'unsuccess_pings': 0}

for host in hosts:
    counter_tup[host] = '0,00'

def count_avg_float(start, last, num_of_pings):
    start = start.replace(',','.')
    last = last.replace(',','.')
    res = str((float(start)*float((num_of_pings - 1)) + float(last)) / num_of_pings)[0:5]
    return res


def pinger(ip_addr, cnt=1):
    result = ping(ip_addr, size=40, count=cnt)
    return result

while overall_count < 15000:
        response_list = []
        workers = len(ip_addresses)
        with ThreadPoolExecutor(max_workers=workers) as exe:
            result = exe.map(pinger, ip_addresses)
            for res in result:
                response_list.append(res)
        today = datetime.datetime.today()
        inter_list = [today.strftime("%d.%m.%Y %H:%M:%S")]
        for resp in response_list:
            inter_list.append(str(resp.rtt_avg_ms)[0:5])
            if resp.success():
                counter_tup['success_pings'] += 1
            else:
                counter_tup['unsuccess_pings'] += 1
                print('There was unsuccessfull ping at ' + inter_list[0] + '\n' + '-' * 5 + '\n')
        
        with open(output, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(inter_list)
        counter +=1
        overall_count += 1
        for resp, host in zip(response_list, out_data[0][1:]):
            counter_tup[host] = count_avg_float(counter_tup[host], str(resp.rtt_avg_ms)[0:5], overall_count)

        if counter == 60:
            counter = 0
            print('\nWorking since ' + start.strftime("%d.%m.%Y %H:%M:%S"))
            print(f'\nOverall counter of runs is: {overall_count}')
            print(f'There are succesfull pings: ' + str(counter_tup['success_pings']) + '\n')
            print(f'There are unsuccessfull pings: ' + str(counter_tup['unsuccess_pings']) + '\n')
            print(f'Statistics for hosts:\n')
            for host in hosts:
                print('Average ' + host + ': ' + counter_tup[host] + '\n---\n')

        time.sleep(1)
