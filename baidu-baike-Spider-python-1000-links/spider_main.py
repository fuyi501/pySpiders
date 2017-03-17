# coding:utf-8

# 爬虫调度器 
# 用来管理 url管理器，网页下载器，网页解析器以及 数据输出器

import url_manager      # 导入 url管理器
import html_downloader  # 导入 网页下载器
import html_parser      # 导入 网页解析器
import html_outputer    # 导入 数据输出器

class SpiderMain(object):

    # 初始化函数，实例化 url管理器，网页下载器，网页解析器以及 数据输出器
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
    
    # 爬虫 抓取函数，整个调度过程都在这个函数中
    def craw(self, root_url):

        count = 1  # 链接计数器，用来统计抓取的链接数，当达到 1000 后退出循环，结束爬虫

        # 在 urls 对象中 添加 主要链接
        self.urls.add_new_url(root_url)

        # 循环爬取网页中的 链接，判断 urls 中是否有未爬取的链接，如果有就继续爬取，如果没有就结束爬取
        while self.urls.has_new_url():

            # try 和 except 用于异常处理，发生异常则结束爬虫
            try:
                # 从 urls 中获取一个未爬取的链接
                new_url = self.urls.get_new_url()
                # 输出抓取的 count ，以及 将要爬取的链接
                print 'craw %d : %s' % (count, new_url)
                # 使用 downloader网页下载器下载新连接的网页内容
                html_cont = self.downloader.download(new_url)
                # 使用 parser解析器 解析网页中新的链接和要获取的数据并赋值给 new_urls, new_data
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                # print new_urls,new_data # 打印 new_urls,new_data
                # 将上一步从网页中解析出来的链接添加到 url管理器中
                self.urls.add_new_urls(new_urls)
                # 将上一步从网页中获取的数据交给 outputer数据输出器 收集数据并处理数据
                self.outputer.collect_data(new_data)

                #当 爬取的链接数达到 20 的时候停止，这个值可以根据需要更改
                if count == 20: 
                    break
                # 在while循环结束时 使链接计数器 自加一
                count += 1
            except:
                print 'craw failed' # 发生异常时，输出 'craw failed'
        # 使用 outputer数据输出器 输出有用的数据到网页中
        self.outputer.output_html()

# main 函数
if __name__ == "__main__":
    # 爬数据的首链接
    root_url = "http://baike.baidu.com/item/Python"
    # 实例化爬虫对象
    obj_spider = SpiderMain()
    # 调用爬虫的 craw 函数
    obj_spider.craw(root_url)
