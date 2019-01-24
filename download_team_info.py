# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def download_team_info():
    teams_url = 'https://nba.hupu.com/teams'

    res = requests.get(teams_url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    body = soup.body

    with open('team_info.txt', 'w') as fp:
        for teamlink in body.find_all('a', attrs = {'class': 'a_teamlink'}):
            url = teamlink['href']
            name_en = url.split('/')[-1]
            name_ch = teamlink.find('h2').getText()
            fp.write('%s\t%s\n' % (name_ch, name_en))
    fp.close()

if __name__ == '__main__':
    download_team_info()
