import os
import time
from multiprocessing import Pool, Manager

import tushare as ts

from database import sqlUtils
from mapper.pojo import StockConcept, StockConceptDetails


def update_stock_concept_details(queue):
        pro = ts.pro_api()
        count = 0
        while not queue.empty():
            try:
                session = sqlUtils.get_sqlalchemy_session()
                record = queue.get()
                df = pro.concept_detail(id=str(record.code))
                print("代码为{}正在插入数据".format(record.code))
                if df is not None:
                    d_len = df.shape[0]
                    for index in range(d_len):
                        resu1 = df.iloc[index]
                        stock_concept_details = StockConceptDetails.transfer(resu1)
                        session.merge(stock_concept_details)
                    session.commit()
                    count = count + 1
                    session.close()
                    print("代码为{}插入数据完成".format(record.code))
                time.sleep(10)
            except Exception as e:
                print(repr(e))
                print("概念代码为" + record.code + "插入数据失败")
        print("当前进程完成插入的数目是{}".format(count))
        return count


if __name__ == '__main__':
    ts.set_token("f69287e7ed3a204a5edb6d6c851fd8d7709aa10cdeac741db751aa94")
    now = time.time()
    # 创建会话
    mySession = sqlUtils.get_sqlalchemy_session()
    record_list = mySession.query(StockConcept).all()
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
        result.append(p.apply_async(update_stock_concept_details, (q, )))
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
