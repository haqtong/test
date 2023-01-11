# encoding=utf-8
import re
import json


def hex_diy(x):
    hex_num = hex(x)
    if len(hex_num) == 5:
        list = [hex_num[:2], '0', hex_num[2:]]
        return ''.join(list)
    else:
        return hex_num


def staiton_link(station_code_10):
    station_link_code = {}
    # 初始化
    for staiton_id, station_name in station_code_10.items():
        staiton_id = str(staiton_id)
        station_link_code[staiton_id] = {'line': [], 'CN': [], '16_code': [], 'link_ex': [], 'link_station': []}

    # 补充地铁站点，相关编码映射
    for staiton_id, station_name in station_code.items():
        staiton_id = str(staiton_id)
        station_link_code[staiton_id]['CN'] = station_name
        station_link_code[staiton_id]['16_code'] = hex_diy(int(staiton_id))
        station_link_code[staiton_id]['line'] = hex_diy(int(staiton_id))[2:4]

    # 补充邻接站点
    for key, values in station_link_code.items():

        station_name_unique = values['CN'].split('(')[0][:-1]
        for station_name, station_id in station_code.items():
            if station_name.split('(')[0][:-1] == station_name_unique:
                station_link_code[key]['link_ex'].append(station_id)
        if int(key) in station_link_code[key]['link_ex']:
            station_link_code[key]['link_ex'].remove(int(key))
        # 获取指定站点的未知，将相邻站点放入link信息中


    with open("station_link_code.json", "w+", encoding='utf-8') as f:
        f.write(json.dumps(station_link_code, ensure_ascii=False))


if __name__ == '__main__':
    with open('station_code.json', encoding='utf-8') as f:
        station_code = json.load(f)
    staiton_link(station_code)
