#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import bs4
import requests


class JianDan(object):
    """
    爬取煎蛋网的段子
    """
    bs4 = bs4
    requests = requests

    url = 'http://jandan.net/duan/page-303#comments'
    agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ("
             "KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
    content_type = ''
    headers = {
        'User-Agent': agent,
    }

    def get_html(self, url):

        headers = self.headers
        f = self.requests.get
        r = f(url, headers=headers)
        print r
        content = r.content
        return content

    def find_author(self, element):
        """
        找到该行的作者
        """
        i = element
        t = i.select(".author > strong")
        v = t[0]
        name = v.string
        return name

    def get_soup(self, html, parser_type="html.parser"):
        """
        获取 soup
        """
        content = html
        f = self.bs4.BeautifulSoup
        soup = f(content, parser_type)
        rows = soup.select(".row")
        for i in rows:
            name = self.find_author(i)
            print name
        return None


if __name__ == '__main__':
    jd = JianDan()
    url = jd.url
    html = jd.get_html(url)
    soup = jd.get_soup(html)
