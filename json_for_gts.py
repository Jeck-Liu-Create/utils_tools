# -*- encoding: utf-8 -*-
'''
@File    :   json_for_gts.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/4/24 14:07   LiuDongxing      1.0   Convert JSON files to GTS
'''

# import lib
import json
import os

#  Data set requirements for paddleocr
def transfrom_dict_to_str(target_dict):
    # 根据字典重新组织数据
    list_target = []
    list_data = target_dict['shapes']
    for item in list_data:
        dict02 = {}
        # 把label 转化为transcription
        dict02['transcription'] = item['label']
        list03 = item['points']
        list04 = []
        for j in list03:
            list04.append([int(j[0]), int(j[1])])
        dict02['points'] = list04
        list_target.append(dict02)
    target_str = str(list_target)
    # 将字符中的"符号提前进行转义
    # target_str = target_str.replace("\"", "\\"")
    # 将字符中的'符号转为"
    target_str = target_str.replace("'", "\"")
    # print(target_str)
    return target_str

# Data set requirements for DB

def transfrom_dict_to_str_DB(target_dict):
    # 根据字典重新组织数据
    global target_str, strdata
    list_target = []
    list02 = []
    list_data = target_dict['shapes']
    for item in list_data:
        list01 = item['points']
        for j in list01:
            list02.append(int(j[0]))
            list02.append(int(j[1]))
        list02.append(item['label'])
        target_str = str(list02)
        target_str =  "".join(target_str.split())
        target_str = target_str.replace('\'', '')
        target_str = target_str.replace('[', '')
        target_str = target_str.replace(']', '')
    print(target_str)
    return target_str






if __name__ == "__main__":
    # json文件的文件夹
    # src = r"C:\Users\JECK\Desktop\one\getimg"
    src = r"C:\Users\JECK\Desktop\1780json"

    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            if filename.endswith('.json'):
                fd = open(os.path.join(src, filename))
                data = fd.read()
                dict01 = json.loads(data)
                target_str = transfrom_dict_to_str_DB(dict01)
                image_path = dict01['imagePath']
                # f.write('rgb/'+image_path.split('\\')[-1]+'\t')
                # f.write('asda')
                path_txt = './rgb/'+image_path.split('\\')[-1]+'.txt'
                f = open(path_txt, 'a', encoding='UTF-8')
                f.write(target_str)
                f.close()