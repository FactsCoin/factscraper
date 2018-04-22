import scrapy
import dateparser
import re

from factscraper import InvalidArticleError, RELIABLE_DOMAINS
from factscraper.parsers import select_parser

class FactycznieSpider(scrapy.Spider):
    name = 'factycznie.spider'

    allowed_domains = RELIABLE_DOMAINS

    start_urls = [
        'http://fakty.interia.pl/',
        'https://www.tvn24.pl/najwazniejsze.xml',
        'http://www.rmf24.pl/fakty/feed']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,
                             self.parse_frontpage)
       
    def parse_frontpage(self, response):
        links = []
        # RSS feeds
        links.extend(response.xpath("//item/link/text()").extract())
        # fakty.interia.pl frontpage
        links.extend(response.xpath(
            "/html/body/div/div/div/section/ul/li/div/div/h2/a/@href").extract())
        for link in links:
            yield response.follow(link, callback=self.parse)

    def parse(self, response):
        try:
            return select_parser(response.url).parse(response)
        except InvalidArticleError:
            pass
