# encoding=utf-8
import pandas as pd
import json

path1 = r'OD路径选择概率20221026.xlsx'
path2 = r'OD路径选择概率.xlsx'
output_path = r'OD路径选择概率20221114.xlsx'


def exec():
    with open('station_code.json', encoding='utf-8') as f:
        station_code = json.load(f)
    df1 = pd.read_excel(path1)
    df1 = df1[df1['PRE_LINE_ID'] != 153]
    df1 = df1.rename(
        columns={'VERSION_NO': '版本号', 'PATH_ID': '有效路径编号', 'PRE_LINE_ID': '起始线路号', 'PRE_STATION_ID': '起始车站号',
                 'LINE_ID': '目的线路号', 'STATION_ID': '目的车站号', 'PROBABILITY': '路径被选择概率', 'RP': '路径时间权值'
                 })

    df1.loc[:, '起始车站名称'] = df1['起始车站号'].apply(lambda x: station_code[str(x)])
    df1.loc[:, '目的车站名称'] = df1['目的车站号'].apply(lambda x: station_code[str(x)])

    df2 = pd.read_excel(path2)
    print(df1.columns)
    print(df2.columns)
    df2 = pd.DataFrame(df2, columns=['有效路径编号', '路径时间权值'])
    df = df1.merge(df2, on='有效路径编号', how='left')
    df.loc[:, '路径时间权值'] = df.apply(lambda x: x['路径时间权值_y'] if str(x['路径时间权值_x']) == 'nan' else x['路径时间权值_x'], axis=1)
    df = pd.DataFrame(df, columns=['版本号', '有效路径编号', '起始线路号', '起始车站号', '起始车站名称', '目的线路号', '目的车站号', '目的车站名称', '路径被选择概率',
                                   '路径时间权值'])
    df.to_excel(output_path, index=0)


if __name__ == '__main__':
    exec()

# version1_1 确定什么情况下 read_csv 要加gbk条件
# version1_2 当前版本支持写入基础路径
