import pandas as pd
import math


def trans(lon, lat, distance, amuith=90):
    '''

    :param lon:
    :param lat:
    :param distance:
    :param amuith: 方向角
    :return:
    '''
    RE = 6371.393 * 1000  # 赤道半径,单位：m
    re = RE * math.cos(lat / 180 * math.pi)  # 纬度切面的半径
    lon2 = lon + distance * math.sin(amuith / 180 * math.pi) / (re * 2 * math.pi) * 360  # 求切面长度占比，与已知点经度相加
    lat2 = lat + distance * math.cos(amuith / 180 * math.pi) / (re * 2 * math.pi) * 360
    return lon2, lat2


def exec():
    path = r'D:\program\data\daily_test\data\25个聚集点指标.csv'
    df = pd.read_csv(path)
    print(df.head())
    df.loc[:, 'loc1'] = df.apply(lambda x: trans(x['点的wgs经度'], x['点的wgs纬度'], 550 / 1.16075, 0), axis=1)
    df.loc[:, 'loc2'] = df.apply(lambda x: trans(x['点的wgs经度'], x['点的wgs纬度'], 550 / 1.16075, 90), axis=1)
    df.loc[:, 'loc3'] = df.apply(lambda x: trans(x['点的wgs经度'], x['点的wgs纬度'], 550 / 1.16075, 180), axis=1)
    df.loc[:, 'loc4'] = df.apply(lambda x: trans(x['点的wgs经度'], x['点的wgs纬度'], 550 / 1.16075, 270), axis=1)
    df.loc[:, 'loc1_trans'] = df.apply(lambda x: x['loc1'][1], axis=1)
    df.loc[:, 'loc2_trans'] = df.apply(lambda x: x['loc2'][0], axis=1)
    df.loc[:, 'loc3_trans'] = df.apply(lambda x: x['loc3'][1], axis=1)
    df.loc[:, 'loc4_trans'] = df.apply(lambda x: x['loc4'][0], axis=1)
    df.loc[:, 'limit_point'] = df.apply(lambda x: [x['loc1_trans'], x['loc2_trans'], x['loc3_trans'], x['loc4_trans']],axis = 1)
    df.to_csv('test.csv')
    limit_point_list = df['limit_point'].values.tolist()

    with open('output/aim_sql.txt','w',encoding='utf-8') as f:
        sql = 'create table temp_linshi_small_data_sum_20221125_all_part_2_sub_2 as select * from temp_linshi_small_data_sum_20221125_all_part_2 where '
        f.write(sql )
        for limit_point in limit_point_list:
            sql = '(GRID_LAT_CENT >= {} and GRID_LAT_CENT < {} and GRID_LNG_CENT >= {}  and GRID_LNG_CENT < {}) or'.format(limit_point[1],limit_point[3],limit_point[0],limit_point[2])
            f.write(sql+'\n')
        f.write(';')


if __name__ == '__main__':
    exec()
    # a, b = trans(120.948112, 30.519695, 4000, 90)
    # print(a,b)
