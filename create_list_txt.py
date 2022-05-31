# -*- encoding: utf-8 -*-
'''
@File    :   create_list_txt.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/4/25 14:45   LiuDongxing      1.0         None
'''

# import lib
import os

if __name__ == "__main__":
    src = r"D:\project\utils_tools\train_images"
    path_txt = r"./train_list.txt"
    f = open(path_txt, 'a', encoding='UTF-8')
    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            if filename.endswith('.jpg'):
                print(filename)
                # image_path = dict01['imagePath']
                # # f.write('rgb/'+image_path.split('\\')[-1]+'\t')
                # # f.write('asda')
                # path_txt = './rgb/'+image_path.split('\\')[-1]+'.txt'
                f.write(filename + '\n')

    f.close()