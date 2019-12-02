import xml.etree.ElementTree as et
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import csv
import multiprocessing
import json
import bs4
from bs4 import BeautifulSoup as Soup




base_url = 'https://unistats.ac.uk/Institutions/Details/'


with open('institutions.csv', 'r') as f:
    reader = csv.reader(f)
    prn_list = list(reader)
    l = [a[0] for a in prn_list]


def multi_request(param_list):
    session = requests.Session()
    json_list = []

    for param in param_list:
        r = session.get(base_url + param)
        print(str(r.status_code) + ": " + param)
        soup = Soup(r.text)
        links = soup.findAll("a", {"class": "linkSite"})
        url = links[0]['href']
        print(url)

        json_list.append([param, url])

    return json_list


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=10)
    pool_output = pool.map(multi_request, prn_list)
    pool.close()
    pool.join()

    with open('inst_urls.json', 'w') as outfile:
        json.dump(pool_output, outfile)

    with open('inst_urls.json') as f:
        data = json.load(f)

    # pd.DataFrame(data[0]).to_csv(('institutions.csv'), index=False)
    # or maybe just
    pd.DataFrame(pool_output).to_csv(('inst_urls.csv'), index=False)
