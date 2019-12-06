#!/usr/lib/python2.7/

import requests
import re
import datetime


COUNT_TO_KEEP = 10
logs_indexes = []
logs_indexes_dict = {}
to_remove_dict = {}
elasticsearch_url = 'http://localhost:9200'

req = requests.get(elasticsearch_url + '/_aliases?pretty=true')
indexes_json = req.json()
patt = re.compile(r'-\d{6}')

for index in indexes_json:
    m = patt.findall(index)
    if m:
        prefix = index.replace(m[0], '')
        m = m[0].replace('-', '')
        service_num = int(m)
        service_name = index[:-7]

        if service_name not in logs_indexes_dict:
            logs_indexes_dict[service_name] = [service_num]
        else:
            logs_indexes_dict[service_name].append(service_num)

for v in logs_indexes_dict.values():
    v.sort()
for k,v in logs_indexes_dict.items():
    if len(v) > COUNT_TO_KEEP:
        v = v[0:len(v)-COUNT_TO_KEEP]
        to_remove_dict[k] = v

for k,v in to_remove_dict.items():
    for num in v:
        k = str(k)
        num = str(num).zfill(6)
        print('Removing "' + k + '-' + num + '"...')
        print(elasticsearch_url + '/' + k + '-' + num)
        try:
            requests.delete(elasticsearch_url + '/' + k + '-' + num )
        except:
            pass
