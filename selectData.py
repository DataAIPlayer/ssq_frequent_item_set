#****************************************************#
# -- coding:UTF-8 --
#Author:zhaobin Chu
#Date:2017-08-09
#Description: select lottery data

import urllib2
from bs4 import BeautifulSoup
from time import sleep
import re

#url = 'http://www.zhcw.com/ssq/kjgg/index.shtml'

#****************************************************
#获取网页源代码
def getPage(href):   
    headers = {  
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; \
                en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
                }  
    req = urllib2.Request(  
        url = href ,  
        headers = headers)
    try:  
        post = urllib2.urlopen(req)  
    except urllib2.HTTPError,e:  
        print e.code  
        print e.reason  
    return post.read()  
 
#****************************************************
#获取所有开奖结果网址后缀
def getSuffix():
    suffixSum = []
    index = ['_'+str(i+2) for i in range(30)]
    index.insert(0,'')
    for fix in index:
        url = 'http://www.zhcw.com/ssq/kjgg/index'+fix+'.shtml'
        page = getPage(url)
        soup = BeautifulSoup(page)
        # 获取当前网页中包含历史双色球开奖数据的Tag
        tags = soup.find_all(href = re.compile("\A/ssq/kjgg/\d"))
        length = len(tags)
        
        # 从Tag中提取当前网页中所有开奖结果网页的后缀
        for i in range(length):
            suffix = tags[i]['href']
            suffixSum.append(suffix)
        sleep(1)
    return suffixSum
    
#****************************************************
#获取所有开奖网页的双色球中奖号码，蓝球标记为b+号码
def getZJnum():
    suffixs = getSuffix()
    num = len(suffixs)
    print 'have got suffixs count: ', num
    ssq_history_ZJnumber = []
    index = 0
    for fix in suffixs:
        print index
        index += 1
        try:
            url = 'http://www.zhcw.com' + fix
            page = getPage(url)
            if index > 402: #网页源代码格式发生了变化，所以分成两部分
                #分离出包含红球开奖号码的字符串
                includeNumStr = page.split\
                                ('<span class="redball_bigst">')
                redNumber = []
                for i in range(6):
                    redNumber.append(includeNumStr[i+1].split('<')[0])
                includeBstr = page.split('<span class="blueball_bigst">')
                blueNumStr = includeBstr[1].split('<')[0]
            else:
                #分离出包含红球开奖号码的字符串
                includeNumStr = page.split('KJ_Z_NUM&quot;:&quot;')[1]
                numStr = includeNumStr.split(';')
                redNumStr = numStr[0:6] # 包含红球号码的list
                #分离蓝球开奖号码
                includeBstr = page.split('KJ_T_NUM&quot;:&quot;')[1]
                blueNumStr = includeBstr.split('&')[0] # 包含蓝球号码的
                redNumber = []
                for i in range(6):
                    redNumber.append(redNumStr[i].split('&')[0])
            blueNumber = ['b' + blueNumStr.split('&')[0]] #标记蓝球
            #print redNumber,blueNumber
            redNumber.sort()
            ssqZJnumber = redNumber + blueNumber
            #print ssqZJnumber,len(ssq_history_ZJnumber)
            ssq_history_ZJnumber.append(ssqZJnumber)
            print 'comlete count: ',len(ssq_history_ZJnumber)
            sleep(1)
        except:
            continue
    return ssq_history_ZJnumber

