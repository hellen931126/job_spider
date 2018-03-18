import json
import os
import random

f = open("config.json", "r")
json_data = json.load(f)
headers = json_data['headers']
