import httpx
from cashare.common.dname import url1
import pandas as pd
from cashare.common.var_token import get_token

from cashare.common.get_data import _retry_get
def stock_list(type:str,):
    if type in['us','hk','ca','eu','tsx','cp','index','etf','fx']:
        url = url1 + '/stock/list/'+type+'/'+ get_token()
        # print(url)
        r = _retry_get(url, timeout=100)
        return r

    else:
        return "type输入错误"

if __name__ == '__main__':
    import cashare as ca

    ca.set_token('r9fcbc791fa47741af9d440bdeb98d9a532')

    df = ca.stock_list(type='hk', )
    print(df)
    df = ca.stock_list(type='us', )
    print(df)

    # df = stock_list(type='eu', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    # df=stock_list(type='hk',token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    # df = stock_list(type='us', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    #
    # df = stock_list(type='tsx', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    # df = stock_list(type='cp', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    # # df = stock_list(type='index', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # # print(df)
    # df = stock_list(type='etf', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)
    # df = stock_list(type='fx', token='h9fcbc791fa47741ab2658eb9a51f557856')
    # print(df)

    pass



