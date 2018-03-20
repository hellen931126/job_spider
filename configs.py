import json
import os
import random

f = open("config.json", "r", encoding="utf-8")
json_data = json.load(f)
headers = json_data['headers']
cookies = json_data['cookies']
city_codes = json_data['city_codes']
