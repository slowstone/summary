import scrapy
from ..items import MybodygalleryItem


class MybodygallerySpider(scrapy.Spider):
    name = "mybodygallery"
    im_ids = []

    def start_requests(self):
        url = 'https://www.mybodygallery.com/'

        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        prefix = 'https://www.mybodygallery.com/'
        item = MybodygalleryItem()
        im_url = response.xpath('//*[@class="gallery-image"]/img/@src').extract()[0]
        ids = im_url.split('/')
        im_id = ids[1] +"-"+ ids[2]
        if im_id in self.im_ids:
            return
        self.im_ids.append(im_id)
        age = response.xpath('//*[@class="gallery-image"]/*/span[@class="picAge"]/b/text()').extract()
        height = response.xpath('//*[@class="gallery-image"]/*/span[@class="picHeight"]/b/text()').extract()
        weight = response.xpath('//*[@class="gallery-image"]/*/span[@class="picWeight"]/b/text()').extract()
        pansize = response.xpath('//*[@class="gallery-image"]/*/span[@class="picPantSize"]/b/text()').extract()
        shirtsize = response.xpath('//*[@class="gallery-image"]/*/span[@class="picShirtSize"]/b/text()').extract()
        bodyshape = response.xpath('//*[@class="gallery-image"]/*/span[@class="picShape"]/img/@src').extract()
        item['im_id'] = im_id
        item['im_url'] = prefix + im_url
        item['age'] = age
        item['height'] = height
        item['weight'] = weight
        item['pansize'] = pansize
        item['shirtsize'] = shirtsize
        item['bodyshape'] = bodyshape
        yield item
        next_url = response.xpath('//*[@class="picLeft"]/@href').extract()[0]
        next_url = prefix + next_url
        pre_url = response.xpath('//*[@class="picRight"]/@href').extract()[0]
        pre_url = prefix + pre_url
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=False)
        yield scrapy.Request(url=pre_url, callback=self.parse, dont_filter=False)