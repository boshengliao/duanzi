#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

import bs4
import os
import requests
import time
import xlwt
import xlrd
from xlutils.copy import copy

class JianDan(object):
    """
    爬取煎蛋网的段子
    """
    bs4 = bs4
    requests = requests

    duanzi_index = 'http://jandan.net/duan'

    page_url = 'http://jandan.net/duan/page-{}#comments'

    url = 'http://jandan.net/duan/page-303#comments'
    agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ("
             "KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
    content_type = ''
    headers = {
        'User-Agent': agent,
    }

    # 工具
    xlwt = xlwt
    xlrd = xlrd
    copy = copy

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
                          unlikes, base_score=20):
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
            # print '作者: {}\n内容: {}\n'.format(authors[i], content[i])
        return r

    def get_current_page(self):
        """
        获取当前页码
        """
        html = self.get_html(self.duanzi_index)
        soup = self.get_soup(html)
        t = soup.select('.current-comment-page')
        txt = t[0].string
        t = txt[1:-1]
        current_page = int(t)
        return current_page

    def get_single_page_contents(self, page):
        """
        获取一页的段子
        """
        url = self.page_url.format(page)
        html = self.get_html(url)
        soup = self.get_soup(html)

        authors = self.get_authors(soup)
        likes = self.get_likes(soup)
        unlikes = self.get_unlikes(soup)
        contents = self.get_contents(soup)

        f = self.get_good_contents
        good_contents = f(contents, authors, likes, unlikes)

        sheet_name = '煎蛋网段子'
        now = datetime.datetime.now().strftime('%Y%m%d')
        filename = '{}-{}.xls'.format(sheet_name, now)
        exists = os.path.exists(filename)
        if exists:
            f = self.write_from_old
            f(good_contents, contents, authors, likes, filename)
        else:
            f = self.create_new
            f(good_contents, contents, authors, likes, filename, sheet_name)
        return None

    def write_from_old(self, good_contents, contents,
                       authors, likes, filename):
        """
        从已存在的 excel 追加内容
        """
        old = self.xlrd.open_workbook(filename)
        row = old.sheets()[0].nrows
        """
        # 不知道为什么此处的 copy 通过 self 调用会出错
        new = self.copy(old)
        TypeError: copy() takes exactly 1 argument (2 given)
        """
        new = copy(old)
        sh = new.get_sheet(0)
        f = self._sheet_write
        f(sh, row, row, good_contents, contents, authors, likes)
        new.save(filename)
        return None

    def create_new(self, good_contents, contents, authors,
                   likes, filename, sheet_name):
        """
        生成新的 excel
        """
        # 写入 excel
        wb = self.xlwt.Workbook()
        sh = wb.add_sheet(sheet_name)
        row = 0
        # 初始化第一行
        titles = ['序号', '内容', '发布者', '赞']
        tmp_num = 0
        for i in titles:
            sh.write(row, tmp_num, i)
            tmp_num += 1
        # 写入实际内容
        row += 1
        tmp_num = 1
        f = self._sheet_write
        f(sh, row, tmp_num, good_contents, contents, authors, likes)
        # 保存
        wb.save(filename)
        return None

    def _sheet_write(self, sheet, row, num, good_contents,
                     contents, authors, likes):
        """
        在 sheet 内写入数据
        """
        sh = sheet
        tmp_num = num
        for i in good_contents:
            author = authors[i]
            like = likes[i]
            content = contents[i]
            sh.write(row, 0, tmp_num)
            sh.write(row, 1, content)
            sh.write(row, 2, author)
            sh.write(row, 3, like)
            tmp_num += 1
            row += 1
        return None

    def get_today_news(self, max_page=5):
        """
        从今天的最新一页开始写入数据
        """
        current = self.get_current_page()
        for i in range(0, max_page):
            self.get_single_page_contents(current)
            current -= 1
            time.sleep(5)
        return

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
    f = jd.get_today_news()
