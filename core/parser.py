# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 17:48
# @Author  : SwordLight
# @File    : analyse.py


from html.parser import HTMLParser


class HtmlParser(HTMLParser):
    '''
    解析html
    找到所有的目标字符出现的上下文
    '''

    def __init__(self, target):
        HTMLParser.__init__(self)
        self.context = []  # 定义data数组用来存储html中的数据
        self.target = target

    def handle_starttag(self, tag, attrs):
        '''
        遇到开始标签时调用
        遍历标签的属性，寻找目标字符串
        如果位于style属性或者标签之中，则上下文为CSS
        不然则为attr
        :param tag:
        :param attrs:
        :return:
        '''

        # 上个目标的结束位置
        if len(self.context) > 0 and "end_position" not in self.context[-1].keys():
            self.context[-1].update({"end_position": self.getpos()})

        for k, v in attrs:
            if self.target in v:
                if k == "style" or tag == 'style':
                    self.context.append({"context": "css", "tag":tag,"start_position": self.getpos()})
                elif k.startswith("on"):
                    self.context.append({"context": "script", "start_position": self.getpos()})
                else:
                    self.context.append({"context": "attr", "start_position": self.getpos()})


    def handle_endtag(self, tag):
        if len(self.context) > 0 and "end_position" not in self.context[-1].keys():
            self.context[-1].update({"end_position": self.getpos()})



    def handle_data(self, data):
        '''
        在标签之间的文本中找到目标字符串
        如果标签为script,则上下文为script
        不然则为html
        :param data:
        :return:
        '''
        if len(self.context) > 0 and "end_position" not in self.context[-1].keys():
            self.context[-1].update({"end_position": self.getpos()})

        if self.target in data:
            if self.lasttag == 'script':
                self.context.append({"context": "script", "start_position": self.getpos()})
            else:
                self.context.append({"context": "html", "start_position": self.getpos()})

    def handle_comment(self, data):
        '''
        在comment中查找目标字符串
        中欧到了则新增一个上下文为comment
        :param data:
        :return:
        '''
        if len(self.context) > 0 and "end_position" not in self.context[-1].keys():
            self.context[-1].update({"end_position": self.getpos()})

        if self.target in data:
            self.context.append({"context": "comment", "start_position": self.getpos()})


if __name__ == "__main__":
    html_code = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Less-1 **Error Based- String**</title>
</head>

<body bgcolor="#000000">
<div style=" margin-top:70px;color:#FFF; font-size:23px; text-align:center">Welcome&nbsp;&nbsp;&nbsp;<font color="#FF0000"> Dhakkan </font><br>
<font size="3" color="#FFFF00">







 
SELECT * FROM users WHERE id='WFloRb' LIMIT 0,1<br><font color= "#FFFF00"></font></font> </div></br></br></br><center>
<img src="../images/Less-1.jpg" /></center>
</body>
</html>'''
    parser = HtmlParser("WFloRb")
    parser.feed(html_code)
    print(parser.context)
    parser.close()
