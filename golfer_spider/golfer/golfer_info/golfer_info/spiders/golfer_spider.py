import scrapy
from ..items import GolferItem


class GolferSpider(scrapy.Spider):
    name = "golfer_info"

    def start_requests(self):
        url = 'https://www.pgatour.com/players.html'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        prefix = 'http://www.pgatour.com'
        hrefs = response.xpath('//*[@class="name"]/a/@href').extract()
        for href in hrefs:
            href = href.split('/')
            href = '/' + href[-2] + '/' + href[-1]
            new_url = prefix + href
            yield scrapy.Request(url=new_url, callback=self.parse_golfer)

    def parse_golfer(self, response):
        item = GolferItem()
        item['player_id'] = response.url.split('/')[-1].replace('.','_')
        item['player_name'] = response.xpath('//*[@id="playersListContainer"]/div/text()').extract()[0]
        item['player_country'] = response.xpath('//*[@class="icon"]/text()').extract()[0]
        item['height'] = response.xpath('//*[@class="player-notes hidden-small"]/div[1]/div[1]/div[@class="value show-on-metric"]/text()').extract()[0]
        item['weight'] = response.xpath('//*[@class="player-notes hidden-small"]/div[1]/div[2]/div[@class="value show-on-metric"]/text()').extract()[0]
        item['age'] = response.xpath('//*[@class="player-notes hidden-small"]/div[2]/div[1]/div[@class="value"]/text()').extract()[0]
        yield item
