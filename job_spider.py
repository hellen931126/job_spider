import requests
import random
import os
import pprint
import csv
import json
import time

from get_proxy import proxys
from bs4 import BeautifulSoup
from configs import headers, cookies


class Job_spider(): 
    base_url = "http://www.lagou.com/zhaopin/"
    
    def __init__(self, keyword):
        self.keyword = keyword

    def __analysis(self): 
        page = 1
        jobs = []
        while True:
            url = Job_spider.base_url + self.keyword + "/" + str(page) + "/" 
            htmls = requests.get(url, headers = random.choice(headers),cookies = cookies, proxies=random.choice(proxys)).text
            soup = BeautifulSoup(htmls, "html5lib")
            contents = soup.select(".item_con_list li")
            if len(contents) == 0:
                break     
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
                format_time = content.select(".format-time")[0].text
                info=[title, salary, company, location, tags, welfare, format_time]
                jobs.append(info)
            page += 1
            time.sleep(random.randint(3,10))
        return jobs
              
    def __save(self, jobs):
        f = open("data.csv", "a")
        writer = csv.writer(f)
        writer.writerows(jobs)
        f.close()

    def go(self):
        jobs = self.__analysis()
        self.__save(jobs)
        

spider = Job_spider("Python")
spider.go()

