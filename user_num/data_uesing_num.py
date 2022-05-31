# -*- encoding: utf-8 -*-
'''
@File    :   data_uesing_num.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/29 15:05   LiuDongxing      1.0         None
'''
# 修改运单的可用数量
# import lib
from user_num.mysql_tools import Do_Mysql_dict

db_name_zy = 'zy_19_10'

def zy_db_query(id):
    q_sql = r"select id,支付金额 from %s where id = %s  limit 1" % (db_name_zy,id)
    res_zt = Do_Mysql_dict().query_sql(q_sql)
    return res_zt


def zy_sum_update(id,sum):
    up_sql = r"UPDATE %s SET 可用数量 = %s WHERE id = %s" % (db_name_zy, sum, id)
    Do_Mysql_dict().update_sql(up_sql)

def main_zy(id):
    zy_data = zy_db_query(id)

    first_data_zy_id = zy_data[0]["id"]
    first_data_zy_sum = zy_data[0]["支付金额"]

    if int(first_data_zy_sum) < 5000:
        zy_sum_update(first_data_zy_id,1)
    elif 5000 <= int(first_data_zy_sum) < 8000:
        zy_sum_update(first_data_zy_id, 2)
    elif 8000 <= int(first_data_zy_sum) < 12000:
        zy_sum_update(first_data_zy_id, 3)
    elif 12000 <= int(first_data_zy_sum) :
        zy_sum_update(first_data_zy_id, 4)

if __name__ == '__main__':

    for i in range(1, 1000000):
        print(i)
        main_zy(i)


