from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float
import utils.transferValueUtils as tv
__author__ = 'Jeremysan'

Base = declarative_base()


class StockMarket(Base):
    # 表名
    __tablename__ = 'stock_market'

    # 主键ID，由代码和日期组成
    id = Column(String, primary_key=True)
    # 股票代码
    ts_code = Column(String)
    # 交易日期
    trade_date = Column(String)
    # 开盘价
    open = Column(Float)
    # 最高价
    high = Column(Float)
    # 最低价
    low = Column(Float)
    # 收盘价
    close = Column(Float)
    # 昨日收盘价
    pre_close = Column(Float)
    # 涨跌额
    change = Column(Float)
    # 涨跌幅
    pct_chg = Column(Float)
    # 成交量 （手）
    vol = Column(Float)
    # 成交额 （千元）
    amount = Column(Float)
    # 5日均线（成交量）
    ma5 = Column(Float)
    # 5日均线（成交额）
    ma5_v = Column(Float)
    # 10日均线（成交量）
    ma10 = Column(Float)
    # 10日均线（成交额）
    ma10_v = Column(Float)
    # 20日均线（成交量）
    ma20 = Column(Float)
    # 20日均线（成交额）
    ma20_v = Column(Float)
    # 30日均线（成交量）
    ma30 = Column(Float)
    # 30日均线（成交额）
    ma30_v = Column(Float)
    # 60日均线（成交量）
    ma60 = Column(Float)
    # 60日均线（成交额）
    ma60_v = Column(Float)
    # 120日均线（成交量）
    ma120 = Column(Float)
    # 120日均线（成交额）
    ma120_v = Column(Float)
    # 250日均线（成交量）
    ma250 = Column(Float)
    # 250日均线（成交额）
    ma250_v = Column(Float)
    # 量比
    volume_ratio = Column(Float)
    # 换手率
    turnover_rate = Column(Float)

    @staticmethod
    def tranfer(row):
        stock_market = StockMarket()
        stock_market.ts_code = tv.get_string(row.ts_code)
        stock_market.trade_date = tv.get_string(row.trade_date)
        # 主键ID由代码加日期组成，是唯一的
        stock_market.id = stock_market.ts_code+stock_market.trade_date
        stock_market.open = tv.get_float(row.open)
        stock_market.high = tv.get_float(row.high)
        stock_market.low = tv.get_float(row.low)
        stock_market.close = tv.get_float(row.close)
        stock_market.amount = tv.get_float(row.amount)
        stock_market.pre_close = tv.get_float(row.pre_close)
        stock_market.change = tv.get_float(row.change)
        stock_market.pct_chg = tv.get_float(row.pct_chg)
        stock_market.vol = tv.get_float(row.vol)
        stock_market.ma5 = tv.get_float(row.ma5)
        stock_market.ma10 = tv.get_float(row.ma10)
        stock_market.ma20 = tv.get_float(row.ma20)
        stock_market.ma30 = tv.get_float(row.ma30)
        stock_market.ma60 = tv.get_float(row.ma60)
        stock_market.ma120 = tv.get_float(row.ma120)
        stock_market.ma250 = tv.get_float(row.ma250)
        stock_market.ma5_v = tv.get_float(row.ma_v_5)
        stock_market.ma10_v = tv.get_float(row.ma_v_10)
        stock_market.ma20_v = tv.get_float(row.ma_v_20)
        stock_market.ma30_v = tv.get_float(row.ma_v_30)
        stock_market.ma60_v = tv.get_float(row.ma_v_60)
        stock_market.ma120_v = tv.get_float(row.ma_v_120)
        stock_market.ma250_v = tv.get_float(row.ma_v_250)
        stock_market.volume_ratio = tv.get_float(row.volume_ratio)
        stock_market.turnover_rate = tv.get_float(row.turnover_rate)
        return stock_market


class StockInfo(Base):
    __tablename__ = 'stock_all'

    # ts代码
    ts_code = Column(String, primary_key=True)
    # 股票名称
    name = Column(String)
    # 所在地区
    area = Column(String)
    # 所属行业
    industry = Column(String)
    # 股票代码
    symbol = Column(String)
    # 市场类型（主板/中小板/创业板）
    market = Column(String)
    # 前缀（沪市SH，深市SZ）
    prefix = Column(String)
    # 上市日期
    list_date = Column(String)

    @staticmethod
    def tranfer(row):
        stock_info = StockInfo()
        stock_info.ts_code = tv.get_string(row[0])
        # stock_info.ts_code = tv.get_string(row.ts_code)
        # stock_info.symbol = tv.get_string(row.symbol)
        stock_info.symbol = tv.get_string(row[1])
        stock_info.name = tv.get_string(row[2])
        # stock_info.name = tv.get_string(row.name)
        stock_info.area = tv.get_string(row[3])
        # stock_info.area = tv.get_string(row.area)
        stock_info.industry = tv.get_string(row[4])
        # stock_info.industry = tv.get_string(row.industry)
        stock_info.market = tv.get_string(row[5])
        # stock_info.market = tv.get_string(row.market)
        stock_info.prefix = tv.get_string(row[0]).split(".")[1]
        # stock_info.list_date = tv.get_string(row.list_date)
        stock_info.list_date = tv.get_string(row[6])
        return stock_info


