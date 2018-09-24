#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Arrowzzzzzz@protonmail.com
#search website information through browser history
#coding：utf-8
import requests
import re
import argparse
import warnings
import time
warnings.filterwarnings('ignore') # 在shell交互时忽略https的警告
class Browser_history():    #类
    def __init__(self):
        self.Baidu_url_re = "https://www.baidu.com/s?ie=UTF-8&wd="       #百度搜索
        self.Google_url_re = "https://www.google.com/search?q="      #谷歌搜索
        self.Bing_url_re = "https://www.bing.com/search?q="      #bing搜索
        self.title = "intitle:"      #查找包含特定title的网站
        self.site = "site:"      #把搜索范围限定在某一网站中
        self.inurl = "inurl:"        #查找包含特定url的网站
        self.filetype = "filetype:"      #查找特定文件格式
        self.protect = "index of "       #查找不受保护的文件目录
        self.re_list = [r'{"title":"(.+?)","url":"(.+?)"}',r"{title:'(.+?)',url:'(.+?)'}"]      #百度结果正则
        self.re_list_google = [r'<div class="rc"><h3 class="r"><a href="(.+?)">(.+?)</a></h3><div class="s"><div>']     #google正则
        self.re_list_bing = [r'<h2><a target="_blank" href="(.+?)" h="ID=(.+?)">(.+?)</a></h2>']     #bing正则
        self.re_next_page = r'<span class="pc">(.+?)</span></strong><a href="(.+?)">'       #百度下一页正则
        self.re_next_page_google = r'<a class="pn" href="(.+?)" id="pnnext" style="text-align:left">'       #google下一页正则
        self.re_next_page_bing= r'<a class="sb_pagN sb_pagN_bp sb_bp " title="下一页" href="(.+?)" h="ID=SERP'     #bing下一页正则
        self.header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"}     #UA头
        self.list_data = []     #搜索结果
        self.page_number = 1        #计数器
        self.old_url = ""       #关键词
        self.re_list_true = ""      #使用什么搜索引擎结果正则
        self.re_next_page_true = ""     #用什么搜索引擎下一页正则
        self.search_engines_true =""        #使用什么搜索引擎
        self.bing_number = 1        #bing下一页计数器

    def find_url(self,key_word,search_engines,search_engines_type):     #搜索引擎关键词搜索
        if self.page_number == 1:       #计数器判断
            request = requests.get(search_engines + search_engines_type + key_word,headers=self.header,verify=False)         #拼接搜索的关键词的url,verify为False(把验SSL证书关掉)
            self.old_key_word = key_word        #保留搜索关键词
            if search_engines[:17] == "https://www.baidu":      #判断是否百度搜索引擎
                self.re_list_true = self.re_list        #百度结果正则
                self.re_next_page_true = self.re_next_page      #百度结果下一页正则
                self.search_engines_true = "www.baidu.com"      #搜索引擎
            elif search_engines[:17] == "https://www.googl":        #判断是否google搜索引擎
                self.re_list_true = self.re_list_google     #google结果正则
                self.re_next_page_true = self.re_next_page_google       #google结果下一页正则
                self.search_engines_true = "www.google.com"     #搜索引擎
            elif search_engines[:17] == "https://www.bing.":        #判断是否bing搜索引擎
                self.re_list_true = self.re_list_bing       #bing结果正则
                self.re_next_page_true = self.re_next_page_bing       #google结果下一页正则
                self.search_engines_true = "www.bing.com"       #搜索引擎
        else :
            request = requests.get(str(key_word), headers=self.header,verify=False)  #搜索引擎下一页链接,verify为False(把验SSL证书关掉)
        response_code = request.status_code         #获得返回状态
        if response_code != 200:        #判断是否访问成功
            print("connection failed,server response status:" + response_code)        #如果不成功返回,返回状态
            exit()      #退出
        else:
            if self.page_number == 1:       #判断是否是下一页
                print("start lookup %s for %s in %s" %(key_word, self.title, self.search_engines_true))     #关键词查找输出信息
            else :
                print("start lookup %s for %s in %s" %(self.old_key_word,self.page_number,self.search_engines_true))      #关键词下一页查找输出信息
        response_data = request.text        #将返回包以text的格式排列
        self.page_number += 1       #关键词下一页计数器计数
        self.url_re(response_data,self.re_list_true,self.re_next_page_true,self.search_engines_true)      #调用正则函数

    def url_re(self,response_data,re_list,re_next_page,search_engines_true):        #搜索结果正则
        for i in re_list:      #循环列表
            E = re.compile(i)       #将j中字段写入到规则E中
            F = E.findall(response_data)        #在页面中查找规则E，输出给F（列表）
            for z in F:     #循环列表
                if search_engines_true == "www.google.com":     #google结果正则出来是url在前标题在后
                    for y in z :        #循环列表(应为第一次循环只能把url和名称循环出来,如果一起输出,就是urlcode编码)
                        self.list_data.insert(0,y)        #添加正则内容到数据中
                elif search_engines_true == "www.bing.com":     #bing结果正则出来是url在前标题在后
                    for y in z :        #循环列表(应为第一次循环只能把url和名称循环出来,如果一起输出,就是urlcode编码)
                        if y[:4] != "SERP":     #正则会匹配出3个结果有一个就是SERP
                            self.list_data.insert(0,y)        #添加正则内容到数据中
                else :
                    for y in z :        #循环列表(应为第一次循环只能把url和名称循环出来,如果一起输出,就是urlcode编码)
                        self.list_data.append(y)        #添加正则内容到数据中
        self.url_next_page(response_data,re_list,re_next_page,search_engines_true)       #调用下一页正则函数

    def url_next_page(self,response_data,re_list,re_next_page,search_engines_true):     #搜索结果下一页正则
        E = re.compile(re_next_page)        #将j中字段写入到规则E中
        F = E.findall(response_data)        #在页面中查找规则E，输出给F（列表)
        url_page_number = ""        #搜索引擎下一页url
        if search_engines_true == "www.baidu.com":      #判断是否百度搜索引擎
            search_engines_true = "https://www.baidu.com"       #百度
            for i in F:     #循环列表
                for y in i:     #循环列表
                    url_page_number = y     #将正则找到的下一页url传递到变量中
                self.find_url(search_engines_true + url_page_number, 1,2)       #拼接下一页url并且调用find_url
