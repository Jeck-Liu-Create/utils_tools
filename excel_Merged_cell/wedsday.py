# -*- encoding: utf-8 -*-
'''
@File    :   wedsday.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/18 19:48   LiuDongxing      1.0         None
'''

# import lib
import os
import xlsxwriter as xw

def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['序号', '酒店', '价格']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insert_data = list(data[j].values())
        row = 'A' + str(i)
        worksheet1.write_row(row, insert_data)
        if j > 0:  # 从第二行数据开始比较
            if data[j]["id"] == data[j - 1]["id"]:
                for column in range(2):  # 拿到需要合并的列
                    worksheet1.merge_range(i - 2, column, i - 1, column, insert_data[column])  # 合并单元格
        i += 1
    workbook.close()  # 关闭表


if __name__ == '__main__':
    # "-------------数据用例-------------"
    testData = [
        {"id": 1, "name": "立智", "price": 100},
        {"id": 2, "name": "维纳", "price": 200},
        {"id": 3, "name": "如家", "price": 300},
        {"id": 3, "name": "如家", "price": 400},
        {"id": 3, "name": "如家", "price": 200},
        {"id": 4, "name": "朗丽兹", "price": 500}
    ]
    fileName = os.path.join(os.path.abspath('.'), 'data_test_2.xlsx')
    xw_toExcel(testData, fileName)
