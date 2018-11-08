# -*- coding: utf-8 -*-
import scrapy
import json
import re
import sys
import requests
from scrapy.spiders import CrawlSpider,Rule
from scrapy.utils.project import get_project_settings
###   www.zimuzu.tv/resource/index_json/rid/32944/channel/tv

def login_get_link(username,password):
    print(username)
    print(password)
    loginurl='http://www.zimuzu.tv/User/Login/ajaxLogin'
    surl='http://www.zimuzu.tv/today'
    header={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Origin':'http://www.zimuzu.tv',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
       'Content-Type': 'application/x-www-form-urlencoded',
        }
    data="account="+username+"&password="+password+"&remember=1"
#    print(data)
    session=requests.Session()
    login=session.post(loginurl,data=data,headers=header)
    print(login.json()) 
    getstat=session.get(surl).text 
#    print(getstat)
    m_new = re.findall(r'href="/resource/(\d{4,5})"',getstat)
    m_new = list(set(m_new))
#    print(m_new)
    today_m = []
    for i in m_new[:2]:
        json_text = session.get("http://www.zimuzu.tv/resource/index_json/rid/%s/channel/tv" %i).text.replace("\\","")
        try:
            json_text = re.search(r'(zmz003.com/\w*?)"',json_text).group(1)
#            print("success re:%s" % json_text)
            today_m.append(json_text)
        except:
#            print("failure id:%s" % json_text)
            pass
#    print(today_m)
    return today_m
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.zimuzu.tv','zmz003.com']
    Settings = get_project_settings()
#    print(type(Settings))
    renren_username  = Settings.get("RENREN_USERNAME").strip()
    renren_password  = Settings.get("RENREN_PASSWORD").strip()
 #   print(renren_username)
 #   print(renren_password)
    if renren_username =="" or renren_username =="":
        sys.exit(u'''
        请填写settings.py中的人人影视用户名(RENREN_USERNAME)和密码(RENREN_PASSWORD)再重新启动脚本。\n
        username or password not specified,please complete the settings.py with RENREN_USERNAME
        and RENREN_PASSWORD ,then restart script''')
    link_all = login_get_link(renren_username,renren_password)
    start_urls = ['http://'+i for i in link_all]
    def parse(self, response):
        item={}
        base_name = response.css("span.name-chs::text").extract_first()
        
        
        if u">正片<" not in response.text:  ###means tv 
            item['movie_name'] = [base_name+i for i in response.css("ul.tab-side >li>a::text").extract()]
            item['movie_link'] = []
            for i in response.css("div.col-infomation >div.tab-content >div.tab-pane"):
                item['movie_link'].append(self.get_tv_link(i,base_name))
            yield item
        else:
            item['movie_name'] = [base_name]
            item['movie_link'] = [self.get_movie_link(response,base_name)]
            yield item

    def get_tv_link(self, response,base_name):
        movie_link = '<p class="download">下载地址：</p><div class="download">\n'
        for i in response.css("ul.down-list >li.item"):
            if u'人人下载器' not in i.extract():#one epsode
                ep_name = base_name + i.css("span.episode::text").extract_first()
                links = i.css("a.btn::attr(href)").extract()
                for link in links:
                    if link[:4]!="http":
                        movie_link +='<p><a href="%s">%s</a></p>\n'%(link,ep_name)
        movie_link +="\n</div>"
        return movie_link


        

    def get_movie_link(self, response,base_name):
        response = response.css("div.col-infomation >div.tab-content >div.tab-pane")[0]
        movie_link = '<p class="download">下载地址：</p><div class="download">\n'
        for i in response.css("ul.down-list"):
            if u'人人下载器' not in i.extract():
                ep_name = i.css("span.filename::text").extract_first()
                links = i.css("a.btn::attr(href)").extract()
                for link in links:
                    if link[:4]!="http":
                        movie_link +='<p><a href="%s">%s</a></p>\n'%(link,ep_name)
        movie_link +="\n</div>"
        return movie_link  
        
        
        
        