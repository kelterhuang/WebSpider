from selenium import webdriver
from bs4 import BeautifulSoup
import re
import logging
import requests
# import time

logging.disable()
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname) - %(message)s')


class Spider:
    def __init__(self):
        self.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe'
                        'bKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
        self.web_url = 'https://card.niconi.co.ni/live'
        self.path = 'C:\\Users\\16904\\Desktop\\JMusic.txt'        # 网址名地址

    @staticmethod
    def web_request(url):
        logging.debug('开始网页get请求')
        driver = requests.get(url)
        all_a = BeautifulSoup(driver.text, 'lxml')
        return all_a

    @staticmethod
    def web_driver(url):
        webchorme = webdriver.Chrome()
        # webchorme.minimize_window()
        webchorme.get(url)
        result = webchorme.page_source
        webchorme.close()
        allinfo = BeautifulSoup(result, 'lxml')
        return allinfo

    @staticmethod
    def re_get(all_a):
        pattern = re.compile(r'Live_(.{4,5}).json')
        result = pattern.findall(str(all_a))
        logging.debug('当前页面共{0}个网站'.format(len(result)))
        return result

    @staticmethod
    def re_title(all_a):
        unallow_str = ['?', '？', '、', '\\', '/', '*', '“', '”', '<', '>', '|', ':', '：']
        pattern = re.compile(r'<title>(.*) - LLSIF 打歌模拟</title>')
        title = pattern.findall(str(all_a))[0]
        title = str(title)
        for each1 in range(len(title)):           # 修复提取文件名不规则导致无法生成文本的bug
            for each2 in unallow_str:
                if title[each1] == each2:
                    print(each2)
                    title = title.replace(title[each1], ' ')
        print(title)
        return title

    @staticmethod
    def re_data(all_a):
        pattern = re.compile(r'timing_sec\\\":(\d*.\d*),\\\"notes_attribute\\\":\d,\\\"notes_level\\\":\d,\\\"eff'
                             r'ect\\\":(\d),\\\"effect_value\\\":(\d*.\d*),\\\"position\\\":(\d*)}')
        data = pattern.findall(str(all_a))
        if len(data) == 0:                                     # 修复特殊网页格式bug
            pattern = re.compile(r'{\\\"notes_level\\\":\d,\\\"effect\\\":(\d),\\\"position\\\":(\d),\\\"notes_att'
                                 r'ribute\\\":\d,\\\"timing_sec\\\":(\d*.\d*),\\\"effect_value\\\":(\d*.\d*)}')
            data = pattern.findall(str(all_a))
            # print(data)
            data1 = []
            data2 = []
            # print(len(data))
            for ele in range(len(data)):
                data2.append(data[ele][2])
                data2.append(data[ele][0])
                data2.append(data[ele][3])
                data2.append(data[ele][1])
                data1.append(data2)
                data2 = []
            data = data1
            # print(data)
        return data

    def website(self, result):
        file = open(self.path, 'w')
        for each in result:
            website = 'https://card.niconi.co.ni/live/Live_'+each+'.json'
            file.write(str(website)+'\n')
        file.close()

    @staticmethod
    def txt_head():
        stren = 'Dim st\nWhile True\n\tIf 10088038 = GetPixelColor(950, 500,1) Then\n\t\tEx' \
                               'it While\n\tEnd If\nWend\nst = TickCount() - 70'
        return stren

    def data_deal_txt(self, firstdata, seconddata, thirddata, fourthdata):
        firstdata1 = int(firstdata*1000)
        stren1 = '\nDelay st + {0} - TickCount()'.format(firstdata1)
        if seconddata is not (3 or 13):
            print(seconddata)
            firstdata2 = firstdata1 + 15
            stren2 = '\nDelay st + {0} - TickCount()'.format(firstdata2)
        else:
            thirddata = int(thirddata*1000)+firstdata1
            stren2 = '\nDelay st + {0} - TickCount()'.format(thirddata)
        position = self.location_deal(fourthdata)
        return stren1, stren2, position

    def data_handel_list(self, f, s, t, r):
        down_time = int(f*1000)
        if s is not (3 or 13):
            up_time = down_time + 15
        else:
            up_time = down_time + int(t*1000)
        position = self.location_deal(r)
        return down_time, up_time, position,

    @staticmethod
    def bubble_sort(lists):           # 冒泡
        # print(len(lists)-1)
        for time1 in range(len(lists)-1):
            for time2 in range((len(lists))-1-time1):
                if lists[time2] > lists[time2 + 1]:
                    temp = lists[time2]
                    lists[time2] = lists[time2 + 1]
                    lists[time2 + 1] = temp
        return lists

    @staticmethod
    def txt_write(lists):            # 实现文本写入，并相邻时间整合
        stren = []
        for each in range(len(lists)):
            stren1 = '\nDelay st + {0} - TickCount()'.format(lists[each][0])
            if each == 0:
                stren.append(stren1)
            else:
                if lists[each][0] - lists[each - 1][0] > 4:
                    stren.append(stren1)
            if lists[each][3] == 'down':
                stren2 = '\nTouchDownEvent {0},{1}'.format(lists[each][1], lists[each][2])
            else:
                stren2 = '\nTouchUpEvent {0}'.format(lists[each][2])
            stren.append(stren2)
        return stren

    @staticmethod
    def location_deal(fourthdata):           # 编号和具体位置信息统一
        data = {'1': '800,1620', '2': '550,1570', '3': '330,1420', '4': '200,1220',
                     '5': '120,960', '6': '200,700', '7': '330,500', '8': '550,350', '9': '800,300'}
        if fourthdata == 1:
            return data['1']
        elif fourthdata == 2:
            return data['2']
        elif fourthdata == 3:
            return data['3']
        elif fourthdata == 4:
            return data['4']
        elif fourthdata == 5:
            return data['5']
        elif fourthdata == 6:
            return data['6']
        elif fourthdata == 7:
            return data['7']
        elif fourthdata == 8:
            return data['8']
        elif fourthdata == 9:
            return data['9']

    def eachsite(self):
        file = open(self.path, 'r')
        data_list = []
        for oneline in file:                         # 遍历文本中每一个网址
            url = oneline                # print(len(file.readlines()))
            print(url)
            imfor = self.web_driver(url)               # 抓取源码
            result_title = self.re_title(imfor)         # 提取歌曲名
            logging.debug(result_title)
            dress = 'D://JM//{0}.txt'.format(result_title)   # 以歌曲名创建文本  以及存放地址
            print('文件路径 '+dress)
            demo_txt = open(dress, 'w')                          # 打开
            demo_txt.write(self.txt_head())                     # 写入文本前面固定文字
            data = self.re_data(imfor)                             # 提取数据
            # print(data)
            if len(data) == 0:
                print('wrong information about {0}'.format(url))
                continue
            for tuples in data:                                        # 对数据进行处理写入文本
                data_deal = self.data_handel_list(float(tuples[0]), int(tuples[1]), float(tuples[2]), int(tuples[3]))      # 数据处理
                list_down_element = [data_deal[0], data_deal[2], tuples[3], 'down']                 # 数据分开写入
                list_up_element = [data_deal[1], data_deal[2], tuples[3], 'up']
                data_list.append(list_down_element)
                data_list.append(list_up_element)
            # print('chuyi', data_list)
            bubble_lists = self.bubble_sort(data_list)                                                                        # 数据排序
            data_list = []                      # 释放内存
            txt_lists = self.txt_write(bubble_lists)
            for line in txt_lists:
                demo_txt.write(line)
            demo_txt.close()
            input()


spider = Spider()
SourcePage = spider.web_request(spider.web_url)         # 网址采集结束就可以先不用
Number = spider.re_get(SourcePage)
spider.website(Number)
spider.eachsite()
