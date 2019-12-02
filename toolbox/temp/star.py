from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os


# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join('d:/dev/proj.py/temp/', '/star_admin/')


class MySpider(CrawlSpider):
    name = 'star'
    allowed_domains = ['www.bootstrapdash.com']
    start_urls = ['https://www.bootstrapdash.com/demo/star-admin-pro/src/demo_1/index.html']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        filename = response.url.split("/")[-2] + '.html'
        filename_with_path = os.path.join('d:/dev/proj.py/temp/star_admin/', filename)
        with open(filename_with_path, 'wb') as f:
            f.write(response.body)

