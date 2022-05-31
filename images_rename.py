# -*- encoding: utf-8 -*-
'''
@File    :   images_rename.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/4/25 8:45   LiuDongxing      1.0         None
'''

# import lib
import cv2
import os
import random


path = r'E:\user\one\picture'
img_paths = os.listdir(path)
print(img_paths)
# print(img_paths)
# img_paths.sort(key=lambda x: int(x[:-4]))  # 倒着数第四位'.'为分界线，按照‘.'左边的数字从小到大排序
# print(img_paths)
save_path = r'E:\\user\\one\\picture_rename\\'


# if not os.path.exists(save_path):
#     # 如果不存在则创建目录
#     # 创建目录操作函数
#     os.makedirs(save_path)
#     print(save_path, " create over!")
# else:
#     print(save_path, " exist!")
img_paths_random = random.sample(img_paths, 100)
i = 0
for img in img_paths_random:
    i += 1
    abs_path = os.path.join(path, img)
    print(abs_path)

    # img_name = img.split('.')[0]
    # print(img_name)
    img_mat = cv2.imread(abs_path)
    # cv2.imshow("img",img_mat)
    # cv2.waitKey(1000)
    print(save_path+str(i).zfill(6))
    cv2.imwrite(save_path + str(i).zfill(6) + ".bmp", img_mat)
    print(i)