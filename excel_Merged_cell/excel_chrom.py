# -*- encoding: utf-8 -*-
'''
@File    :   excel_chrom.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/5/18 19:51   LiuDongxing      1.0         None
'''

# import lib
import pandas as pd

# Create a test df
df = pd.DataFrame({'Name': ['Tesla','Tesla','Toyota','Ford','Ford','Ford'],
                   'Type': ['Model X','Model Y','Corolla','Bronco','Fiesta','Mustang']})

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']
merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 2})

for car in df['Name'].unique():
    # find indices and add one to account for header
    u=df.loc[df['Name']==car].index.values + 1

    if len(u) <2:
        pass # do not merge cells if there is only one car name
    else:
        # merge cells using the first and last indices
        worksheet.merge_range(u[0], 0, u[-1], 0, df.loc[u[0],'Name'], merge_format)
writer.save()
