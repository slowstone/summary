import scrapy
from ..items import RankItem

class RankSpider(scrapy.Spider):
    name = 'golfer_rank'

    def start_requests(self):
        url = 'https://www.pgatour.com/stats/stat.186.html'

        yield scrapy.Request(url=url, callback=self.parse_rank)

    def parse_rank(self, response):
        for i in range(1000):
            item = RankItem()
            ss = '//*[@id="statsTable"]/tbody/tr[' + str(i+1) + ']'
            player_id = response.xpath(ss+'/td[@class="player-name"]/a/@href').extract()[0]
            player_id = player_id.split('/')[-1]
            item['player_id'] = player_id.replace('.','_')
            item['player_name'] = response.xpath(ss+'/td[@class="player-name"]/a/text()').extract()
            item['player_rank'] = response.xpath(ss+'/td[1]/text()').extract()
            yield item