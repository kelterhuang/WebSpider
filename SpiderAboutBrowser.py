from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import os
import re
import json
import urllib
# #############################################
# #############################################一定要将功能分开，这样能够进行较好的调试和操作


class Picture:
    def __init__(self):                                                 # 类的初始化操作     这个使用Chrome无头浏览器就不需要这个headers，不然出现异常
        self.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://pic.sogou.com/pics?query=%B5%E7%C4%D4%B1%DA%D6%BD&di=2&_asf=pic.sogou.com&w=05009900'             
        self.path = 'C:\\Users\\16904\\Desktop\\pictures'

    @staticmethod
    def scroll_down(driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1), "次下拉操作")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(10)                                           # 等待10秒（时间可以根据自己的网速而定），页面加载出来再执行下拉操作  全部加载出来，然后获取url

    def mkdir(self):
        folder = os.path.exists(self.path)
        if not folder:                   # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.path)            # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  new folder...  ---")
            print("---  OK  ---")
        else:
            print("---  There is this folder!  ---")

    def getinto(self):                                               # 获取图片网址
        print('开始网页get请求')                            # 使用selenium通过PhantomJS来进行网络请求
        driver = webdriver.Chrome() 
        driver.get(self.web_url)
        self.scroll_down(driver=driver, times=3)
        print('开始获取所有标签')
        all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('img', class_='img-hover')  # 获取网页中的class为cV68d的所有a标签  ?????
        driver.close()
        print("a标签的数量是：", len(all_a))  # 这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
        name = 1 
        for a in all_a:                                         # 循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
            img_str = a['src']                            # a标签中完整的srcset字符串
            # img_str = re.search('.*q=60\s2400w.(.*)q=60\s2592w',img_str,re.M)
            print('a标签的style内容是：', img_str)  
            pictures = requests.get(img_str)
            file_name = str(name)+'.jpg'
            path2 = os.path.join(self.path, file_name)
            f = open(path2, 'ab')
            f.write(pictures.content)
            name = name + 1


common = Picture()
common.mkdir()
common.getinto()