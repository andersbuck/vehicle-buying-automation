# -*- coding: utf-8 -*-
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "fbmktscrape-css"
    start_urls = [
        'https://www.facebook.com/marketplace/charlotte/vehicles/?vehicleMake=Jeep&vehicleModel=Jeep%20Cherokee&minVehicleYear=1997&maxVehicleYear=2001&sort=CREATION_TIME_DESCEND',
    ]

    def parse(self, response):
        for quote in response.css("div._7yc _3ogd"):
            yield {
                'title': quote.css("#marketplace-modal-dialog-title::title").extract_first(),
                'price': quote.css("._f3l _4x3g::text").extract_first(),
                'mileage': quote.css("._uc9 _214v fsm fwn fcg::text").extract_first()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

