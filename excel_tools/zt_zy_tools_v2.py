# -*- encoding: utf-8 -*-
'''
@File    :   zt_zy_tools.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/11 21:14   LiuDongxing      1.0         None
'''

# import lib
from mysql_tools import Do_Mysql_dict
import datetime

# global id_yun
db_name_one = 'zt_new'
db_name_two = 'zy_new'
id_default = 0


def db_name_unit(id,db_name):
    q_sql = r"select `金额` from %s where id=%s limit 1" % (db_name, str(id))
    res_q = Do_Mysql_dict().query_sql(q_sql)
    return res_q


def select_db(id):
    id_yun = id
    # 全局变量
    global id_default,db_name_two,db_name_one

    # sum_dan = db_name_unit(id, db_name_one)
    id_sql = r"select `差值` from %s where id= %s limit 1" % \
             (db_name_two,id_yun)
    sum_yun = Do_Mysql_dict().query_sql(id_sql)

    if float(sum_yun[0]['差值']) != 0:
    # 按照顺序查找未被使用的 zt_dan
        id_sql_one = r"SELECT id,`实际付款金额` FROM %s WHERE  id > '%s' and `标志` !=1 LIMIT 1" % (db_name_one,id_default)
        # print(id_sql_one)
        zt_one = Do_Mysql_dict().query_sql(id_sql_one)
        dan_one_id = zt_one[0]['id']
        dan_one_sum = zt_one[0]['实际付款金额']
        value_one = float(sum_yun[0]['差值'])-float(dan_one_sum)

        # zt_dan 倒扣
        if value_one == 0:
            # zt_dan 更新
            dan_update_two = r"UPDATE %s SET 标志 = '%s' , id_2 = '%s' , `实际付款金额` = '%s' WHERE id = '%s'" % (
                db_name_one, 1, id_yun, str(sum_yun[0]['差值']), dan_one_id)
            Do_Mysql_dict().update_sql(dan_update_two)
            # zy_yun 更新
            yun_update_three = r"UPDATE %s SET 差值 = '%s' WHERE id = '%s'" % (db_name_two, 0, id_yun)
            Do_Mysql_dict().update_sql(yun_update_three)

        elif 0 < value_one <= 1000 or value_one < 0:
            # zt_dan 更新
            dan_update_two = r"UPDATE %s SET 标志 = '%s' , id_2 = '%s' , `实际付款金额` = '%s' WHERE id = '%s'" % (
                db_name_one, 1, id_yun, str(sum_yun[0]['差值']), dan_one_id)
            Do_Mysql_dict().update_sql(dan_update_two)
            # zy_yun 更新
            yun_update_three = r"UPDATE %s SET 差值 = '%s' WHERE id = '%s'" % (db_name_two, 0, id_yun)
            Do_Mysql_dict().update_sql(yun_update_three)

        elif value_one > 1000:
            # zt_dan 更新
            dan_update_one = r"UPDATE %s SET 标志 = '%s' , id_2 = '%s' WHERE id = '%s'" % (db_name_one,1,id_yun,dan_one_id)
            # print(dan_update_one)
            Do_Mysql_dict().update_sql(dan_update_one)
            # zy_yun 更新
            yun_update_two = r"UPDATE %s SET 差值 = '%s' WHERE id = '%s'" % (db_name_two,value_one,id_yun)
            Do_Mysql_dict().update_sql(yun_update_two)

        # elif value_one < 0:
        #     dan_update_two = r"UPDATE %s SET 标志 = '%s' , id_2 = '%s' , `实际付款金额` = '%s' WHERE id = '%s'" % (
        #         db_name_one, 1, id_yun, str(sum_yun[0]['差值']), dan_one_id)
        #     Do_Mysql_dict().update_sql(dan_update_two)
        #     # zy_yun 更新
        #     yun_update_three = r"UPDATE %s SET 差值 = '%s' WHERE id = '%s'" % (db_name_two, 0, id_yun)
        #     Do_Mysql_dict().update_sql(yun_update_three)



        id_default = dan_one_id

        id_sql_other = r"select `差值` from %s where id= %s limit 1" % \
                 (db_name_two, id_yun)
        Do_Mysql_dict().query_sql(id_sql_other)
        if float(sum_yun[0]['差值']) != 0:
            select_db(id_yun)


        # if float(sum_yun[0]['差值']) <= 1000:
        #     id_sql_two = r"SELECT id,`实际付款金额` FROM %s WHERE  id > '%s' and `标志` !=1 LIMIT 1" % (db_name_one, id_default)
        #     zt_two = Do_Mysql_dict().query_sql(id_sql_two)
        #     dan_two_id = zt_two[0]['id']
        #     # zt_dan 更新
        #     dan_update_two = r"UPDATE %s SET 标志 = '%s' , id_2 = '%s' , `实际付款金额` = '%s' WHERE id = '%s'" % (
        #     db_name_one, 1, id_yun, str(sum_yun[0]['差值']), dan_two_id)
        #     Do_Mysql_dict().update_sql(dan_update_two)
        #     # zy_yun 更新
        #     yun_update_three = r"UPDATE %s SET 差值 = '%s' WHERE id = '%s'" % (db_name_two, 0, id_yun)
        #     Do_Mysql_dict().update_sql(yun_update_three)


if __name__ == '__main__':
    for i in range(1,2614):
        print(i)
        select_db(i)









