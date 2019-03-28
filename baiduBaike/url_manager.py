# coding:utf-8

# url管理器

class UrlManager(object):

    # 构造函数，
    # new_urls 用来存放没有爬取数据的链接，
    # old_urls用来存放已经爬取过的链接，
    # 防止 链接被重复爬取，浪费资源
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    # 将没有爬取过的链接 添加到 new_urls集合中
    def add_new_url(self, url):
        if url is None:
            return
        # 判断将要添加的 新链接 有没有在 new_urls集合 和 old_urls集合中
        # 如果都没有的话说明这个链接还没有爬取，则添加到 new_urls集合中 等待爬取
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    
    # 在 爬虫调度器中实际上调用的是这个函数，
    # 因为在一个网页中解析出来的链接本身就是一个集合，
    # 所以需要对这个集合进行遍历，取出其中的链接一个一个的添加到 new_urls中
    def add_new_urls(self, urls):

        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    
    # 用来判断 new_urls中是否还有没有爬取的链接
    def has_new_url(self):
        # print 'has 进来了 %d' %(len(self.new_urls))
        return len(self.new_urls) != 0

    # 从 new_urls中取出一个待爬取链接并返回，同时将这个链接添加到 old_urls集合中，说明已经爬取过了
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
