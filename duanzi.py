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
        """
        获取 html
        """
        headers = self.headers
        f = self.requests.get
        r = f(url, headers=headers)
        print r
        content = r.content
        return content

    def find_author(self, row):
        """
        找到该行的作者
        """
        i = row
        t = i.select(".author > strong")
        v = t[0]
        name = v.string
        return name

    def get_authors(self, soup):
        """
        获取所有作者
        """
        r = []
        elements = soup.select(".author > strong")
        for i in elements:
            t = i.string
            r.append(t)
        print '作者数量', len(r)
        return r

    def get_likes(self, soup):
        """
        获取所有赞
        """
        r = []
        elements = soup.select(".tucao-like-container > span")
        for i in elements:
            t = i.string
            r.append(t)
        print '赞的数量', len(r),
        return r

    def get_unlikes(self, soup):
        """
        获取所有踩
        """
        r = []
        elements = soup.select(".tucao-unlike-container > span")
        for i in elements:
            t = i.string
            r.append(t)
        print '踩的数量', len(r),
        return r

    def get_soup(self, html, parser_type="html.parser"):
        """
        获取 soup
        """
        content = html
        f = self.bs4.BeautifulSoup
        soup = f(content, parser_type)
        return soup


if __name__ == '__main__':
    jd = JianDan()
    url = jd.url
    html = jd.get_html(url)
    soup = jd.get_soup(html)

    r = jd.get_authors(soup)
    r = jd.get_likes(soup)
    r = jd.get_unlikes(soup)

    # rows = soup.select(".row")
    # print len(rows)
    # for i in rows:
    #     t = i.select(".tucao-like-container > span")
    #     like = t[0]
    #     print like
    #     # name = jd.find_author(i)
    #     # print name

    # 计算赞比踩多20以上的 row
    # likes = soup.select(".tucao-like-container > span")
    # for i in likes:
    #     print i.string
