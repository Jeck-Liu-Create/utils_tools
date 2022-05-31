# -*- encoding: utf-8 -*-
'''
@File    :   five_zt_zy.py
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved.
             Unauthorized copying of this file, via any medium is strictly prohibited
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/13 13:40   LiuDongxing      1.0         None
'''
# import lib
from mysql_tools import Do_Mysql_dict
import datetime

db_name_zt = 'zt_data'
db_name_zy = 'zy_data'

# 按照使用未标记和时间未标记 为条件查到最早一条 可用 ZT id数据 和 金额数据
def zt_db_query():
    q_sql = r"select id,发货日期, from %s where 使用标志 != 1 and 时间标志 !=1  limit 1" % (db_name_zt)
    res_zt = Do_Mysql_dict().query_sql(q_sql)
    return res_zt

# 按照差值不等于0 为条件查到最早一条 ZY id数据 和 差值
def zy_db_query():
    q_sql = r"select id,可用数量,建单日期 from %s where  可用数量 != 0 and 停止标志 != 1    limit 1" % (db_name_zy)
    res_zy = Do_Mysql_dict().query_sql(q_sql)
    return res_zy

# 运单 可用数量 更新
def zy_cha_update(id,sum):
    up_sql = r"UPDATE %s SET 可用数量 = %s WHERE id = %s" % (db_name_zy, sum, id)
    Do_Mysql_dict().update_sql(up_sql)

# 运单 停止标志 更新
def zy_stop_update(id):
    up_sql = r"UPDATE %s SET 停止标志 = %s WHERE id = %s" % (db_name_zy, 1, id)
    Do_Mysql_dict().update_sql(up_sql)


# 运单 差值 , 标志 更新
# def zy_cha_flag_update(id,sum):
#     up_sql = r"UPDATE %s SET 差值 = %s , 标志 = 1 WHERE id = %s" % (db_name_zy, sum, id)
#     Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 使用标志位
# def zt_used_update(id_2,id):
#     up_sql = r"UPDATE %s SET id_2 = %s, 使用标志 = 1  WHERE id = %s" % (db_name_zt, id_2, id)
#     Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 时间标志位
def zt_time_update(id):
    up_sql = r"UPDATE %s SET 时间标志 = 1  WHERE id = %s" % (db_name_zt, id)
    Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 使用标志位
def zt_flag_sum_update(id_2,id):
    up_sql = r"UPDATE %s SET 使用标志 = 1 ,id_2 = %s WHERE id = %s" % (db_name_zt,id_2,id)
    Do_Mysql_dict().update_sql(up_sql)

def main_other():
    # 取 zt 头部数据

    first_data_zt = zt_db_query()
    first_data_zt_id = first_data_zt[0]["id"]
    first_data_zt_date = first_data_zt[0]["发货日期"]
    print("正在处理 zt id: %s" % (first_data_zt_id))

    first_data_zy = zy_db_query()
    first_data_zy_id = first_data_zy[0]["id"]
    first_data_zy_sum = float(first_data_zy[0]["支付金额"])
    first_data_zt_user = float(first_data_zy[0]["可用数量"])
    first_data_zy_date = first_data_zy[0]["建单日期"]


    if int((first_data_zt_date - first_data_zy_date).days) < 15:

        if first_data_zy_sum > 10000:
            if first_data_zy_date <= first_data_zt_date:
                zt_flag_sum_update(first_data_zy_id, first_data_zt_id)
                zy_cha_update(first_data_zy_id, first_data_zt_user - 1)
            else:
                zt_time_update(first_data_zt_id)

        elif 8000 <= first_data_zy_sum <= 10000:
            if first_data_zy_date <= first_data_zt_date:
                zt_flag_sum_update(first_data_zy_id, first_data_zt_id)
                zy_cha_update(first_data_zy_id, first_data_zt_user - 1)
            else:
                zt_time_update(first_data_zt_id)

        elif first_data_zy_sum <= 8000:
            if first_data_zy_date <= first_data_zt_date:
                zt_flag_sum_update(first_data_zy_id, first_data_zt_id)
                zy_cha_update(first_data_zy_id, first_data_zt_user - 1)
            else:
                zt_time_update(first_data_zt_id)

    else:
        zy_stop_update(first_data_zy_id)



if __name__ == '__main__':

    for i in range(1, 1000000):
        print(i)
        main_other()