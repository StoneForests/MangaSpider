#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/1 17:00
# @Author  : 1o00
# @Site    : 
# @File    : 18Comic.py
# @Software: PyCharm

# !/usr/bin/env python

# -*- coding: utf-8 -*-

import requests
import re
import os
from bs4 import BeautifulSoup
import logging
import sys
import getopt

logging.basicConfig(level=logging.DEBUG)


class Album:
    def __init__(self, html, save_path):
        self.html = html
        self.save_path = save_path
        self.name = ""
        self.photo_list = []
        self.host = re.findall("https://[a-zA-Z0-9]*\\.[a-zA-Z0-9]*", html)[0]

    def get_photo_list(self):
        r = requests.get(self.html)
        r.encoding = 'utf-8'
        response = r.text
        soup = BeautifulSoup(response, "html.parser")
        self.name = re.sub(r'[/\\:*?<>|]', '', soup.find("div", itemprop="name").string.strip())
        photo_html_content = soup.find("ul", {'class': 'btn-toolbar'})
        if photo_html_content is None:
            photo_html_content = soup.find("div", {'class': 'thumb-overlay'})
        photo_html_list = re.findall("/photo/[0-9]+", str(photo_html_content))
        photo_save_path = self.save_path + "\\" + self.name
        for photo_html in photo_html_list:
            photo_html = self.host + photo_html
            self.photo_list.append(Photo(html=photo_html, save_path=photo_save_path))

    def download(self):
        self.get_photo_list()
        logging.info("开始下载漫画{}".format(self.name))
        for photo in self.photo_list:
            photo.download()
        logging.info("漫画{}下载完成".format(self.name))


class Photo:
    def __init__(self, html, save_path):
        self.html = html
        self.name = ""
        self.picture_list = []
        self.save_path = save_path

    def get_picture_list(self):
        r = requests.get(self.html)
        r.encoding = 'utf-8'
        response = r.text
        soup = BeautifulSoup(response, "html.parser")
        self.name = re.sub(r'[/\\:*?<>|]', '', soup.find('div', {'class': 'pull-left hidden'}).string.strip())
        pic_html_content = soup.find("div", "panel-body")
        pic_html_list = re.findall("https:.+photos/[0-9]+/[0-9]+.jpg", str(pic_html_content))
        pic_save_path = self.save_path + "\\" + self.name
        for pic_html in pic_html_list:
            picture = Picture(pic_html, pic_save_path)
            self.picture_list.append(picture)

    def download(self):
        self.get_picture_list()
        logging.info("开始下载章节{}".format(self.name))
        for pic in self.picture_list:
            pic.download()
        logging.info("章节{}下载完成".format(self.name))


class Picture:
    def __init__(self, html, save_path):
        self.html = html
        self.name = ""
        self.save_path = save_path

    def download(self):
        self.name = re.findall("[0-9]+.jpg", self.html)[0]
        if not os.path.isdir(self.save_path):
            try:
                os.makedirs(self.save_path)
            except Exception as e:
                logging.error(e)
                exit()
        pic_save_path_with_filename = self.save_path + '\\' + self.name
        if os.path.isfile(pic_save_path_with_filename):
            logging.info("图片：{}已存在".format(pic_save_path_with_filename))
            pass
        else:
            img_data = requests.get(self.html)
            with open(pic_save_path_with_filename, 'wb')as f:
                f.write(img_data.content)
                logging.info("正在保存{}".format(self.name))
                f.close()


if __name__ == '__main__':
    save_path = os.path.abspath(u'.\\18comic_output')
    # parse params
    opts, args = getopt.getopt(sys.argv[1:], 'hi:s:', ['id=', 'save='])
    for opt, arg in opts:
        if opt == '-h':
            print('python 18Comic.py -i <manga_id> -s <output_folder_path>')
            sys.exit()
        if opt in ['-i', '--id']:
            html = "https://18comic.vip/album/" + arg
        elif opt in ['--save', '-s']:
            save_path = arg
    # running
    html = "https://18comic.vip/album/"
    album = Album(html, save_path)
    album.download()
