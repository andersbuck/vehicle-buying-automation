# -*- coding: utf-8 -*-
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "bdauctionscrape-css"
    start_urls = [
        'http://www.bdaaofnc.com/runlist.asp',
    ]

    def parse(self, response):
        for quote in response.css("table tr"):
            yield {
                'make': quote.css("td:nth-child(4)::text").extract_first(),
                'model': quote.css("td:nth-child(6)::text").extract_first(),
                'year': quote.css("td:nth-child(5)::text").extract_first(),
                'miles': quote.css("td:nth-child(8)::text").extract_first()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

