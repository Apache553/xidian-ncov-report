#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import os

if os.path.exists("NOSUBMIT"):
    exit()

data = {}

with open("data_3chk.json","r") as fd:
    data=json.load(fd)
    
conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',data={'username':data['_u'],'password':data['_p']})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Submit
del data['_u']
del data['_p']

result = conn.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',data=data)
print(result.text)
