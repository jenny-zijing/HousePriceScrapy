# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from FangTianXia.items import FangtianxiaItem
import logging

def NameAndUrl(fileName):
    listUrl = []
    with codecs.open(fileName, 'r', 'utf-8') as f:
        for line in f.readlines():
            url = line.split(' ')[1].strip()
            if 'http://' in url:
                listUrl.append(url)
    return listUrl


class FangTianXiaSpider(CrawlSpider):
    name='spider'
    start_urls=NameAndUrl(r'/Users/jingjing/Desktop/NameAndUrl')


    def parse(self, response):
        item = FangtianxiaItem()
        selector=Selector(response)

        try:
            item['name'] = selector.xpath(r'//div[@class="ceninfo_sq"]/h1/a/text()').extract()[0]
            if '小区网'.decode('utf-8') in item['name']:
                item['name']=item['name'].rstrip('小区网'.decode('utf-8'))
            item['price'] = selector.xpath(r'//div[@class="box detaiLtop mt20 clearfix"]'
                                       r'/dl[1]/dd/span/text()').extract()[0]
            item['xiangqingUrl']=response.url
            url=selector.xpath(r'//iframe[@hspace and @vspace and @style]/@src').extract()[0]
            item['coordinateUrl']=url
        except AttributeError,e:
            print e
            return

        item['district'] = ''
        item['circle'] = ''
        item['developer'] = ''
        item['construction_area'] = ''
        item['current_num_households'] = ''
        item['afforest_ratio'] = ''
        item['postcode'] = ''
        item['completion_time'] = ''
        item['construction_type'] = ''
        item['floor_space'] = ''
        item['total_num'] = ''
        item['volume_fraction'] = ''
        item['property_fee'] = ''

        try:
            tableSelector=selector.xpath(r'//dl[@class=" clearfix mr30"]/dd')
        except AttributeError,e:
            print e
            return

        for lineSelector in tableSelector:
            listNameAndContext=lineSelector.xpath('string(.)').extract()
            listNameAndContext=listNameAndContext[0].split('：'.decode('utf-8'))
            if listNameAndContext[0]=='所属区域'.decode('utf-8'):
                item['district']=listNameAndContext[1]
            elif listNameAndContext[0]=='环线位置'.decode('utf-8'):
                item['circle']=listNameAndContext[1]
            elif listNameAndContext[0]=='开 发 商'.decode('utf-8'):
                item['developer']=listNameAndContext[1]
            elif listNameAndContext[0]=='建筑面积'.decode('utf-8'):
                item['construction_area']=listNameAndContext[1]
            elif listNameAndContext[0]=='当期户数'.decode('utf-8'):
                item['current_num_households']=listNameAndContext[1]
            elif listNameAndContext[0]=='绿 化 率'.decode('utf-8'):
                item['afforest_ratio']=listNameAndContext[1]
            elif listNameAndContext[0]=='邮    编'.decode('utf-8'):
                item['postcode']=listNameAndContext[1]
            elif listNameAndContext[0]=='竣工时间'.decode('utf-8'):
                item['completion_time']=listNameAndContext[1]
            elif listNameAndContext[0]=='建筑类别'.decode('utf-8'):
                item['construction_type']=listNameAndContext[1]
            elif listNameAndContext[0]=='占地面积'.decode('utf-8'):
                item['floor_space']=listNameAndContext[1]
            elif listNameAndContext[0]=='总 户 数'.decode('utf-8'):
                item['total_num']=listNameAndContext[1]
            elif listNameAndContext[0]=='容 积 率'.decode('utf-8'):
                item['volume_fraction']=listNameAndContext[1]
            elif listNameAndContext[0]=='物 业 费'.decode('utf-8'):
                item['property_fee']=listNameAndContext[1]
            else:
                continue

        request=scrapy.Request(url,callback=self.parse_coordinate)
        request.meta['item'] =item
        yield request



    def parse_coordinate(self,response):
        item=response.meta['item']

        try:
            item['longitude']=re.search(r'mapInfo=.*?px:"(.*?)",py:',response.text,re.S).group(1)
            item['latitude']=re.search(r'mapInfo=.*?py:"(.*?)",isKey:',response.text,re.S).group(1)
        except AttributeError,e:
            print e
        return item




















