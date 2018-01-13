#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import bs4
import requests

url = 'http://jandan.net/duan/page-303#comments'
agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ("
         "KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
content_type = ''
headers = {
    'User-Agent': agent,
}

print agent
r = requests.get(url, headers=headers)
print r
# print dir(r)
# print 'text', r.text
content = r.content
# print 'content', content

soup = bs4.BeautifulSoup(content, "html.parser")
rows = soup.select(".row")
print type(soup), type(rows)
for i in rows:
    t = i.select(".author > strong")
    v = t[0]
    name = v.string
    print name

"""
# 找到所有段子
txts = soup.select(".text > p")
# print 'txts', txts
for i in txts:
    print i
"""


def t():
    print 'hello'
    return None
