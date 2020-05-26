from datetime import datetime, date, timedelta
from utils.configUtils import config

day_k_data_time = config.day_k_data_time
minute_k_data_time = config.minute_k_data_time


def get_beijing_time():
    dt = datetime.now().utcnow()
    return dt + timedelta(hours=8)


def get_day_k_data_time():
    now = datetime.now()
    # 跟配置中的日k数据入库时间进行比较，如果时间提前了，只能拿前一天的数据
    if now.hour < day_k_data_time:
        delta = timedelta(days=-1)
        today = now + delta
    else:
        today = now
    str_time = today.strftime("%Y-%m-%d")
    return str_time
