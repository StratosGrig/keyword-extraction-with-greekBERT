import scrapy
import string


class MednetSpider(scrapy.Spider):
	name = "mednet"
	start_urls = ["http://www.mednet.gr/archives/older-gr.html"]

	def parse(self, response, **kwargs):

		all_hrefs = response.xpath('//a/@href').extract()
		issues_hrefs = []
		for href in all_hrefs:
			if "contents" in href:
				issues_hrefs.append(href)

		for href in issues_hrefs:
			yield scrapy.Request("http://www.mednet.gr/archives/" + href, callback=self.parse_issues)

	def parse_issues(self, response):
		all_hrefs = response.xpath('//a/@href').extract()
		abstract_hrefs = []
		for href in all_hrefs:
			if "per" in href:
				abstract_hrefs.append(href)

		for href in abstract_hrefs:
			yield scrapy.Request("http://www.mednet.gr/archives/" + href, callback=self.parse_abstracts)

	def parse_abstracts(self, response):
		title = response.css('span.HeadTitle::text').getall()
		abstract = response.css('p.AbsText::text').getall()
		keywords = response.css('span.AbsText::text').getall()

		if len(title) == 0:
			title = response.css('font.HeadTitle::text').getall()

		if len(title) == 0:
			title = response.css('p.HeadTitle::text').getall()

		if len(abstract) == 0 or len(abstract[0].split()) < 10:
			if len(keywords) >= 2 :
				abstract = keywords[0:-1]
				keywords = keywords[-1:]

		title = " ".join(title)
		abstract = " ".join(abstract)
		keywords = " ".join(keywords)

		title = title.replace("\r", " ")
		title = title.replace("\n", " ")

		abstract = abstract.replace("\r", " ")
		abstract = abstract.replace("\n", " ")

		keywords = keywords.replace("\r", " ")
		keywords = keywords.replace("\n", " ")

		if "�" not in abstract and "�" not in title and "�" not in keywords:

			if abstract != '' and keywords != '':
				yield {
					'title': title,
					'abstract': abstract,
					'keywords': keywords
				}
