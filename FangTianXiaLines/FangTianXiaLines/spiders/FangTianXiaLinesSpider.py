# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector

def pagesURL(totalNum):
    urls = []
    for i in range(1, totalNum + 1):
        url = 'http://esf.wuhan.fang.com/housing/__0_0_0_0_' + str(i) + '_0_0/'
        urls.append(url)
    return urls
class FangTianXiaLinsSpider(CrawlSpider):
    name = 'spider'
    start_urls=pagesURL(1)
    NameAndUrl={'name':'','url':''}
    def parse(self, response):
        selector = Selector(response)
        lines=selector.xpath(r'//div[contains(@id,"houselist_") '
                             r'and contains(@class,"list rel")]').extract()
        with codecs.open('/users/jingjing/desktop/NameAndUrl','a','utf-8') as f:
            for everyline in lines:
                selector=Selector(text=everyline)

                self.NameAndUrl['url']=selector.xpath(r'//dl/dd/p/a[@href and @class and @target]'
                                                  r'/@href').extract()[0]
                self.NameAndUrl['name']=selector.xpath(r'//dl/dd/p/a[@href and @class and @target]'
                                                  r'/text()').extract()[0]
                self.NameAndUrl['url']=self.NameAndUrl['url']+'xiangqing/'
                if r'esf/' in self.NameAndUrl['url']:
                    self.NameAndUrl['url']=self.NameAndUrl['url'].replace('esf/','')
                f.writelines(self.NameAndUrl['name']+' '+self.NameAndUrl['url'])
                f.write('\n')

