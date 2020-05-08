import baostock as bs
import pandas as pd
from utils import transferValueUtils
from mapper.stock import StockKData

bs.login()
rs = bs.query_history_k_data_plus(code='sz.002086', fields=
                                              "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                              start_date='2020-05-01', end_date='2020-05-06')
k_data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    k_data_list.append(rs.get_row_data())
df = pd.DataFrame(k_data_list, columns=rs.fields)
result = df.iloc[0]
print('result : ' + result)
trans = StockKData.transfer(result)
print('trans : ')
print(trans)
bs.logout()
