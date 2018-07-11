# -*-coding: utf-8 -*-

import scrapy
from HupuSpider.items import HupuspiderItem
from HupuSpider.settings import columns_ch, columns_en

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

        player_info = response.css('div.team_data')

        name = player_info.css('h2::text').extract_first()
        name = name.strip('\n')
        #self.log(name)
        if name.find(u'（') == -1:
            info_dict[u'英文名'] = name
        else:
            info_dict[u'中文名'] = name[:name.find(u'（')]
            info_dict[u'英文名'] = name[name.find(u'（')+1: name.find(u'）')]

        for p in player_info.css('div.font p'):
            info = p.css('::text').extract_first()
            if p.css('a'):
                info = info + p.css('a::text').extract_first()
            info_list = info.replace(u',', u'，').split(u'：')
            info_dict[info_list[0]] = info_list[1]

        position = info_dict[u'位置']
        if position.find(u'（') > -1:
            info_dict[u'位置'] = position[:position.find(u'（')]
            info_dict[u'号码'] = position[position.find(u'（')+1: position.find(u'号')]

        item = HupuspiderItem()
        for i in xrange(len(columns_ch)):
            item[columns_en[i]] = info_dict[columns_ch[i]]
        yield item

