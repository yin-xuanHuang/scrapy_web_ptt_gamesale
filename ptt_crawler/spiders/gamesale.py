# -*- coding: utf-8 -*-
import scrapy
import re

class GamesaleSpider(scrapy.Spider):
    name = 'gamesale'
    start_urls = ['https://www.ptt.cc/bbs/Gamesale/index.html']

    def __init__(self, crawl_page='0', *args, **kwargs):
        super(GamesaleSpider, self).__init__(*args, **kwargs)
        if crawl_page.isnumeric():
            self._crawl_pages = int(crawl_page)
        else:
            self._crawl_pages = 0
        self._count_pages = 0

    def parse(self, response):
        article_links = response.xpath('//*[@class="title"]/a/@href').extract()

        for article_link in article_links:
            yield scrapy.Request(response.urljoin(article_link),callback=self.parse_article, dont_filter=True)

        next_link = response.xpath('//*[@class="btn-group btn-group-paging"]/a[text()="‹ 上頁"]/@href').extract_first()

        if not next_link is None:
            self._count_pages += 1
            if self._crawl_pages != 0 and self._crawl_pages == self._count_pages:
                pass
            else:
                yield scrapy.Request(response.urljoin(next_link), callback=self.parse)


    def parse_article(self, response):
        content = response.xpath('//*[@id="main-content"]/text()').extract_first()
        header_list = response.xpath('//*[@class="article-meta-value"]/text()').extract()
        author = ""
        title = ""
        date = ""
        if len(header_list) > 3:
            author = header_list[0]
            title = header_list[2]
            date = header_list[3]

        link_id = response.xpath('//*[@class="f2"]/a/@href').extract_first()
        article_id = ""
        if not link_id is None:
            rwords = re.compile(r'.*bbs/(.*).html')
            id_object = rwords.search(link_id)
            if not id_object is None:
                article_id = id_object.group(1)

        yield {
                'author': author,
                'title': title,
                'date': date,
                'content':content,
                'article_id':article_id
                }
