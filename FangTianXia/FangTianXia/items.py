# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class FangtianxiaItem(Item):
    # define the fields for your item here like:
    name = Field()
    price=Field()
    longitude=Field()
    latitude=Field()
    district=Field()
    circle=Field()
    developer= Field()
    construction_area=Field()
    current_num_households=Field()
    afforest_ratio=Field()
    postcode=Field()
    completion_time=Field()
    construction_type=Field()
    floor_space=Field()
    total_num=Field()
    volume_fraction=Field()
    property_fee=Field()
    xiangqingUrl=Field()
    coordinateUrl=Field()


