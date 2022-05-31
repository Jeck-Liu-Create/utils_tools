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

db_name_zt = 'zt_coul'
db_name_zy = 'zy_coul'

# 按照使用未标记和时间未标记 为条件查到最早一条 可用 ZT id数据 和 金额数据
def zt_db_query():
    q_sql = r"select id,发货日期 from %s where 使用标志 != 1 and 时间标志 !=1  limit 1" % (db_name_zt)
    res_zt = Do_Mysql_dict().query_sql(q_sql)
    return res_zt

# 按照差值不等于0 为条件查到最早一条 ZY id数据 和 差值
def zy_db_query():
    q_sql = r"select id,建单日期  from %s where  标志 != 1 limit 1" % (db_name_zy)
    res_zy = Do_Mysql_dict().query_sql(q_sql)
    return res_zy

# 修改运单标志
def zy_flag_updata(id):
    id_update = r"UPDATE %s SET 标志 = '%s' WHERE id = %s" % (db_name_zy ,1 , id)
    Do_Mysql_dict().update_sql(id_update)

# 磅单修改时间标志
def zt_time_update(id):
    up_sql = r"UPDATE %s SET 时间标志 = 1  WHERE id = %s" % (db_name_zt, id)
    Do_Mysql_dict().update_sql(up_sql)

# 修改运单的 id_3 = 磅单的 id , 同时设置标志为1
def zy_flag_updata(id_3,id):
    up_sql = r"UPDATE %s SET 标志 = 1 ,id_3 = '%s' WHERE id = '%s'" % (db_name_zy, id_3,id)
    Do_Mysql_dict().update_sql(up_sql)

# 磅单 id_2 = 运单 id , 同时设置使用标志位1
def zt_flag_updata(id_2,id):
    up_sql = r"UPDATE %s SET 使用标志 = 1 ,id_2 = '%s' WHERE id = '%s'" % (db_name_zt, id_2,id)
    Do_Mysql_dict().update_sql(up_sql)


def main_other():
    first_data_zt = zt_db_query()
    first_data_zt_id = first_data_zt[0]['id']
    first_data_zt_date = first_data_zt[0]['发货日期']

    first_data_zy = zy_db_query()
    first_data_zy_id = first_data_zy[0]["id"]
    first_data_zy_date = first_data_zy[0]["建单日期"]

    print( r" zy id 号: %s" % str(first_data_zy_id) )

    # 判断 建单日期 是否 小于 发货日期
    # 如果满足则进行直接赋值
    # 如果不满足 则直接修改最首部 zt 的 时间标志 , 后递归
    if first_data_zy_date <= first_data_zt_date:
        # 修改运单的 id_3 = 磅单的 id , 同时设置标志为1
        zy_flag_updata(first_data_zt_id,first_data_zy_id)
        # 磅单 id_2 = 运单 id , 同时设置使用标志位1
        zt_flag_updata(first_data_zy_id,first_data_zt_id)
    else:
        zt_time_update(first_data_zt_id)



if __name__ == '__main__':

    for i in range(1, 1000000):
        print(i)
        main_other()