from cashare import get_token
from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
#个股股息
def div_data(ca_code):
    li = handle_url(code=ca_code, token=get_token())
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        r["date"] = pd.to_datetime(r["date"], unit='ms')

        return r

def handle_url(code,token):
    g_url=url1+'/us/stock/s_d_history/'+code+'/'+token
    return g_url
if __name__ == '__main__':
    import cashare as ca
    ca.set_token('r9fcbc791fa47741af9d440bdeb98d9a532')
    df=ca.div_data(ca_code='aapl')
    print(df)


