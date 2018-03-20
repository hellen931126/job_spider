import requests
import random
import json
import pprint
import re
import csv

from get_proxy import proxys
from configs import headers, cookies, city_codes
from bs4 import BeautifulSoup


class Internship_spider():
    base_url = "http://www.shixiseng.com/interns/"
    new_city_codes = {v: k for k, v in city_codes.items()}

    def __init__(self, keyword, city):
        self.keyword = keyword
        self.city = city + "市"

    def __get_uuids(self):
        city_code = Internship_spider.new_city_codes[self.city]
        p = 1
        uuids = []
        while True:
            url = Internship_spider.base_url + "c-" + \
                city_code + "_?k=" + self.keyword + "&p=" + str(p)
            htmls = requests.get(url, headers=random.choice(
                headers), cookies=cookies, proxies=random.choice(proxys)).text
            soup = BeautifulSoup(htmls, "html5lib")
            links = soup.select(".position-list li .name-box a")
            if len(links) == 0:
                break
            for link in links:
                uuids.append(link.get('data-info'))
            p += 1
        return uuids

    def __analysis(self, uuids):
        intern_urls = []
        for uuid in uuids:
            intern_urls.append(
                "https://wap.shixiseng.com/app/intern/info?uuid=" + uuid)
        internships = []
        for intern_url in intern_urls:
            unicode_strs = requests.get(intern_url, headers=random.choice(
                headers), cookies=cookies, proxies=random.choice(proxys)).text
            htmls = unicode_strs.encode('latin-1').decode('unicode_escape')
            title = str(re.findall('"iname"\:([\s\S]*?)\,', htmls))[4:-3]
            company = {"company_name": str(re.findall('"cname"\:([\s\S]*?)\,', htmls))[4:-3],
                       "industry": str(re.findall('"industry"\:([\s\S]*?)\,', htmls))[4:-3],
                       "scale": str(re.findall('"scale"\:([\s\S]*?)\,', htmls))[4:-3]
                       }
            salary = str(re.findall('"minsal"\:([\s\S]*?)\,', htmls))[4:-3] + "-" + str(
                re.findall('"maxsal"\:([\s\S]*?)\,', htmls))[4:-3]
            frequency = str(re.findall(
                '"day"\:([\s\S]*?)\,', htmls))[3:-2] + '天每周'
            month = str(re.findall(
                '"month"\:([\s\S]*?)\,', htmls))[3:-2] + '个月'
            address = str(re.findall('"address"\:([\s\S]*?)\,', htmls))[4:-3]
            degree = str(re.findall('"degree"\:([\s\S]*?)\,', htmls))[4:-3]
            refresh_time = str(re.findall(
                '"refresh"\:([\s\S]*?)\,', htmls))[4:-3]
            info = [title, company, salary, frequency,
                    month, address, degree, refresh_time]
            internships.append(info)
        return internships

    def __save(self, internships):
        f = open("internship_data.csv", "a")
        writer = csv.writer(f)
        writer.writerows(internships)
        f.close()

    def go(self):
        uuids = self.__get_uuids()
        internships = self.__analysis(uuids)
        self.__save(internships)


spider = Internship_spider("Python", "北京")
spider.go()