#        elif search_engines_true == "www.google.com":       #判断是否google搜索引擎
        else :  # 判断是否google搜索引擎
             if search_engines_true != "www.bing.com":
                 search_engines_true = "https://www.google.com"     #google
                 for i in F:        #循环列表
                     url_page_number = i.replace("amp;", "", 3)     #google下一页会去掉页面中下一页链接里3个amp字符
                     time.sleep(3)      #防止请求过快,被google机器人机制识别到
                     self.find_url(search_engines_true + url_page_number, 1,2)      #拼接下一页url并且调用find_url
             else :
                 search_engines_true = "https://www.bing.com"  # bing
                 for i in F:  # 循环列表
                     url_page_number = i.replace("amp;", "", 2)  # bing下一页会去掉页面中下一页链接里2个amp字符
                     if int(url_page_number[38:-10]) > int(
                             self.bing_number):  # bing没有下一页的时候下一页链接是前面的链接,所以我们只要判断这次下一页中特定数字是不是比上一次大就行
                         self.bing_number = url_page_number[38:-10]  # 获取当前下一页中特定数字
                         #time.sleep(3)  # 防止请求过快,被bing机器人机制识别到
                         self.find_url(search_engines_true + url_page_number, 1, 2)  # 拼接下一页url并且调用find_url


    def touch_key_work(self,key_word,text_list):
        with open( key_word + ".txt", "a+",encoding="utf-8") as text:     #打开/创建文件
            for i in text_list:     #循环查找出来的内容
                if i[:4] == "http":     #判断是否是url
                    text.write("URL-" + i + "\n\n")
                else :
                    text.write("标题-" + i + "\n")
        del text
        print("end lookup")


if __name__ == '__main__':
     def if_se(value):      #判断se是否正常函数
         search_engines = ""        #定义初始值
         search_engines_list = ["baidu","google","bing"]        #se可选填的值
         search_engines_listing = ["https://www.baidu.com/s?ie=UTF-8&wd=","https://www.google.com/search?q=","https://www.bing.com/search?q="]       #se可选值的对应结果
         number = -1        #计数器
         for i in search_engines_list:      #循环可选值
             number += 1        #计数器技计数
             if value == i:     #填写的值是否在可选值范围内
                 search_engines = search_engines_listing[number]        #获取可选值对应的结果
                 break
         return search_engines      #返回初始值

     def if_type(value):        #判断type是否正常函数
         search_engines_type = ""       #定义初始值
         type_list = ["intitle","site","inurl","filetype","index of"]       #type可选填的值
         for i in type_list:        #循环可选值
             if value == i:     #填写的值是否在可选值范围内
                 search_engines_type = value + ":"      #拼接传入findul函数的值
                 break
         return search_engines_type     #返回初始值

     print("""
    _______                                                             
    ___    |______________________      ________________________________
    __  /| |_  ___/_  ___/  __ \_ | /| / /__  /__  /__  /__  /__  /__  /
    _  ___ |  /   _  /   / /_/ /_ |/ |/ /__  /__  /__  /__  /__  /__  /_
    /_/  |_/_/    /_/    \____/____/|__/ _____/____/____/____/____/____/
                                                                        
    The Elder Scrolls V：Skyrim is good game
     """)       #benner
     parser = argparse.ArgumentParser(prog="Arrowzzzzzz-tools-Browser_histery",usage="lookup key work for search engines",description="version=1.0",epilog=":)")        #创建一个ArgumentParser对象;prog(文件名，默认为sys.argv[0]，用来在help信息中描述程序的名称);usage(描述程序用途的字符串);description (help信息前显示的信息);epilog (help信息之后显示的信息)
     parser.add_argument('key_word', type=str, help="lookup key word")        #添加参数
     parser.add_argument('-se', type=str, help="select search engines.\nbaidu:www.baidu.com;\ngoogle:www.google.com;\nbing:www.bing.com;")        #添加可存在参数(选择搜索引擎)
     parser.add_argument("-type", type=str, help="select search engines advanced search operators.\nintitle;\nsite;\ninurl;\nfiletype;\nindex of;")     #添加可存在参数(选择搜索引擎高级语句)
     args = parser.parse_args()        #ArgumentParser
     zzzzzz = Browser_history()
     if args.se:        #判断se是否填写
         se_value = args.se
     else:      #定义se的默认值
         se_value = "baidu"
     if args.type:      #判断type是否填写
         type_value = args.type
     else:      #定义type的默认值
         type_value = "inurl"
     se = if_se(se_value)   #查看se值是否正确
     type = if_type(type_value)     #查看type值是否正确
     if se == "":       #se值不正确报错信息
         print("-se Error in value. baidu/google/bing")
         exit()
     if type == "":     #type值不正确报错信息
         print("-type Error in value. intitle/site/inurl/filetype/index of")
         exit()
     zzzzzz.find_url(args.key_word,se,type)
     zzzzzz.touch_key_work(args.key_word,zzzzzz.list_data)
