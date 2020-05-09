from mapper.stock import StockIndustry
from database import sqlUtils
import baostock as bs
import pandas as pd


session = sqlUtils.get_sqlalchemy_session()
bs.login()
rs = bs.query_stock_industry()
industry_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    industry_list.append(rs.get_row_data())
df = pd.DataFrame(industry_list, columns=rs.fields)
d_len = df.shape[0]
for index in range(d_len):
    row = df.iloc[index]
    stock_industry = StockIndustry.transfer(row)
    session.merge(stock_industry)
session.commit()
session.close()
bs.logout()
