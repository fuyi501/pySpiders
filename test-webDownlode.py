
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