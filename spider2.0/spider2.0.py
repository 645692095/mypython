'''
@Descripttion: A spider about HUAWEIP30 from jd
@version: 2.0
@Author: mopin1
@Date: 2019-11-10 21:56:52
@LastEditTime: 2019-11-22 20:57:15
@Coding: UTF-8
'''

import requests
from requests.exceptions import RequestException
import winreg
import json
from time import sleep
from pyecharts.charts import Pie
from pyecharts import options as opts
from apscheduler.schedulers.blocking import BlockingScheduler

'''自定义的.py文件'''
from mydb import mydb
from mydict import mydict
from myException import Already_exists


def set_time_to_start():
    main(page=100)

def get_page(url, headers):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
                index=response.text.index("{")
                return json.loads(response.text[index:-2])
        # print(response.status_code)
        return None
    except RequestException:#异常处理
        print('error')
        return None

def get_desktop():#获取桌面路径
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

desktop=get_desktop()#获取桌面路径，desktop为str类型

def draw_color(list1,list2):
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
    pie.render(desktop+"\\jd.huaweiP30.colors.html")
    return True

headers = {
    'Accept': '*/*',#应对反爬机制
    'Sec-Fetch-Mode': 'no-cors',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Referer':"https://item.jd.com/100002795955.html"
	}

def main(pages):
    mydb_beau=mydb()
    mydict_beau=mydict()
    mydb_beau.create_table('customer')
    row_count=mydb_beau.get_count()
    try:
        for i in range(pages):
            if i==0:
                url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3436&productId=100002795955&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            else:
                url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3423&productId=100002795955&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(i)

            r_dict = get_page(url,headers=headers)
            
            for element in r_dict['comments']:
                customer_list=[element['id'],element['content'].replace(" ","").replace("\n","").replace('"',"'")[0:255],element['productColor'],element['creationTime']]
                mydb_beau.insert_data(customer_list)

                if row_count==mydb_beau.get_count():
                    raise Already_exists()
                else:
                    row_count=mydb_beau.get_count()
                    
            if i>=10 and i%10==0:#每十页休息30s
                sleep(30)
    except Already_exists:
        pass

    if i==pages-1:
        print('数据收集完成！')
    else:
        print('数据更新完成！')
    list_kinds=['天空之境','亮黑色','极光色','赤茶橘','珠光贝母']
    color_list=mydb_beau.get_color_data()
    list_numbers=[color_list.count('天空之境'),color_list.count('亮黑色'),color_list.count('极光色'),color_list.count('赤茶橘'),color_list.count('珠光贝母')]
    
    for comment in mydb_beau.get_str_comments():
        mydict_beau.add_into_comment_dictionary(mydict_beau.divide_commint(comment))
    if(mydict_beau.draw_dictionary(mydict_beau.sort_dictionary())):
        print("高频词词云已经绘好！")

    mydb_beau.close()

    if(draw_color(list_kinds,list_numbers)):     
        print('颜色饼状图已经更新！')

if __name__=='__main__':
    main(pages=100)#首次执行

    scheduler = BlockingScheduler()
    '''采用固定时间间隔（interval）的方式，每隔1天执行一次'''
    scheduler.add_job(set_time_to_start, 'interval', days=1)

    scheduler.start()
