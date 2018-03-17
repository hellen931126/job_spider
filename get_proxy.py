import requests 
import os 
from bs4 import BeautifulSoup 

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'} 
url = 'http://www.xicidaili.com/nn/1' 
s = requests.get(url,headers = headers) 
soup = BeautifulSoup(s.text,'lxml') 
ips = soup.select('#ip_list tr')  
proxys = list()

for i in ips:   
    ipp = i.select('td') 
    if len(ipp) < 3:
        continue
    ip = ipp[1].text 
    host = ipp[2].text
    proxy = 'http:\\' + ip + ':' + host
    proxies = {'proxy':proxy} 
    proxys.append(proxies)

print('Finished!')



