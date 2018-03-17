import requests
import random
import os
import pprint
import csv

from verify_proxy_ips import proxys
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'} 

class Job_spider(): 
    url = "http://www.lagou.com/zhaopin/"
    
    def __init__(self, keyword):
        self.keyword = keyword

    def __fetch_content(self):
        htmls = requests.get(Job_spider.url + self.keyword + "/1/", headers = headers, proxies=random.choice(proxys))
        htmls = htmls.text
        return htmls

    def __analysis(self, htmls):
        soup = BeautifulSoup(htmls, "html5lib")
        contents = soup.select(".item_con_list li")
        
        jobs = []
        for content in contents:
            jobs.append({
                "title": content.select("h3")[0].text, 
                "salary": content.select(".money")[0].text,
                "company": {
                    "company_name": content.select(".company_name a")[0].text,
                    "industry": content.select(".industry")[0].text.strip()
                },
                "location": content.select(".add em")[0].text, 
                "tags": [tag.text for tag in content.select(".list_item_bot .li_b_l span")],
                "welfare": content.select(".li_b_r")[0].text,
                "time": content.select(".format-time")[0].text     
            })
        return jobs
    
    def __save(self, jobs):
        f = open("data.csv", "w")
        writer = csv.DictWriter(f, jobs[0].keys())
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
        f.close()

    def go(self):
        htmls = self.__fetch_content()
        jobs = self.__analysis(htmls)
        self.__save(jobs)


spider = Job_spider("Python")
spider.go()

