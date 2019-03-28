# coding:utf-8

import json
import codecs
import urllib
# 网页数据输出器，输出有价值的数据到文件中

class HtmlOutputer(object):

    def __init__(self):
        self.datas = []

    # 收集数据到数组中，数组中的每个数据都是一个 json 数据
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # 输出 json 数据信息
    def output_json_info(self,data):
        json_str = json.dumps(data,ensure_ascii=False,indent=4)
        print(json_str)
        

    # 输出数据到 json 文件中
    def output_json(self):
        with codecs.open("out.json","w",'utf-8') as f:

            json.dump(self.datas,f,ensure_ascii=False,indent=4)
            print("加载入文件完成...")
        
        
    # 输出数据到 html 文件中
    def output_html(self):
        
        fout = open('output.html','w')

        fout.write('<html>')
        fout.write("<body>")
        fout.write("<table border='0.1'>")

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td width='30'>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()
