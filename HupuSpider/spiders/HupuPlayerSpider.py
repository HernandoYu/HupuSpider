# -*-coding: utf-8 -*-

import scrapy
from HupuSpider.items import HupuspiderItem
import os

columns_ch = [u'姓名', u'位置', u'身高', u'体重', u'生日', u'球队',
              u'学校', u'选秀', u'国籍', u'本赛季薪金', u'合同']

class HupuPlayerSpider(scrapy.Spider):
    name = 'hupu'
    start_urls = [
        'https://nba.hupu.com/teams',
    ]

    def parse(self, response):
        #self.log('parsing: %s' % response.url)

        teams = response.css('a.a_teamlink')

        for team in teams:
            team_link = team.css('::attr(href)').extract_first()
            team_player_url = team_link.replace('team', 'player')
            if team_player_url is not None:
                yield scrapy.Request(team_player_url, callback=self.parse_team)



    def parse_team(self, response):
        #self.log('parsing: %s' % response.url)

        players =  response.css('td.left b a')

        for player in players:
            player_link = player.css('::attr(href)').extract_first()
            if player_link is not None:
                yield scrapy.Request(player_link, callback=self.parse_player)


    def parse_player(self, response):
        #self.log('parsing: %s' % response.url)

        info_dict = dict(zip(columns_ch, [''] * len(columns_ch)))

        if not os.path.exists('playerinfo.csv'):
            f = open('playerinfo.csv', 'a')
            f.write(','.join(columns_ch[:10]).encode('utf-8'))
        else:
            f = open('playerinfo.csv', 'a')

        player_info = response.css('div.team_data')

        name = player_info.css('h2::text').extract_first()
        name = name.rstrip('\n')
        #self.log(name)
        info_dict[u'姓名'] = name

        for p in player_info.css('div.font p'):
            info = p.css('::text').extract_first()
            if p.css('a'):
                info = info + p.css('a::text').extract_first()
            info_list = info.split(u'：')
            info_dict[info_list[0]] = info_list[1]

        value_list = [info_dict[key] for key in columns_ch[:10]]
        f.write(','.join(value_list).encode('utf-8'))

        f.close()

