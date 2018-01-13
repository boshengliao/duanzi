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
        print '赞的数量', len(r)
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
        print '踩的数量', len(r)
        return r

    def get_contents(self, soup):
        """
        获取所有段子内容
        """
        r = []
        elements = soup.select(".text > p")
        for i in elements:
            t = i.string
            r.append(t)
        print '段子的数量', len(r)
        return r

    def get_good_contents(self, content, authors, likes,
                          unlikes, base_score=100):
        """
        获取优质内容. 喜欢 - 不喜欢 = n.
        """
        r = []
        n = len(authors)
        for i in range(n):
            like = likes[i]
            unlike = unlikes[i]
            score = int(like) - int(unlike)
            if score < base_score:
                continue
            r.append(i)
            print '作者: {}\n内容: {}\n'.format(authors[i], content[i])
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

    authors = jd.get_authors(soup)
    likes = jd.get_likes(soup)
    unlikes = jd.get_unlikes(soup)
    contents = jd.get_contents(soup)

    f = jd.get_good_contents
    good_content = f(contents, authors, likes, unlikes)
    print good_content
