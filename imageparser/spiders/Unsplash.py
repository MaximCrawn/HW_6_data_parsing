import scrapy
from scrapy.http import HtmlResponse
from items import ImageparserItem
from scrapy.loader import ItemLoader

class UnsplashSpider(scrapy.Spider):
    name = "Unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/s/photos/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response):
        categories = response.xpath("//a[contains(@title,'More')]")
        print()
        for category_url in categories:
            yield response.follow(category_url, callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        print()
        photo_links = response.xpath("//a[@itemprop='contentUrl']")
        category_name = response.xpath("//h1/text()").get()
        print()
        for photo_url in photo_links:
            yield response.follow(photo_url, callback=self.parse_photo, meta={'category': category_name})

    def parse_photo(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=ImageparserItem(), response=response)
        loader.add_xpath('image_name', "//h1/text()")
        loader.add_value('category', response.meta['category'])
        loader.add_xpath('images', "//button[@aria-label='Zoom in on this image']/..//img[contains(@srcset,'https')]/@srcset")

        yield loader.load_item()
