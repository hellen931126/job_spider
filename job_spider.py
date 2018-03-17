import requests
import random
import os
import pprint
import csv

from verify_proxy_ips import proxys
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'} 

class Job_spider(): 
    base_url = "http://www.lagou.com/zhaopin/"
    
    def __init__(self, keyword):
        self.keyword = keyword

    def __get_urls(self, end):
        urls = []
        for page in range(end):
            urls.append(Job_spider.base_url + self.keyword + "/" + str(page+1) + "/")
        return urls

    def __analysis(self, url):
        htmls = requests.get(url, headers = headers,proxies=random.choice(proxys)).text
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
        urls = self.__get_urls(end=30)
        for url in urls:
            jobs = self.__analysis(url)
            self.__save(jobs)
        

spider = Job_spider("Python")
spider.go()

