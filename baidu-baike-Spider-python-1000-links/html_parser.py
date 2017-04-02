# coding:utf-8

# 网页解析器
# 根据下载好的网页内容，从中解析出有价值的数据

from bs4 import BeautifulSoup
import re
import urlparse
import urllib

class HtmlParser(object):

    # 从网页内容中 解析出新的链接，并添加到 new_urls集合中
    def _get_new_urls(self, page_url, soup):

        new_urls = set() # 初始化 new_urls 集合，用来存放 网页中的所有链接
        # 使用 BeautifulSoup 的find_all 方法获取页面中的所有链接
        # 百度百科词条链接从 /view/123.html 变成了 /item/xxx 这样的形式了
        links = soup.find_all('a', href=re.compile(r"/item/[\u4e00-\u9fa5]{0,10}"))
      
        # 因为在 百度百科中的链接是 /item/xxx 这样的形式，他不是一个完整的链接
        # 所以 先从 links 中获取 href 属性，然后使用  urlparse.urljoin() 方法拼接成一个新的链接，这个方法具体内容百度
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)

        return new_urls

    # 获取网页中有价值的数据
    def _get_new_data(self, page_url, soup):

        res_data = {} # 用来存放 数据，json格式

        # url 链接
        res_data['url'] = page_url

        # title 百度百科词条的 title
        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()

        # summary 百度百科词条的简介
        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        return res_data

    # 网页解析函数 page_url 为要解析的网页链接，html_cont 为要解析的网页内容
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        # 实例化 BeautifulSoup 对象
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        # 获取网页中的新链接
        new_urls = self._get_new_urls(page_url, soup)
        # 获取网页中有价值的数据
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data
