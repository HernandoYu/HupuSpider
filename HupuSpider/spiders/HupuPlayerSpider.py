# -*-coding: utf-8 -*-

import scrapy
from HupuSpider.items import HupuspiderItem

class HupuPlayerSpider(scrapy.Spider):
    name = 'hupu'
    start_urls = [
        'https://nba.hupu.com/teams',
    ]

    def parse(self, response):
        #self.log('parsing: %s' % response.url)

        teams = response.css('a.a_teamlink')
        a = 0
        for team in teams:
            team_link = team.css('::attr(href)').extract_first()
            team_player_url = team_link.replace('team', 'player')
            if team_player_url is not None:
                yield scrapy.Request(team_player_url, callback=self.parse_team)
            a += 1
            if a > 0:
                break


    def parse_team(self, response):
        #self.log('parsing: %s' % response.url)

        players =  response.css('td.left b a')
        a = 0
        for player in players:
            player_link = player.css('::attr(href)').extract_first()
            if player_link is not None:
                yield scrapy.Request(player_link, callback=self.parse_player)
            a += 1
            if a > 1:
                break


    def parse_player(self, response):
        #self.log('parsing: %s' % response.url)

        f = open('playerinfo.csv', 'a')

        player_info = response.css('div.team_data')

        name = player_info.css('h2::text').extract_first()
        f.write(name.encode('utf-8'))

        for p in player_info.css('div.font p'):
            info = p.css('::text').extract_first()
            if p.css('a'):
                info = info + p.css('a::text').extract_first()
            self.log(info)
            f.write(',')
            f.write(info.encode('utf-8'))
        f.close()

