from selenium import webdriver

#打开浏览器
brower = webdriver.Chrome("D:/chromedriver/chromedriver.exe")
url='https://music.163.com/#/discover/toplist'
brower.get(url)

#寻找logo文字
#logo = brower.find_elements_by_class_name('logo')[0]
#print(logo.text)


#一般情况下动态加载的内容都可以找到

#有一种情况就没有
#就是网页内存在网页框架iframe
#需要切换网页的层级
#语法：brower.switch_to.frame(iframe的id或者你提前获取这个对象，放入此处）

#方法一：id
#brower.switch_to.frame('g_iframe')
#方法二：name
#brower.switch_to.frame('contentFrame')
#方法三：提前用变量存iframe
iframe = brower.find_element_by_id('g_iframe')
brower.switch_to.frame(iframe)

#寻找大容器
toplist = brower.find_element_by_id('toplist')
#寻找tbody 通过标签名
tbody = toplist.find_elements_by_tag_name('tbody')[0]
#寻找所有tr
trs = tbody.find_elements_by_tag_name('tr')


dataList = []
for each in trs:
    #排名
    rank = each.find_elements_by_tag_name('td')[0].find_elements_by_class_name('num')[0].text
    musicName = each.find_elements_by_tag_name('td')[1].find_elements_by_class_name('txt')[0].\
        find_element_by_tag_name('b').get_attribute('title')
    #print(musicName)
    singer = each.find_elements_by_tag_name('td')[3].find_elements_by_class_name('text')[0].\
        get_attribute('title')
    #print(singer)
    dataList.append([rank,musicName,singer])
#print(dataList)
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = '云音乐飙升榜'
ws.append(['排名','歌名','歌手'])
for data in dataList:
    ws.append(data)

wb.save("云音乐飙升榜.xlsx")