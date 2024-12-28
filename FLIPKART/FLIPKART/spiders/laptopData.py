import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader
from FLIPKART.items import FlipkartItem

class LaptopdataSpider(scrapy.Spider):
    name = "laptopData"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g"]

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(
              
            url=url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                      
                       PageMethod("wait_for_timeout", 1000),
                       PageMethod("wait_for_load_state","domcontentloaded"),
                       PageMethod("wait_for_load_state","networkidle"),
                     ],
                }
        )

    def parse(self, response):
       
       laptops = response.css('div[class="tUxRFH"] > a')

       for lp in laptops:
                item = ItemLoader(item=FlipkartItem(), selector=lp)
                item.add_css("img_name", 'div[class="Otbq5D"] img::attr("alt")')
                item.add_css("image_url", 'div[class="Otbq5D"] img::attr("src")')
                item.add_css("title", "div.yKfJKb > div.col-7-12 > div.KzDlHZ")
                item.add_css("price", "div.yKfJKb > div.BfVC2z > div.cN1yYO > div.hl05eU > div.Nx9bqj::text")
                yield item.load_item()    
       

