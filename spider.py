'''
@Description: A spider about HUAWEIP30 in jd.com
@Version: 1.0
@Author: mopin1
@Date: 2019-11-22 12:10:46
@LastEditTime: 2019-11-22 12:40:52
'''
import winreg
import requests
from requests.exceptions import RequestException
from time import sleep
import json
from pyecharts.charts import Pie
from pyecharts import options as opts

def get_desktop():#获取桌面路径
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

desktop=get_desktop()#desktop为str类型

def get_page(url, headers):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        print(response.status_code)
        return None
    except RequestException:#异常处理
        print('Error!')
        return None

def write_to_file(content):
    fp=open(desktop+'\\jd.huaweiP30.json','w',encoding='utf-8')
    print(content[26:-2],file=fp)#字符串写入文件
    fp.close()

def read_from_file():
    fp=open(desktop+'\\jd.huaweiP30.json',"r",encoding='utf-8')
    contents=json.load(fp)#读出文件，content为dict类型
    fp.close()
    return contents

def draw(list1,list2):
    pie = Pie()
    pie.add("",list(zip(list1,list2)))
    pie.set_global_opts(
                title_opts=opts.TitleOpts(title="消费者购买的HUAWEIP30颜色图例"),#标题
                legend_opts=opts.LegendOpts(
                    orient="vertical", pos_top="15%", pos_left="4%"
                ),
            )
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))#图例显示（颜色+人数），例：亮黑色：46
    pie.set_colors(["lightblue", "black", "turquoise", "orangered", "lightpink"])
    pie.render(desktop+"\\jd.huaweiP30.html")
    return 1

def main(i):
    
    global sky_color,black_color,aurora_color,red_color,pearl_color

    if i==0:
        url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3436&productId=100002795955&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    else:
        url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3423&productId=100002795955&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(i)
    headers = {
        'Accept': '*/*',#应对反爬机制
        # 'Sec-Fetch-Mode': 'no-cors',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Referer':"https://item.jd.com/100002795955.html"
        }

    r = get_page(url,headers=headers)

    write_to_file(r)
    contents=read_from_file()
    
    for element in contents['comments']:
        #print(element['productColor'])
        if element['productColor']=='天空之境':
            sky_color+=1
        elif element['productColor']=='亮黑色':
            black_color+=1
        elif element['productColor']=='极光色':
            aurora_color+=1
        elif element['productColor']=='赤茶橘':
            red_color+=1
        elif element['productColor']=='珠光贝母':
            pearl_color+=1
    print("第{}页完成！".format(i+1))

    if i==49:
        sleep(60)#获取第50页数据后，挂起60s

    if i==99:
        list1=['天空之境','亮黑色','极光色','赤茶橘','珠光贝母']
        list2=[sky_color,black_color,aurora_color,red_color,pearl_color]
        print('数据收集完成！')

        if(draw(list1,list2)==1):      #绘图
            print('饼状图已经绘好！')

if __name__=='__main__':

    global sky_color,black_color,aurora_color,red_color,pearl_color

    sky_color=0#天空之境
    black_color=0#亮黑色
    aurora_color=0#极光色
    red_color=0#赤茶橘
    pearl_color=0#珠光贝母
    
    pages=100
    for i in range(pages):#爬取100页
        main(i)

