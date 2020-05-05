import os
import time
from multiprocessing import Pool, Manager

import tushare as ts

from database import sqlUtils
from mapper.pojo import StockDailyBasic, StockUpdateRecord


def update_day_stock_by_code(queue):
        pro = ts.pro_api()
        today = int(time.time())
        # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        time_struct = time.localtime(today)
        strTime = time.strftime("%Y%m%d", time_struct)
        count = 0
        while not queue.empty():
            try:
                session = sqlUtils.get_sqlalchemy_session()
                record = queue.get()
                update_daily_basic_date = None
                start_date = record.update_daily_basic_date
                df = pro.daily_basic(ts_code=str(record.ts_code), start_date=start_date, end_date=strTime)
                print("代码为" + record.ts_code + "正在插入数据")
                if df is not None:
                    d_len = df.shape[0]
                    for index in range(d_len):
                        resu1 = df.iloc[index]
                        if index == 0:
                            update_daily_basic_date = str(resu1.trade_date)
                        stock_daily_basic = StockDailyBasic.tranfer(resu1)
                        session.merge(stock_daily_basic)
                    session.commit()
                    print("代码为" + record.ts_code + "插入数据完成")
                    # 更新当前代码的最新更新日期
                    record.update_daily_basic_date = update_daily_basic_date
                    session.merge(record)
                    session.commit()
                    count = count + 1
                    session.close()
            except Exception:
                print(Exception)
                print("代码为" + record.ts_code + "插入数据失败")
        print("当前进程完成插入的数目是{}".format(count))
        return count


if __name__ == '__main__':
    ts.set_token("f69287e7ed3a204a5edb6d6c851fd8d7709aa10cdeac741db751aa94")
    now = time.time()
    # 创建会话
    mySession = sqlUtils.get_sqlalchemy_session()
    record_list = mySession.query(StockUpdateRecord).all()
    mySession.close()
    m = Manager()
    q = m.Queue()
    before_count = 0
    for row in record_list:
        q.put(row)
        before_count = before_count+1

    p = Pool(processes=os.cpu_count())
    result = []
    for i in range(os.cpu_count()):
        result.append(p.apply_async(update_day_stock_by_code, (q,)))
    print("等待子进程完成数据插入")
    p.close()
    p.join()
    end = time.time()  # 结束计时
    total_time = end - now
    total_count = 0
    for sub_result in result:
        total_count = total_count + int(sub_result.get())
    print("更新每日行情完成耗时：{:.2f}秒，本次更新{}条记录，成功更新{}条记录".format(total_time, before_count, total_count))
    # 如果有更新失败的代码的话，以csv的格式保存
    # if not error_codes.empty():
    #     print("本次更新失败的代码有 {}".format(error_codes))
    #     datas = pd.DataFrame({"失败代码": error_codes})
    #     error_dir = "stockUpdateError\\" + str(datetime.date.today())
    #     fileutils.mkdirpwd(error_dir)
    #     datas.to_csv(error_dir + "\error_code1.csv", index=False, sep=",")
