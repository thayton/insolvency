#!/usr/bin/env python

import math
import json
import requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pprint import pprint

'''
https://www.thegazette.co.uk/insolvency/publish-date/2015-09-22/notice?categorycode=G405010202+-2&location-distance-1=1&numberOfLocationSearches=1&results-page-size=10

G405010202 : Appointment of liquidators
-2         : none-insolvency_personal

<input type="checkbox" name="categorycode" id="none-insolvency_personal" value="-2" checked="true" role="checkbox">
<input type="checkbox" name="categorycode" id="check-G405010202" value="G405010202" checked="checked" role="checkbox">
'''

class Scraper(object):
    def __init__(self):
        self.url = 'https://www.thegazette.co.uk/insolvency/'
        self.url_data = 'https://www.thegazette.co.uk/insolvency/publish-date/%s/notice/data.json?categorycode=%s %s&location-distance-1=1&numberOfLocationSearches=1&results-page-size=10&results-page=%d'

    def scrape(self):
        r = requests.get(self.url)
        s = BeautifulSoup(r.text, 'html.parser')

        t = s.find('label', text='Appointment of liquidators')
        i = s.find('input', id=t['for'])
        x = i['value']
        
        i = s.find('input', id='none-insolvency_personal')
        y = i['value']

        today = datetime.today()
        aweek_ago = today - timedelta(days=7)
        print aweek_ago.strftime('%Y-%m-%d')

#        u = self.url_data % (aweek_ago.strftime('%Y-%m-%d'), x,y)
        pageno = 1
        u = self.url_data % ('2015-09-22', x, y, pageno)

        r = requests.get(u)
        j = json.loads(r.text)

        total = int(j['f:total'])
        last_page = math.ceil(total / 10)

        print json.dumps(j, indent=4)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape()