class StockDailyBasic(Base):
    __tablename__ = 'stock_daily_basic'

    # 主键
    id = Column(String, primary_key=True)
    # 股票代码
    ts_code = Column(String)
    # 交易日期
    trade_date = Column(String)
    # 收盘价
    close = Column(Float)
    # 换手率
    turnover_rate = Column(Float)
    # 换手率（自然流通股）
    turnover_rate_f = Column(Float)
    # 量比
    volume_ratio = Column(Float)
    # 市盈率（总市值/净利润）
    pe = Column(Float)
    # 市盈率（TTM）
    pe_ttm = Column(Float)
    # 市净率（总市值 / 净资产）
    pb = Column(Float)
    # 市销率
    ps = Column(Float)
    # 市销率（TTM）
    ps_ttm = Column(Float)
    # 总股本 （万股）
    total_share = Column(Float)
    # 流通股本 （万股）
    float_share = Column(Float)
    # 自由流通股本 （万）
    free_share = Column(Float)
    # 总市值 （万元）
    total_mv = Column(Float)
    # 流通市值（万元）
    circ_mv = Column(Float)

    @staticmethod
    def tranfer(row):
        stock_daily_basic = StockDailyBasic()
        stock_daily_basic.ts_code = tv.get_string(row.ts_code)
        stock_daily_basic.trade_date = tv.get_string(row.trade_date)
        # 主键ID由代码加日期组成，是唯一的
        stock_daily_basic.id = stock_daily_basic.ts_code + stock_daily_basic.trade_date
        stock_daily_basic.close = tv.get_float(row.close)
        stock_daily_basic.turnover_rate = tv.get_float(row.turnover_rate)
        stock_daily_basic.turnover_rate_f = tv.get_float(row.turnover_rate_f)
        stock_daily_basic.volume_ratio = tv.get_float(row.volume_ratio)
        stock_daily_basic.pe = tv.get_float(row.pe)
        stock_daily_basic.pe_ttm = tv.get_float(row.pe_ttm)
        stock_daily_basic.pb = tv.get_float(row.pb)
        stock_daily_basic.ps = tv.get_float(row.ps)
        stock_daily_basic.ps_ttm = tv.get_float(row.ps_ttm)
        stock_daily_basic.total_share = tv.get_float(row.total_share)
        stock_daily_basic.float_share = tv.get_float(row.float_share)
        stock_daily_basic.free_share = tv.get_float(row.free_share)
        stock_daily_basic.total_mv = tv.get_float(row.total_mv)
        stock_daily_basic.circ_mv = tv.get_float(row.circ_mv)
        return stock_daily_basic


class StockUpdateRecord(Base):
    __tablename__ = 'stock_update_record'

    # ts代码
    ts_code = Column(String, primary_key=True)
    # 通用行情更新最后日期
    update_market_date = Column(String)
    # 每日基础信息更新最后日期
    update_daily_basic_date = Column(String)


class StockConcept(Base):
    __tablename__ = 'stock_concept'

    # 概念分类ID
    code = Column(String, primary_key=True)
    # 概念分类名称
    name = Column(String)
    # 来源
    src = Column(String)

    @staticmethod
    def transfer(row):
        stock_concept = StockConcept()
        stock_concept.code = tv.get_string(row.code)
        stock_concept.name = tv.get_string(row[1])
        stock_concept.src = tv.get_string(row.src)
        return stock_concept



class StockConceptDetails(Base):
    __tablename__ = 'stock_concept_details'

    # 概念分类ID
    id = Column(String, primary_key=True)
    # 概念分类股票代码
    ts_code = Column(String, primary_key=True)

    @staticmethod
    def transfer(row):
        stock_concept_details = StockConceptDetails()
        stock_concept_details.id = tv.get_string(row.id)
        stock_concept_details.ts_code = tv.get_string(row.ts_code)
        return stock_concept_details
