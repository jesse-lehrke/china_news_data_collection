
# This was a simplied approach to the Pipeline and Search script (forthcoming)
# It only collects json data, urls can then be used for full scrape (verify? where is code). 
# This can be efficient and also allows pre-filtering etc
# Note that "content" returned is not full content!

# The following is printed while running:
## Pages to collect: 37
## Fetching page 37 of 37 in ...
## 0:00:01.347291     #(how long request took: for optimization of collection time)
## Entries: 35     #(how many entries on this page)
## Progress check: 1835    #(for ensuring collection actually collecting)
## Waiting: 4.524211177872525     #(sleep time)
## Max request time: 0:00:02.201813     #(how long longest request took: for optimization of collection time)
## DONE

######################################
# TO DO:
# All to function(s) with key as iterable
# output names dynamic based on key
# New functions for "initialize" and "save"
#-------------------------------------
# LONG-TERM - initialize can read test header,
# then edit as neeed (i.e. user-agent)
######################################

import requests
import json
import csv
import time
import random
from requests.exceptions import ProxyError, HTTPError, ConnectionError

PATH = './DATA/'

json_out = 'running_requests_data.jsonl'
csv_out = 'peoples_request_data.csv'

search_key = '气候变迁'
broad = True #False # Use False mostly
per_page = 50 #iirc this is the max

def connection_retry(collected_json):            
    
    try:

        print('Fetching page ' + str(data['page']) + ' of ' + str(pages) + ' in ...')

        response = requests.post(url, timeout=30, headers=header, json=data)
        
        print(response.elapsed)
        request_times.append(response.elapsed)

        res_json = response.json()

        new_dict = res_json['data']['records']
        print('Entries: ' + str(len(new_dict)))
        
        with open(PATH + json_out, 'a') as f:
            json.dump(new_dict[0], f)
            f.write('\n')

        collected_json.extend(new_dict)

        data['page'] +=1

        print('Progress check: ' + (str(len(collected_json))))

        nap_time = random.uniform(4, 8)
        print('Waiting: ' + str(nap_time))
        time.sleep(nap_time)

    except ConnectionError:
        print('Connection error...sleeping for 2 minutes')
        time.sleep(120)
        print('Retrying...')
        connection_retry(collected_json) 
    
    except:
        print('Connection error...sleeping for 2 minutes')
        time.sleep(120)
        print('Retrying...')
        connection_retry(collected_json) 
    
    return collected_json

# Data needed for scrape
header = {
    'Host': "search.people.cn",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    'Accept': "application/json, text/plain, */*",
    'Accept-Language': "en-US,en;q=0.5",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/json",
    'Content-Length': "133",
    'Origin': "http://search.people.cn",
    'DNT': "1",
    'Connection': "keep-alive",
    'Referer': "http://search.people.cn/s/?keyword=%E4%BD%8E%E7%A2%B3&st=0&_=1642524678300", # Make dynamic
    'Cookie': "__jsluid_h=15839ae46a8ceadc0378501fcdc8ca8b; sso_c=0"
}

data = {"key":search_key,"page":1,"limit":per_page,"hasTitle":True,"hasContent":True,"isFuzzy":broad,"type":0,"sortType":2,"startTime":0,"endTime":0}#  KEY???

url = "http://search.people.cn/search-platform/front/search"

# Start of scrape
response = requests.post(url, headers=header, json=data)

res_json = response.json()

pages = int(res_json['data']['pages'])
print('Pages to collect: ' + str(pages))

collected_json = []
request_times = []

while data['page'] <= pages:

    connection_retry(collected_json)

# Saving to CSV
with open(PATH + csv_out, 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, 
                        fieldnames=collected_json[0].keys(),

                       )
    fc.writeheader()
    fc.writerows(collected_json)

# Closing up
print('Max request time: ' + str(max(request_times)))
print('DONE')