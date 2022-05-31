import xlwings as xw
import pandas as pd
'''
按条件将一个工作表拆分为多个工作表
'''
file_path = r'A.xlsx'  # 给出来源工作簿的文件路径及工作簿名称
sheet_name = 'A'  # 给出要拆分的工作表的名称
app = xw.App(visible=True, add_book=False)
workbook = app.books.open(file_path)
worksheet = workbook.sheets[sheet_name]
sheet_names = [j.name for j in workbook.sheets]
print(sheet_names)
# 以DataFrame格式读取要拆分的工作表数据
value = worksheet.range('A1').options(pd.DataFrame,header = 1,
                                     index = False, expand = 'table').value  # 读取要拆分的工作表中的所有数据
print(value)
# 将数据按照“名称”分组
data = value.groupby('创单月份')
print(data)
for idx, group in data:
    print(idx)
    print(group)
    # 如果工作簿的工作表名不存在，则新增，否则替换
    if idx not in sheet_names:
        # 在工作簿中新增工作表并命名为当前的产品名称
        new_worksheet = workbook.sheets.add(idx)
        # 将按分组好的数据添加到新增的工作表
        new_worksheet.range('A1').options(index = False).value = group
    workbook.sheets[idx].range('A1').options(index = False).value = group
workbook.save()
workbook.close()
app.quit()


