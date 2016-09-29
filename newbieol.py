#-*_coding:utf8-*-
#sudo pip install requests
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print 'start crawling...'

#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('course_0_(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('course_0_\d+','course_0_%s'%i,url,re.S)
            page_group.append(link)
        return page_group
#geteveryclass用来抓取每个课程块的信息
    def geteveryclass(self,source):
#        everyclass = re.findall('(<li class="free_course">.*?</li>)',source,re.S)
        everyclass = re.findall('\n<a href="/course/index.*?</div>',source,re.S)
        return everyclass
#getinfo用来从每个课程块中提取出我们需要的信息
    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('html" target="_blank">(.*?)</a></h4>',eachclass,re.S).group(1)
        info['content'] = re.search('class="con-txt pb5">(.*?)</p>',eachclass,re.S).group(1)
        info['time'] = re.search('class="course_time"><i class="fa fa-clock-o"></i>(.*?)</span>',eachclass,re.S).group(1)
        info['oldprice'] = re.search('old_price">(.*?)</span>',eachclass,re.S).group(1)

        return info
#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['time'] + '\n')
            f.writelines('class oldprice:' + each['oldprice'] + '\n\n\n')
        f.close()

if __name__ == '__main__':

    classinfo = []
    url = 'http://www.newbieol.com/course_0_1.html'
    newbiespider = spider()
    all_links = newbiespider.changepage(url,5)
    for link in all_links:
        print '正在处理页面：' + link
        html = newbiespider.getsource(link)
        everyclass = newbiespider.geteveryclass(html)
        for each in everyclass:
            info = newbiespider.getinfo(each)
            classinfo.append(info)
    newbiespider.saveinfo(classinfo)
