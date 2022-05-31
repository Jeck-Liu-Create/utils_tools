# -*- encoding: utf-8 -*-
'''
@File    :   mysql_tools.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/10 11:36   LiuDongxing      1.0         None
'''
import pymysql

class Do_Mysql_dict:
    def __init__(self):
        # 连接数据库
        self.conn=pymysql.connect(
                             host='127.0.0.1',
                             user="other",
                             password="123456",
                             database="p_2022_05_14_2",
                             port=3306,
                             charset="utf8",cursorclass = pymysql.cursors.DictCursor)
        self.cursor=self.conn.cursor() #创建游标

    def query_sql(self,sql,state="all"):
        #编写sql语句
        # query_sql='select * from ftes.user where user_name="lyc4"'
        res=self.cursor.execute(sql)       #执行sql语句
        # data=self.conn.commit()          #增删改要用到conmit  查询不用
        #获取查询的结果 fetchone查询一条结果 fetchall查询多条结果 fetchmany查询指定条数
        if state==1:
            res=self.cursor.fetchone()
        else:
            res=self.cursor.fetchall()

        self.cursor.close() #关闭游标
        self.conn.close() #关闭数据库
        return res

    def del_sql(self,sql):
        # 编写del_sql语句
        # del_sql='delete from ftes.user where user_id=48'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit() #增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

    def insert_sql(self,sql):
        # 编写del_sql语句
        # insert_sql='insert into ftes.net_bar values(net_bar_id=8,net_bar_name="ldd")'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

    def update_sql(self,sql):
        # 编写del_sql语句
        # insert_sql='insert into ftes.net_bar values(net_bar_id=8,net_bar_name="ldd")'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

class Do_Mysql:
    def __init__(self):
        # 连接数据库
        self.conn=pymysql.connect(host="127.0.0.1",
                             user="other",
                             password="123456",
                             database="p_2022_05_14_2",
                             port=3306,
                             charset="utf8")
        self.cursor=self.conn.cursor() #创建游标

    def query_sql(self,sql,state="all"):
        #编写sql语句
        # query_sql='select * from ftes.user where user_name="lyc4"'
        res=self.cursor.execute(sql)       #执行sql语句
        # data=self.conn.commit()          #增删改要用到conmit  查询不用
        #获取查询的结果 fetchone查询一条结果 fetchall查询多条结果 fetchmany查询指定条数
        if state==1:
            res=self.cursor.fetchone()
        else:
            res=self.cursor.fetchall()

        self.cursor.close() #关闭游标
        self.conn.close() #关闭数据库
        return res

    def del_sql(self,sql):
        # 编写del_sql语句
        # del_sql='delete from ftes.user where user_id=48'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit() #增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

    def insert_sql(self,sql):
        # 编写del_sql语句
        # insert_sql='insert into ftes.net_bar values(net_bar_id=8,net_bar_name="ldd")'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

    def update_sql(self,sql):
        # 编写del_sql语句
        # insert_sql='insert into ftes.net_bar values(net_bar_id=8,net_bar_name="ldd")'
        res = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 增删改要用到conmit  查询不用
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库

if __name__ == '__main__':

    q_sql = 'select * from zt_data where id=1'
    res_q = Do_Mysql().query_sql(q_sql)
    print(res_q)

