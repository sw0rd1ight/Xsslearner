# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 17:48
# @Author  : SwordLight
# @File    : analyse.py


from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []  # 定义data数组用来存储html中的数据
        self.links = []

    def handle_starttag(self, tag, attrs):
        print('handle_starttag <%s>' % tag)
        print('start tag pos:',self.getpos())
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)

    def handle_endtag(self, tag):
        print('handle_endtag </%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('handle_startendtag <%s>' % tag)
        print('start tag pos:', self.getpos())
        print('handle_startendtag <%s/>' % tag)

    def handle_data(self, data):
        print('dta pos:', self.getpos())
        print('handle_data data===>', data)
        print('dta pos:', self.getpos())

    def handle_comment(self, data):
        print('handle_comment <!--', data, '-->')

    def handle_entityref(self, name):
        print('handle_entityref &%s;' % name)

    def handle_charref(self, name):
        print('handle_entityref &#%s;' % name)



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
    parser = MyHTMLParser()
    parser.feed(html_code)
    parser.close()
    print(parser.data)
    print(parser.links)