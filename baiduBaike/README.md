
# [Python开发简单爬虫](http://www.imooc.com/learn/563) 课程内容

> 爬虫技术用来从互联网上自动获取需要的数据。课程从对爬虫的介绍出发，引入一个简单爬虫的技术架构，然后通过是什么、怎么做、现场演示三步骤，解释爬虫技术架构中的三个模块。最后，一套优雅精美的爬虫代码实战编写，向大家演示了实战抓取百度百科1000个页面的数据全过程

## 爬虫架构

![/python-spider/spider.png](http://images.fuyix.cn//python-spider/spider.png)

## 爬虫的运行流程

![/python-spider/pachongyuanli.png](http://images.fuyix.cn//python-spider/pachongyuanli.png)

## url管理器

![/python-spider/url.png](http://images.fuyix.cn//python-spider/url.png)

## 网页下载器

![/python-spider/downloader.png](http://images.fuyix.cn//python-spider/downloader.png)

### python有哪几种网页下载器

- urllib2  python官方的基础模块
- requests  第三方包，功能更强大

### urllib2 怎么使用

- **urllib2 下载网页的方法1：最简洁方法**

```python

import urllib2

# 直接请求
response = urllib2.urlopen('http://www.baidu.com')

# 获取状态码，如果是200 表示获取成功
print response.getcode()

# 读取内容
cont = response.read()

```

- **urllib2 下载网页的方法2：添加data、http header**

```python
import urllib2

# 创建 request 对象
request = urllib2.Request(url)

# 添加数据
request.add_data('a','1')

# 添加http的header
request.add_header('User-Agent','Mozilla/5.0')

# 发送请求获取结果
response = urllib2.urlopen(request)
```

- **urllib2 下载网页的方法3：添加特殊情景的处理器**

![/python-spider/urllib2-3.png](http://images.fuyix.cn//python-spider/urllib2-3.png)

```python

import urllib2,cookielib

# 创建cookie 容器
cj = cookielib.CookieJar()

# 创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#给 urllib2 安装 opener
urllib2.install_opener(opener)

# 使用带有 cookie 的 urllib2 访问网页
response = urllib2.urlopen('http://www.baidu.com')
```

### urllib2 实例完整代码

```python

#coding:utf-8
import urllib2
import cookielib

url = "http://www.baidu.com"

print '第一种方法'
response1 = urllib2.urlopen(url)
print response1.getcode()
cont = response1.read()
print len(cont)

print '第二种方法'
request = urllib2.Request(url)
request.add_header('User-Agent','Mozilla/5.0')
response2 = urllib2.urlopen(request)
print response2.getcode()
cont = response2.read()
print len(cont)

print '第三种方法'
# 创建cookie 容器
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print response3.getcode()
print cj
cont = response3.read()
print cont
```


## 网页解析器

![/python-spider/webpaser.png](http://images.fuyix.cn//python-spider/webpaser.png)

### python 有哪几种网页解析器

![/python-spider/webparser2.png](http://images.fuyix.cn//python-spider/webparser2.png)

![/python-spider/webparserdom.png](http://images.fuyix.cn//python-spider/webparserdom.png)


### [Beaufiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/) 简介

Python 第三方库，用于 从 HTML 或 XML 中提取数据

安装并测试 bs4

- 安装：pip install beautifulsoup4
- 测试：import bs4 ; print bs4

### BeautifulSoup 的用法

![/python-spider/bs4.png](http://images.fuyix.cn//python-spider/bs4.png)

- **创建 BeautifulSoup 对象**

```python
from bs4 import BeautifulSoup

# 根据HTML网页字符串创建的 BeautifulSoup 对象
soup = BeautifulSoup（
                    html_doc,                # HTML 文档字符串
                    'html.parser',           # HTML 解析器
                    from_encoding='utf-8'    # HTML 文档的编码
                      ）

```

- **搜索节点（find_all,find）**

```python
# 方法：find_all(name,attrs,string)

# 查找所有标签为a的节点
soup.find_all('a')

# 查找所有标签为a，链接符合 /view/123.html 形式的节点
soup.find_all('a',href='/view/123.html')
soup.find_all('a',href=re.compile(r'/view/\d+\.htm'))

# 查找所有标签为div，class为abc，文字为python 的节点
soup.find_all('div',class_='abc',string='python')
```

- **访问节点信息**

```python
# 得到节点 ：<a href='1.html'>Python</a>

# 获取查找到的节点的标签名称
node.name

# 获取查找到的a节点的href属性
node['href']

# 获取查找到的a节点的链接文字
node.get_text()
```

### BeautifulSoup 实例测试

```python
# coding:utf8

from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')

print '获取所有的链接'
links = soup.find_all('a')
for link in links:
  print link.name,link['href'],link.get_text()

print '获取lacie的链接'
link_node = soup.find('a',href="http://example.com/lacie")
print link_node.name,link_node['href'],link_node.get_text()

print '正则匹配'
link_node = soup.find('a',href=re.compile(r"ill"))
print link_node.name,link_node['href'],link_node.get_text()


print '获取p段落文字'
p_node = soup.find('p',class_="title")
print p_node.name,p_node.get_text()

```

## 爬虫实例

### 开发爬虫的一般步骤

![/python-spider/baike1.png](http://images.fuyix.cn//python-spider/baike1.png)

### 爬取百度百科python词条相关词条网页

![/python-spider/baike2.png](http://images.fuyix.cn//python-spider/baike2.png)

### 实例代码：
