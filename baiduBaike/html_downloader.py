# coding:utf-8

# 网页下载器
# 根据给的 url 下载对应的页面

import urllib2

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)

        if response.getcode() != 200:
            return None

        return response.read()
