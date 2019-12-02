import xml.etree.ElementTree as et
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import csv
import multiprocessing
import json


base_url = 'https://data.unistats.ac.uk/api/v4/KIS/Institution/'


def parseXML():
    tree = et.parse('db/kis20181023141616.xml')
    root = tree.getroot()
    return root


def list_2_csv():
    for a in parseXML().iter('INSTITUTION'):
        prn = a.find('UKPRN').text
        prn_list.append(prn)
        with open(('prn_list.csv'), 'w', newline='') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(prn_list)


with open('prn_list.csv', 'r') as f:
    reader = csv.reader(f)
    prn_list = list(reader)


def multi_request(param_list):
    session = requests.Session()
    json_list = []

    for param in param_list:
        r = session.get(base_url + param + '.json', auth=HTTPBasicAuth('5V1SDVL9P0TG04V102MK', 'pass'))
        print(str(r.status_code) + ": " + param)
        json_list.append(r.json())

    return json_list


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=10)
    pool_output = pool.map(multi_request, prn_list)
    pool.close()
    pool.join()

    with open('institution.json', 'w') as outfile:
        json.dump(pool_output, outfile)

    with open('institution.json') as f:
        data = json.load(f)

    pd.DataFrame(data[0]).to_csv(('institutions.csv'), index=False)
    # or maybe just
    pd.DataFrame(pool_output[0]).to_csv(('institutions.csv'), index=False)
