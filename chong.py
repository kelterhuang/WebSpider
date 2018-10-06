import requests
import re                                      # 正则表达式
import os 
# import bs4
from bs4 import BeautifulSoup

# %%   Get请求 获得网页HTML内容
'''
r = requests.get('https://unsplash.com')
print(r.text)
print(type(r))   #<class 'requests.models.Response'> 
'''


# %%   Get带参数
# 下面代码向服务器发送的请求中包含了两个参数key1和key2，以及两个参数的值。实际上它构造成了如下网址：
# http://httpbin.org/get?key1=value1&key2=value2
'''
payload = {'key1': 'value1','key2': 'value2'}
r =  requests.get("http://httpbin.org/get",params = payload)
'''

# %%   Post请求
'''
#无参数的Post请求
r = requests.post('http://httpbin.org/post')
#有参数的Post请求
payload = {'key1': 'value1','key2': 'value2'}
r = requests.post('http://httpbin.org/post', data = payload)
'''

# %%   其他请求
'''
r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")
'''

# %% 从HTML中获得图片-->BeautifulSoup库

# %% Tag
'''
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
soup = BeautifulSoup(html_doc, 'lxml')                     #声明BeautifulSoup对象
find = soup.find('p')                                                    #使用find方法查到第一个p标签
print("find's return type is ", type(find))                    #输出返回值类型
print("find's content is", find)                                    #输出find获取的值
print("find's Tag Name is ", find.name)                     #输出标签的名字
print("find's Attribute(class) is ", find['class'])          #输出标签的class属性值
print('NavigableString is：', find.string)
'''

# %%  comment 注释
'''
markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup)
comment = soup.b.string
type(comment)
print(type(comment))  # <class 'bs4.element.Comment'>
if type(comment) == bs4.element.Comment:
    print('该字符是注释')
else:
    print('该字符不是注释')
'''

# %% ,class_='img-box'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}  #模拟chrome浏览器
path = 'c:\\users\\16904\\Desktop\\pictures'


def file():
    folder = os.path.exists(path)
    if not folder:                   # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            # makedirs 创建文件时如果路径不存在会创建这个路径
        print ("---  new folder...  ---")
        print ("---  OK  ---")
    else:
        print ("---  There is this folder!  ---")


def geturl():
    web_url = 'https://unsplash.com/'
    r = requests.get(web_url, headers=headers)                                          # 像目标url地址发送get请求，返回一个response对象
    soup = BeautifulSoup(r.text, 'lxml').find_all('img', class_='_2zEKz')   # 共有68张图片 soup是list
    name = 0
    for go in soup:
        url = go['srcset']
        study = re.search('.*q=60\s2400w.(.*)q=60\s2592w',url,re.M)
        if study:
            suc = study.group(1)
            print(suc)
        else:
            print('no')
        pictures = requests.get(suc, headers=headers)
        file_name = str(name)+'.jpg'
        path2 = os.path.join(path,file_name)
        f = open(path2, 'ab')
        f.write(pictures.content)
        name = name + 1


file()
geturl()

'''
for a in soup:
    print(a['srcset'])
soup = str(soup)
print(soup)
study = re.findall('https.*q=60\s2400w.\s(.*)',soup,re.S)
print (study)

print(study)
i=0
for all in study :
    print(all,i)
    i=i+1
result =  re.findall('https.*q=60\s2400w.(.*)q=60\s2592w',soup,re.S)
print (str(result))
'''


# %%
'''res = requests.get('http://pic.sogou.com/pics/recommend?category=%B1%DA%D6%BD')
soup = BeautifulSoup(res.text,'html.parser')
print(soup.select('img'))

def getSogouImag(category,length,path):
    n = length
    cate = category
    imgs = requests.get('http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category='+cate+'&tag=%E5%85%A8%E9%83%A8&start=0&len='+str(n))
    jd = json.loads(imgs.text)
    jd = jd['all_items']
    imgs_url = []
    for j in jd:
        imgs_url.append(j['bthumbUrl'])
    m = 0
    for img_url in imgs_url:
            print('***** '+str(m)+'.jpg *****'+'   Downloading...')
            urllib.request.urlretrieve(img_url,path+str(m)+'.jpg')
            m = m + 1
    print('Download complete!')

getSogouImag('壁纸',2000,'d:/download/壁纸/')
'''
# %%
"""
data = '''
    <div>
    <span class='a' protype='d'>1</span>
    <span class='a' protype='d'>2</span>
    <span class='a' protype='d'>3</span>
    <span class='a' protype='d'>4</span>
    </div>
'''
soup = BeautifulSoup(data, 'lxml')
spans = soup.find_all('span')
print(spans)                                                  #可以读取所有的标签<span
span_content=[]
for i in spans:
    print(i)                                        #这里取标签span的内容
    span_content.append(i.text)
print(span_content)
"""
'''
<span class="a" protype="d">1</span> 1
<span class="a" protype="d">2</span> 2
<span class="a" protype="d">3</span> 3
<span class="a" protype="d">4</span> 4
[u'1', u'2', u'3', u'4']

path = 'c:\\users\\16904\\Desktop\\pictures'
folder = os.path.exists(path)
if not folder:                   # 判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs(path)            # makedirs 创建文件时如果路径不存在会创建这个路径
    print ("---  new folder...  ---")
    print ("---  OK  ---")
else:
    print ("---  There is this folder!  ---")
'''