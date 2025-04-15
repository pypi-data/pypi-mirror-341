from cashare.common.dname import url1
#所有股票拆分日历
from cashare.common.get_data import _retry_get
from cashare.common.var_token import get_token

def sp_data(ca_code):
    li = handle_url(code=ca_code, token=get_token())
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        # r["date"] = pd.to_datetime(r["date"], unit='ms')

        return r

def handle_url(code,token):
    g_url = url1 + '/us/stock/sp/' +code+'/'+token
    return g_url
if __name__ == '__main__':
    import cashare as ca
    ca.set_token('r9fcbc791fa47741af9d440bdeb98d9a532')
    df=ca.sp_data( ca_code='aapl')
    print(df)
    pass




