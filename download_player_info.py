# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def read_team_info():
    fp = open('team_info.txt', 'r')
    team_info_dict = dict()

    for line in fp.readlines():
        values = line.strip().split('\t')
        team_info_dict[values[1]] = values[0]

    return team_info_dict

def download_player_info_one_team(team_en, team_ch):
    player_url = 'https://nba.hupu.com/players/%s' % team_en

    res = requests.get(player_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    body = soup.body

    table = body.find('table', {'class': 'players_table'})
    trs = table.find_all('tr')[1:]

    player_list = list()

    for tr in trs:
        tds = tr.find_all('td')
        info_dict = dict()
        info_dict = {'team_ch': team_ch, 'team_en': team_en}
        info_dict['name_ch'] = tds[1].find('b').getText().encode('utf-8')
        info_dict['name_en'] = tds[1].find('p').find('b').getText().encode('utf-8')
        info_dict['number'] = tds[2].getText().encode('utf-8')
        info_dict['position'] = tds[3].getText().encode('utf-8')
        info_dict['height'] = tds[4].getText().encode('utf-8')
        info_dict['weight'] = tds[5].getText().encode('utf-8')
        info_dict['birthday'] = tds[6].getText().encode('utf-8')
        info_dict['annual_salary'] = tds[7].find('b').getText().encode('utf-8')
        player_list.append(info_dict)

    return player_list

def download_player_info():
    team_info_dict = read_team_info()

    player_list = list()
    for team in team_info_dict:
        player_list.extend(download_player_info_one_team(team, team_info_dict[team]))

    column_list = ['name_ch', 'name_en', 'team_ch', 'team_en', 'number', 'position',
                   'height', 'weight', 'weight', 'birthday', 'annual_salary']
    player_df = pd.DataFrame(player_list, columns = column_list)

    player_df.to_csv('player_info.csv', index=False, encoding='gbk')


if __name__ == '__main__':
    download_player_info()
