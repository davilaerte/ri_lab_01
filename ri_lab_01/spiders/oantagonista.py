# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from datetime import datetime


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    allowed_domains = ['oantagonista.com']
    start_urls = []

    data_limite = datetime.strptime('01/01/2018', '%d/%m/%Y')
    news_number = 150

    def __init__(self, *a, **kw):
        super(OantagonistaSpider, self).__init__(*a, **kw)
        with open('seeds/oantagonista.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        first_url = response.css('a.article_link::attr(href)').get()

        yield response.follow(first_url, callback=self.parse_content)
    
    def parse_content(self, response):
        data = datetime.strptime(response.css('time.published::attr(datetime)').get(), '%Y-%m-%d %H:%M:%S')

        if (data > self.data_limite):
            yield {
                'title': response.css('h1.entry-title::text').get(),
                'subtitle': '-',
                'author': '-',
                'date': data.strftime("%d/%m/%Y %H:%M:%S"),
                'section': response.css('span.categoria a::text').get(),
                'text': ''.join(response.css('div.entry-content p::text').getall()),
                'url': response.url
            }

            next_url = response.css('div.nex-prev-links a::attr(href)').re_first('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

            self.news_number -= 1

            if self.news_number > 0:
                yield response.follow(next_url, callback=self.parse_content)