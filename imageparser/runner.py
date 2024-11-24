from scrapy.utils.reactor import install_reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.Unsplash import UnsplashSpider

if __name__ == '__main__':
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    #query = input('')
    process.crawl(UnsplashSpider, query = 'ocean')
    process.start()

