import scrapy
from ..items import GolferImItem


class GolferImSpider(scrapy.Spider):
    name = "golfer_im"

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
            yield scrapy.Request(url=new_url, callback=self.parse_golfer_im)

    def parse_golfer_im(self,response):
        item = GolferImItem()
        player_id = response.url.split('/')[-1].replace('.','_')
        image_urls = response.xpath('/html/head/meta[@itemprop="image"]/@content').extract()
        item['player_id'] = player_id
        item['image_urls'] = image_urls
        yield item