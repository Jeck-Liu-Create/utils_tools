# -*- encoding: utf-8 -*-
'''
@File    :   del_chinese.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/4/25 9:25   LiuDongxing      1.0         None
'''

# import lib
import re
import os
import cv2


def renamedir(path):
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        oldpath = os.path.join(path,list[i])
        newname =  re.sub('[\u4e00-\u9fa5]','',oldpath)
        os.rename(oldpath,newname)
        print(newname)

if __name__ == "__main__":
    rootdir = r'D:\project\utils_tools\img'
    savedir =  r'D:/project/utils_tools/img_rename/'

    renamedir(rootdir)
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])

        # # 你想对文件的操作
        filename = list[i]
        first_img = cv2.imread(path,1)

        # 按照指定格式保存
        base_filename = filename

        dirset = os.path.join(savedir, base_filename)

        cv2.imwrite(dirset,first_img)

        print(path)
        print(filename)