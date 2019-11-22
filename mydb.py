'''
@Descripttion: some behavior about mysql(database:HUAWEIP30,table:customer)
@version: 1.0
@Author: mopin1
@Date: 2019-11-01 20:35:48
@LastEditTime: 2019-11-22 20:59:23
@Coding: UTF-8
'''

import pymysql

class mydb:
    def __init__(self):
        self.db = pymysql.connect("localhost","root","123456","huaweip30" )
        self.cursor=self.db.cursor()

    def close(self):# 关闭数据库连接
        self.db.close()
    
    '''获取当前数据库行数'''
    def get_count(self):
        sql = "SELECT * FROM CUSTOMER" 
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return len(results)

    '''向数据库插入数据'''
    def insert_data(self,customer_list):

        sql ='INSERT IGNORE INTO CUSTOMER(ID,CONTENT,COLOR,DATE) VALUES ("{}","{}","{}","{}")'.format(customer_list[0],customer_list[1],customer_list[2],customer_list[3])
        self.sql_execute(sql)
    
    '''获取所以数据中的颜色信息'''
    def get_color_data(self):
        color_list=[]
        sql = "SELECT * FROM CUSTOMER" 
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            
            for row in results:
                color_list.append(row[2])
            return color_list
        except:
            print ("Error: unable to fetch data")
    
    '''获取所以文字评论'''
    def get_str_comments(self):
        comments_list=[]
        sql = "SELECT * FROM CUSTOMER" 
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            
            for row in results:
                comments_list.append(row[1])
            return comments_list
        except:
            print ("Error: unable to fetch data")

    '''获取所有完整评论'''
    def get_alldata(self):
        sql = "SELECT * FROM CUSTOMER" 
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            for row in results:
                id = row[0]
                content = row[1]
                color = row[2]
                date = row[3]

                print ("ID:{},CONTENT:{},COLOR:{},DATE:{}".format(id, content, color, date))
        except:
            print ("Error: unable to fetch data")

    '''创建customer表，若已存在则发出warning'''
    def create_table(self,table):
        sql = "CREATE TABLE IF NOT EXISTS "+table +"(ID  CHAR(255),CONTENT  CHAR(255),COLOR CHAR(255),DATE CHAR(255),PRIMARY KEY (ID),UNIQUE KEY (DATE))"
        self.sql_execute(sql)
    
    '''执行sql语句'''
    def sql_execute(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("rollback")
            self.db.rollback()