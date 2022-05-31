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

db_name_zt = 'zt_coul_2'
db_name_zy = 'zy_coul_2'

# 按照使用未标记和时间未标记 为条件查到最早一条 可用 ZT id数据 和 金额数据
def zt_db_query():
    q_sql = r"select id,发货日期 from %s where 使用标志 != 1 and 时间标志 !=1  limit 1" % (db_name_zt)
    res_zt = Do_Mysql_dict().query_sql(q_sql)
    return res_zt

# 按照差值不等于0 为条件查到最早一条 ZY id数据 和 差值
def zy_db_query():
    q_sql = r"select id,建单日期,车牌号  from zy_coul_2 where  zy_coul_2.标志 != 1 limit 1"
    res_zy = Do_Mysql_dict().query_sql(q_sql)
    return res_zy

# 查询符合要求的运单
def zt_db_zy_query(data_one,car_num):
    # q_sql = r"SELECT id,车牌号码 FROM %s WHERE  发货日期 > %s and 发货日期 < %s and 车牌号码 = %s and 使用标志 != 1 LIMIT 1 ;" \
    #         % (db_name_zt,str(data_one + datetime.timedelta(-1)) ,str(data_one + datetime.timedelta(31)),car_num)
    q_sql = r"SELECT * FROM (SELECT * FROM zt_coul_2 WHERE zt_coul_2.`发货日期` >= '%s' and  zt_coul_2.`发货日期` <= '%s' and zt_coul_2.使用标志 !=1 ) AS zuzu WHERE zuzu.`车牌号码` = '%s' ;"  % (data_one, data_one + datetime.timedelta(30),car_num)

    print(q_sql)

    res_zy = Do_Mysql_dict().query_sql(q_sql)
    return res_zy


# 修改运单标志
def zy_flag_updata(id):
    id_update = r"UPDATE zy_coul_2 SET 标志 = 1 WHERE id = '%s'" % (id)
    Do_Mysql_dict().update_sql(id_update)

# 设置运单 id_3
def zy_id_3_updata(id,id_3):
    id_update = r"UPDATE %s SET id_3 = %s WHERE id = '%s'" % (db_name_zy,id_3, id)
    Do_Mysql_dict().update_sql(id_update)

# 修改磅单使用标志
def zt_flag_updata(id_2,id):
    id_update = r"UPDATE zt_coul_2 SET zt_coul_2.使用标志 = 1 ,zt_coul_2.id_2 = '%s' WHERE id = '%s'" % ( id_2, id)
    Do_Mysql_dict().update_sql(id_update)


def main_other():
    first_data_zy = zy_db_query()
    first_data_zy_id = first_data_zy[0]["id"]
    first_data_zy_car = first_data_zy[0]["车牌号"]
    first_data_zy_date = first_data_zy[0]["建单日期"]

    print( r" zy id 号: %s" % str(first_data_zy_id) )

    first_data_zt = zt_db_zy_query(first_data_zy_date, first_data_zy_car)
    print(first_data_zt)

    if str(first_data_zt) == '()':
        zy_flag_updata(first_data_zy_id)
    else:
        first_data_zt_id = first_data_zt[0]["id"]
        zy_id_3_updata(first_data_zy_id,first_data_zt_id)
        zt_flag_updata(first_data_zy_id,first_data_zt_id)
        zy_flag_updata(first_data_zy_id)


if __name__ == '__main__':

    for i in range(1, 1000000):
        print(i)
        main_other()