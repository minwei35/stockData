import baostock as bs
import pandas as pd
from mapper.stock import StockBasic
from database import sqlUtils


class DayStockAll(object):
    def update_stock_all(self):
        bs.login()
        rs = bs.query_stock_basic()
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        data = pd.DataFrame(data_list, columns=rs.fields)
        # 创建会话
        session = sqlUtils.get_sqlalchemy_session()
        d_len = data.shape[0]
        for i in range(d_len):
            row = data.iloc[i]
            stock_basic = StockBasic.tranfer(row)
            session.merge(stock_basic)
            session.commit()
        session.close()
        bs.logout()
        print("股票列表已更新")


day_stock = DayStockAll()
day_stock.update_stock_all()
