# -*- coding: utf-8 -*-
import re
import json

from scrapy.selector import Selector
try:
	from scrapy.spider import Spider
except:
	from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from jobSearch.items import *
from jobSearch.misc.log import *	

class JobSpider(CrawlSpider):
	"""docstring for JobSpider"""
	name="jobinfo"
	allowed_domains=["sjtu.edu.cn"]
	start_urls=[
		"http://bbs.sjtu.edu.cn/bbsdoc?board=jobInfo",
		# "http://bbs.sjtu.edu.cn/bbsdoc,board,JobInfo,page,5892.html",
	]
	rules=[
		Rule(sle(allow=("/bbsdoc,board,JobInfo,page,589\d{1}")), follow=True, callback='parse_item')
		# Rule(sle(allow=("/bbsdoc,board,JobInfo,page,\d+")), follow=True, callback='parse_item')
	]
	def parse_item(self, response):
		items=[]
		sel=Selector(response)
		#get "http://bbs.sjtu.edu.cn/"
		base_url=get_base_url(response)
		#get the detail of current url
		for sites_even in sel.xpath('//table[@border="0"]//tr/td'):	
  			namex=sites_even.xpath('a[contains(@href, "html")]/text()')
  			if str(namex) != "[]":
  				item=JobsearchItem()
				item['catalog']=sites_even.xpath('../td[1]/text()').extract()[0]
				url_detail=sites_even.xpath('a[contains(@href, "html")]/@href').extract()[0]
				item['detailLink']=urljoin_rfc(base_url, url_detail)
  				item['name']=namex.extract()[0]
				item['publishTime']=sites_even.xpath('../td[4]/text()').extract()[0]
				item['keywords']=""
				items.append(item)
		info('parsed '+str(response))
		return items

	def _process_request(self, request):
		info('process '+str(request))
		return request	
