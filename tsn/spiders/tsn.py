from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from items import TsnItem

class BbcSpider(CrawlSpider):
	name = "tsn"
	allowed_domains = ['ru.tsn.ua']
	start_urls = [
	"http://ru.tsn.ua/ukrayina",
	]

	rules = [Rule(LinkExtractor(allow=['ukrayina'], deny = ['http://ru.tsn.ua/archive/ukrayina']), 'parse_story')]

	def parse_story(self, response):

		story = TsnItem()
		story['url'] = response.url
		story['headline'] = response.xpath("//title/text()").extract()
		data_from_json = json.loads(response.body)
		#story['intro'] = response.css('p.introduction::text').extract()

		return story	