# -*- encoding: utf-8 -*-
'''
@File    :   yunda_bangdan_mh.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/10 11:29   LiuDongxing      1.0         None
'''

# import lib
from mysql_tools import Do_Mysql_dict
import multiprocessing.dummy as mp

def user_tools_db_query(id,db_name):
    q_sql = r"select * from '%s' where id='%s'" % (db_name,str(id))
    res_q = Do_Mysql_dict().query_sql(q_sql)
    print(res_q)

def db_name_unit(id,db_name):
    q_sql = r"select 车辆编号,出厂日期,净重 from %s where id=%s limit 1" % (db_name, str(id))
    res_q = Do_Mysql_dict().query_sql(q_sql)
    return res_q

def batch(name):
    sql_id_nm = "select id from %s order by id desc limit 1" % str(name)
    id_nm_dict = Do_Mysql_dict().query_sql(sql_id_nm)
    print(id_nm_dict[0]['id'])
    return int(id_nm_dict[0]['id'])

def select_db(id):
    db_name_one = '2021bangdan'
    db_name_two = '2021yundan'
    dict_db = db_name_unit(id,db_name_one)
    id_sql = r"select id from %s where 原发车号 = '%s' and 皮重日期 = '%s' and 计费数量（吨）= '%s' limit 1" % (db_name_two,str(dict_db[0]['车辆编号']),str(dict_db[0]['出厂日期']),str(dict_db[0]['净重']))
    print(id_sql)
    try:
        id_sql_df = Do_Mysql_dict().query_sql(id_sql)
        return id_sql_df,True
    except:
        return None,False

def main_user():
    for i in range(1,batch('2021yundan')):
       one ,two = select_db(i)
       if two:
           print(one)

def user_set(i):
    one, two = select_db(i)
    if two:
        print(one)

# 匹配总量大于一的后处理情况
def mix_only_all(id,id_list):
    list_data = []
    db_name = '2021yundan'
    determine = 'test'
    id_query = r"select `%s` from %s where id = `%s` limit 1" % (determine,db_name,str(id))
    id_sql_df = Do_Mysql_dict().query_sql(id_query)
    id_sql_df = id_sql_df[0][str(determine)]
    for i in id_list:
        db_name_other = '2021bangdan'
        determine_other = "test"
        print(i['id'])
        id_query_list = r"select `%s` from %s where id =`%s` limit 1" % (determine_other,db_name_other,str(i['id']))
        list_data.append([int(id_sql_df) - int(id_query_list), i['id'],])

    for x in range(len(list_data)):
        for j in range(0, len(list_data) - x - 1):
            if list_data[j][0] > list_data[j + 1][0]:
                temp = list_data[j]
                list_data[j] = list_data[j + 1]
                list_data[j + 1] = temp

    print(list_data)

    id_other = list_data[0][1]




# 部分相同近似匹配其他数据
def select_db_mix(id):
    db_name_one = '2021bangdan'
    db_name_two = '2021yundan'
    dict_db = db_name_unit(id,db_name_one)
    id_sql = r"select id from %s where 原发车号 = '%s' and 皮重日期 = '%s' and 计费数量（吨）= '%s' limit 1" % (db_name_two,str(dict_db[0]['车辆编号']),str(dict_db[0]['出厂日期']),str(dict_db[0]['净重']))
    print(id_sql)

    try:
        id_sql_df = Do_Mysql_dict().query_sql(id_sql)
        if len(dict_db) > 1 :
            return id_sql_df,True
    except:
        return None,False


if __name__ == '__main__':

    list_data = []
    for i in range(1,10):
        print(i)
        one ,two = select_db(i)
        if two:
            if str(one) != '()':
                list_data.append(one[0]['id'])


    print(list_data)


