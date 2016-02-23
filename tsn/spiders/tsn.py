from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from items import TsnItem


class TsnSpider(CrawlSpider):
	name = "tsn"
	allowed_domains = ['tsn.ua']
	start_urls = [
	"http://ru.tsn.ua/ukrayina",
	]

	rules = [Rule(LinkExtractor(allow=['ukrayina'], deny = ['http://ru.tsn.ua/archive/ukrayina']), 'parse_story')]

	def parse_story(self, response):

		item = TsnItem()
		item['url'] = response.url
		# story['headline'] = [s.encode('utf-8') for s in response.xpath("//title/text()").extract()]
		item['headline'] = response.xpath("//title/text()").extract()[0]
		try:
			item['date'] = response.xpath(r".//*[@id='main_grid']/div[2]/div[2]/div[2]/span/span[1]/text()").extract()[0]
		except:
			item['date'] = "there is no date in a site"
		#data_from_json = json.loads(response.body)
		#story['intro'] = response.css('p.introduction::text').extract()

		return item