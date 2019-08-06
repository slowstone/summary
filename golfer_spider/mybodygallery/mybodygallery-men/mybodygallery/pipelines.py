# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MybodygalleryPipeline(object):
    def get_media_requests(self, item, info):
        image_url = item['im_url']
        yield scrapy.Request(image_url, meta={'im_id':item['im_id']}, dont_filter=False)

    def file_path(self, request, response=None, info=None):
        return request.meta['im_id']

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
