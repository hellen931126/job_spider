import requests
import random
import os
import pprint
import csv
import json

from get_proxy import proxys
from bs4 import BeautifulSoup
from test import headers

# headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'} 


class Job_spider(): 
    base_url = "http://www.lagou.com/zhaopin/"
    
    def __init__(self, keyword):
        self.keyword = keyword
    
    def __isempty(self, url):
        htmls = requests.get(url, headers = random.choice(headers),proxies=random.choice(proxys)).text
        soup = BeautifulSoup(htmls, "html5lib")
        contents = soup.select(".item_con_list li")
        if contents:
            return False
        return True

    def __get_urls(self):
        urls = []
        page = 1
        while True:
            url = Job_spider.base_url + self.keyword + "/" + str(page) + "/"
            if self.__isempty(url):
                break    
            urls.append(url)
            page += 1
        return urls

    def __analysis(self, url):
        htmls = requests.get(url, headers = random.choice(headers),proxies=random.choice(proxys)).text
        soup = BeautifulSoup(htmls, "html5lib")
        contents = soup.select(".item_con_list li")

        jobs = []
        for content in contents:
            title = content.select("h3")[0].text
            salary = content.select(".money")[0].text
            company = {
                    "company_name": content.select(".company_name a")[0].text,
                    "industry": content.select(".industry")[0].text.strip()
                }
            location = content.select(".add em")[0].text
            tags = [tag.text for tag in content.select(".list_item_bot .li_b_l span")]
            welfare = content.select(".li_b_r")[0].text
            time = content.select(".format-time")[0].text
            info=[title, salary, company, location, tags, welfare, time]
            jobs.append(info)
        return jobs
    
    def __save(self, jobs):
        f = open("data.csv", "a")
        writer = csv.writer(f)
        writer.writerows(jobs)
        f.close()

    def go(self):
        urls = self.__get_urls()
        for url in urls:
            jobs = self.__analysis(url)
            self.__save(jobs)
        

spider = Job_spider("Python")
spider.go()

