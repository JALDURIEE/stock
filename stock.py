#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import time
from plotly import offline
import requests


codes1 = {
    '上证指数': 'SH000001',
    '深证成指': 'SZ399001',
    '创业板指': 'SZ399006',
    '沪深300': 'SH000300',
    '上证50': 'SH000016',
    '中证红利': 'SH000922',
    '中证500': 'SH000905',
    '中证1000': 'SH000852',
    '恒生指数': 'HKHSI',
    '纳斯达克100': '.NDX'
}

codes2 = {
    '中证畜牧': 'CSI930707',
    '中证医疗': 'SZ399989',
    '中证白酒': 'SZ399997',
    '中证军工': 'SZ399967',
    '中证银行': 'SZ399986',
    '半导体': 'CSIH30184',
    '中证煤炭': 'SZ399998',
    '动漫游戏': 'CSI930901',
    '新能源': 'SH000941',
    '光伏产业': 'CSI931151',
    '房地产': 'CSI931775',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'cookie': 'device_id=0bd1da24552e228a249df868ec7b4650; s=by1va3j3up; Hm_lvt_1db88642e346389874251b5a1eded6e3=1661954313,1663415348; _gid=GA1.2.671812870.1663415350; bid=161460bd6104e86c6c821f2c9ac6f349_l85vh01t; snbim_minify=true; xq_a_token=80b283f898285a9e82e2e80cf77e5a4051435344; xqat=80b283f898285a9e82e2e80cf77e5a4051435344; xq_r_token=01c799b47d711195ad89f38fa2cc6b9c9fb7e4e3; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY2NTcwNTUzNCwiY3RtIjoxNjYzNDIxMzA3NDYwLCJjaWQiOiJkOWQwbjRBWnVwIn0.ZN9kp1xV2Td_nFVTBPzJTdqZZz7FB9jydgL2XSIIFFvTnZMaQkHblllF0NDQAfIaQrtrcoZM6n6HV5OaEHnpj80L88OOErYDKVFQ5iUQWhGvwyAYYWD_D8Td06jmLwk20cE9rs_mcEOKJ7fXVZGiKsuKVlPIuzQWNoJcglM3ijV4ZlYuNM_h92aEtge2zeybZrIBC-CuCqLkNn_lmK8lMxiXMAy1cPaKpJcQ5cg-e_K4c9R3-1ltEcN-ctJAKX0M3V07iDlthgKrDUzB79XGIAhg8R9o4oMxAb_tT8yAAguu0WbXLZDS3QBO6EZ-WnyxOItCBNbEElgm9df_-Irw3w; u=431663421326562; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1663480662; _ga_34B604LFFQ=GS1.1.1663479059.11.1.1663480663.58.0.0; _ga=GA1.1.2023299546.1659613831',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

kline_url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'


# 查询指数的k线数据
def get_kine_data(code):
    params = {
        'symbol': code,
        'begin': int(round(time.time() * 1000)),
        'period': 'week',
        'type': 'before',
        'count': -1,
        'indicator': 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
    }
    response = get_response(url=kline_url, params=params, headers=headers)
    # print(json.dumps(response.json()))
    return response.json()


# 获取指数一周的涨幅
def get_week_data(code):
    json_data = get_kine_data(code)
    # precent_list = []
    # for item in json_data['data']['item']:
    #     # item列表中第8个元素代表涨幅
    #     precent_list.append(item[7])
    # # 返回一周涨幅
    # return round(sum(precent_list),2)
    return json_data['data']['item'][0][7]


# 获取字典中指数的一周涨幅
def get_week_data_list(codes):
    list = []
    for key, value in codes.items():
        print(f'正在获取{key}的本周涨幅数据')
        percent = get_week_data(value)
        item = (key, value, percent)
        list.append(item)
        print('获取数据成功')
    #根据涨幅升序排序
    return sorted(list, key=lambda x: x[2])


def get_response(url, params, headers):
    # 请求被服务器断开拒绝以后重新发送请求
    while True:
        try:
            response = requests.get(url=url, params=params, headers=headers)
            return response
        except Exception as e:
            print(e)
            time.sleep(2)

#显示图形界面
def show_html(codes,filepath,title):
    list = get_week_data_list(codes)
    x = []
    y = []
    text = []
    for item in list:
        x.append(item[0])
        y.append(item[2]/100)
        text.append(str(item[2])+'%')
    data = [{
        'type':'bar',
        'x':x,
        'y':y,
        'text':text,
        'textposition':'outside',
    }]
    myLayout = {
        'title':title,
        'yaxis': {'tickformat': ',.0%'}
    }
    fig = {'data':data,'layout':myLayout}
    offline.plot(fig,filename=filepath)


if __name__ == '__main__':
    # get_data('SH000001')
    # print(get_week_data_list(codes1))
    show_html(codes1,'stock1.html','本周主要宽基指数涨幅')
    show_html(codes2,'stock2.html','本周主要行业指数涨幅')