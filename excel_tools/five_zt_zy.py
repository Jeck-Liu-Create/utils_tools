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
        设置 运单更新为( 运单金额 - 磅单金额 );
        磅单金额不变，标记已处理，匹配运单 id;

  elif  -3000 <= 磅单金额 - 运单金额 <= -1500 时:
        磅单金额不变，标记已经处理，匹配运单 id;
        下一条磅单金额直接修改为( 运单金额 - 磅单金额 )，并且标记已经处理;

  elif  磅单金额 - 运单金额  > -1500 时:
        磅单金额直接改为运单剩余金额，标记已经处理，匹配运单 id;
 
'''


# import lib
from mysql_tools import Do_Mysql_dict
import datetime

def user_tools_db_query(id,db_name):
    q_sql = r"select * from %s where id='%s'" % (db_name,str(id))
    res_q = Do_Mysql_dict().query_sql(q_sql)
    print(res_q)

def db_name_unit(id,db_name):
    q_sql = r"select `皮重日期` from %s where id=%s limit 1" % (db_name, str(id))
    res_q = Do_Mysql_dict().query_sql(q_sql)
    return res_q

def batch(name):
    sql_id_nm = "select id from %s order by id desc limit 1" % str(name)
    id_nm_dict = Do_Mysql_dict().query_sql(sql_id_nm)
    print(id_nm_dict[0]['id'])
    return int(id_nm_dict[0]['id'])

def select_db(id):
    db_name_one = 'zt_3'
    db_name_two = 'zy_3'
    dict_db = db_name_unit(id,db_name_one)
    id_sql = r"select id from %s where '%s' < 支付时间1 and 支付时间1 <= '%s' and 标志 != 1 " % \
             (db_name_two,str(dict_db[0]['皮重日期']),str(dict_db[0]['皮重日期']+datetime.timedelta(10)))
    print(id_sql)
    id_sql_df = Do_Mysql_dict().query_sql(id_sql)
    if len(id_sql_df) >= 1 :
        print("打印")
        mix_only_all(id, id_sql_df)

# 匹配总量大于一的后处理情况
def mix_only_all(id,id_list):
    id_update = r"UPDATE zt_3 SET id_2 = %s WHERE id = %s" % (str(id_list[0]["id"]), id)
    Do_Mysql_dict().update_sql(id_update)
    id_update_2 = r"UPDATE zy_3 SET 标志 = 1 WHERE id = %s" % (str(id_list[0]["id"]))
    Do_Mysql_dict().update_sql(id_update_2)


if __name__ == '__main__':

    list_data = []
    for i in range(10,37447):
        print(i)
        select_db(i)