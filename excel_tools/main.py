# -*- encoding: utf-8 -*-
'''
@File    :   main.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/10 10:17   LiuDongxing      1.0         None
'''
# import lib
from mysql_tools import Do_Mysql_dict
import datetime

def select(id):
    id_sql = r"select 皮重日期 from zt_3 where id = %s" % (id)
    id_sql_df = Do_Mysql_dict().query_sql(id_sql)
    print(id_sql_df[0]["皮重日期"])
    return id_sql_df[0]["皮重日期"]


if __name__ == '__main__':
    print(select(1) < select(1000))
    print((select(1) - select(1000)).days)