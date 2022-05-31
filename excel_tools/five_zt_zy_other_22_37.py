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

'''
@方案1

    if  磅单金额 - 运单金额 < -3000 时:
        设置时 运单更新为( 运单金额 - 磅单金额 );
        磅单金额不变，标记已处理，匹配运单 id;

  elif  -3000 <= 磅单金额 - 运单金额 <= -1500 时:
        磅单金额不变，标记已经处理，匹配运单 id;
        下一条磅单金额直接修改为( 运单金额 - 磅单金额 )，并且标记已经处理;

  elif  磅单金额 - 运单金额  > -1500 时:
        磅单金额直接改为运单剩余金额，标记已经处理，匹配运单 id;
'''

# import lib
from mysql_tools_2 import Do_Mysql_dict
import datetime

db_name_zt = 'zt_coul'
db_name_zy = 'zy_coul'

# 按照使用未标记和时间未标记 为条件查到最早一条 可用 ZT id数据 和 金额数据
def zt_db_query():
    q_sql = r"select id,金额,发货日期 from %s where 使用标志 != 1 and 时间标志 !=1  limit 1" % (db_name_zt)
    res_zt = Do_Mysql_dict().query_sql(q_sql)
    return res_zt

# 按照差值不等于0 为条件查到最早一条 ZY id数据 和 差值
def zy_db_query():
    q_sql = r"select id,差值,建单日期,标志 from %s where  差值 != 0   limit 1" % (db_name_zy)
    res_zy = Do_Mysql_dict().query_sql(q_sql)
    return res_zy

# 运单 差值 更新
def zy_cha_update(id,sum):
    up_sql = r"UPDATE %s SET 差值 = %s WHERE id = %s" % (db_name_zy, sum, id)
    Do_Mysql_dict().update_sql(up_sql)

# 运单 差值 , 标志 更新
def zy_cha_flag_update(id,sum):
    up_sql = r"UPDATE %s SET 差值 = %s , 标志 = 1 WHERE id = %s" % (db_name_zy, sum, id)
    Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 使用标志位
def zt_used_update(id_2,id):
    up_sql = r"UPDATE %s SET id_2 = %s, 使用标志 = 1  WHERE id = %s" % (db_name_zt, id_2, id)
    Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 时间标志位
def zt_time_update(id):
    up_sql = r"UPDATE %s SET 时间标志 = 1  WHERE id = %s" % (db_name_zt, id)
    Do_Mysql_dict().update_sql(up_sql)

# ZT 匹配 id 修改 使用标志位,金额
def zt_flag_sum_update(id_2,sum,id):
    up_sql = r"UPDATE %s SET 使用标志 = 1 , 金额 = %s ,id_2 = %s WHERE id = %s" % (db_name_zt,sum,id_2,id)
    Do_Mysql_dict().update_sql(up_sql)


def main_other():
    # 取 zt 头部数据

    first_data_zt = zt_db_query()
    first_data_zt_id = first_data_zt[0]["id"]
    first_data_zt_sum = float(first_data_zt[0]["金额"])
    first_data_zt_date = first_data_zt[0]["发货日期"]
    print("正在处理 zt id: %s" % (first_data_zt_id))

    first_data_zy = zy_db_query()
    first_data_zy_id = first_data_zy[0]["id"]
    first_data_zy_sum = float(first_data_zy[0]["差值"])
    first_data_zy_date = first_data_zy[0]["建单日期"]
    first_data_zy_Flag = first_data_zy[0]["标志"]


    # 判断 建单日期 是否 小于 发货日期
    # 如果满足则进行之后判断
    # 如果不满足 则直接修改最首部 zt 的 时间标志 , 后递归
    if first_data_zy_date <= first_data_zt_date:

        # 判断 运单标志是否不为1
        # 若果不为1则进入
        # 若果为1则修改当前zt 修改使用标记  金额 为 运单金额 同时修改运单差值为 0
        if int(first_data_zy_Flag) != 1 :
            value_data = first_data_zt_sum - first_data_zy_sum
            if value_data < -3700:
                print(" 磅单金额 - 运单金额 < -3700 时 ")
                zy_cha_update(first_data_zy_id,(first_data_zy_sum-first_data_zt_sum))
                zt_used_update(first_data_zy_id,first_data_zt_id)
            elif -3700 <= value_data <= -2200:
                print(" -3700 <= 磅单金额 - 运单金额 <= -2200 时 ")
                zt_used_update(first_data_zy_id, first_data_zt_id)
                zy_cha_flag_update(first_data_zy_id,(first_data_zy_sum-first_data_zt_sum))
            elif value_data > -2200:
                print(" 磅单金额 - 运单金额  < -2200 时 ")
                zt_flag_sum_update(first_data_zy_id, first_data_zy_sum, first_data_zt_id)
                zy_cha_update(first_data_zy_id, 0)
        else:
            zt_flag_sum_update(first_data_zy_id,first_data_zy_sum,first_data_zt_id)
            zy_cha_update(first_data_zy_id, 0)
    else:
        zt_time_update(first_data_zt_id)



if __name__ == '__main__':

    for i in range(1, 1000000):
        print(i)
        main_other()