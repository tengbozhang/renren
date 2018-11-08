# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class RenrenPipeline(object):
    def __init__(self):
        self.filet = open('movie.html', 'w',encoding="utf8")

    def close_spider(self, spider):
        self.filet.close()

    def process_item(self, item, spider):
        for i in range(len(item["movie_name"])):
            self.filet.write(item["movie_name"][i]+"\n\t\n"\
                                 +item["movie_link"][i]+"\n\n\t\n\n")
     #       self.filet.write(item["movie_name"][i]+"\n\t\n123\n\t\n123\n\t\n"\
     #                            +item["movie_link"][i]+"\n\t\n"+"omjj"+"\n\t\n" + 'dzp'+"\n\n\t\n\n")
        return item

