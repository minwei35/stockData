from datetime import datetime

from sqlalchemy import Column, String, Float, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base

import utils.transferValueUtils as tv

__author__ = 'Jeremysan'

Base = declarative_base()


class StockBasic(Base):
    __tablename__ = 'stock_basic'

    # 证券代码
    code = Column(String, primary_key=True)
    # 证券名称
    code_name = Column(String)
    # 上市日期
    ipodate = Column(String)
    # 退市日期
    outdate = Column(String)
    # 证券类型，其中1：股票，2：指数,3：其它
    type = Column(String)
    # 上市状态，其中1：上市，0：退市
    status = Column(String)

    @staticmethod
    def tranfer(row):
        stock_info = StockBasic()
        stock_info.code = tv.get_attr_string(row, 'code')
        stock_info.code_name = tv.get_attr_string(row, 'code_name')
        stock_info.ipodate = tv.get_attr_string(row, 'ipoDate')
        stock_info.outdate = tv.get_attr_string(row, 'outDate')
        stock_info.type = tv.get_attr_string(row, 'type')
        stock_info.status = tv.get_attr_string(row, 'status')
        return stock_info


class StockIndustry(Base):
    __tablename__ = 'stock_industry'

    # 证券代码
    code = Column(String, primary_key=True)
    # 证券名称
    code_name = Column(String)
    # 更新日期
    update_date = Column(String)
    # 所属行业
    industry = Column(String)
    # 所属行业类别
    industry_classification = Column(String)

    @staticmethod
    def transfer(row):
        stock_industry = StockIndustry()
        stock_industry.update_date = tv.get_attr_string(row, 'updateDate')
        stock_industry.code = tv.get_attr_string(row, 'code')
        stock_industry.code_name = tv.get_attr_string(row, 'code_name')
        stock_industry.industry = tv.get_attr_string(row, 'industry')
        stock_industry.industry_classification = tv.get_attr_string(row, 'industryClassification')
        return stock_industry


class StockDataUpdateRecord(Base):
    __tablename__ = 'stock_data_update_record'

    # 证券代码
    code = Column(String(10), primary_key=True, nullable=False)
    # 更新的最新日期
    update_daily_basic_date = Column(String(10))
    # 是否上市
    is_list = Column(Float(1))


class StockKData(Base):
    __tablename__ = 'stock_k_data'

    # 主键ID，由代码和日期组成
    id = Column(String, primary_key=True)
    # 证券代码
    code = Column(String)
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
    # 昨收盘价
    preclose = Column(Float)
    # 成交数量 单位：股
    volume = Column(Float)
    # 成交金额 精度：小数点后4位；单位：人民币元
    amount = Column(Float)
    # 复权状态(1：后复权， 2：前复权，3：不复权）
    adjustflag = Column(Float)
    # 换手率 精度：小数点后6位；单位：%
    turn = Column(Float)
    # 交易状态  1：正常交易 0：停牌
    tradestatus = Column(Float)
    # 涨跌幅（百分比）  精度：小数点后6位
    pctchg = Column(Float)
    # 滚动市盈率  精度：小数点后6位
    pettm = Column(Float)
    # 滚动市销率  精度：小数点后6位
    psttm = Column(Float)
    # 滚动市现率  精度：小数点后6位
    pcfncfttm = Column(Float)
    # 市净率  精度：小数点后6位
    pbmrq = Column(Float)
    # 是否ST  1是，0否
    isst = Column(Float)

    @staticmethod
    def transfer(row):
        # date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST
        stock_k_data = StockKData()
        stock_k_data.trade_date = tv.get_attr_string(row, 'date')
        stock_k_data.code = tv.get_attr_string(row, 'code')
        stock_k_data.open = tv.get_attr_float(row, 'open')
        stock_k_data.high = tv.get_attr_float(row, 'high')
        stock_k_data.low = tv.get_attr_float(row, 'low')
        stock_k_data.close = tv.get_attr_float(row, 'close')
        stock_k_data.preclose = tv.get_attr_float(row, 'preclose')
        stock_k_data.volume = tv.get_attr_float(row, 'volume')
        stock_k_data.amount = tv.get_attr_float(row, 'amount')
        stock_k_data.adjustflag = tv.get_attr_float(row, 'adjustflag')
        stock_k_data.turn = tv.get_attr_float(row, 'turn')
        stock_k_data.tradestatus = tv.get_attr_float(row, 'tradestatus')
        stock_k_data.pctchg = tv.get_attr_float(row, 'pctChg')
        stock_k_data.pettm = tv.get_attr_float(row, 'peTTM')
        stock_k_data.pbmrq = tv.get_attr_float(row, 'pbMRQ')
        stock_k_data.psttm = tv.get_attr_float(row, 'psTTM')
        stock_k_data.pcfncfttm = tv.get_attr_float(row, 'pcfNcfTTM')
        stock_k_data.isst = tv.get_attr_float(row, 'isST')
        stock_k_data.id = stock_k_data.code + ':' + stock_k_data.trade_date
        return stock_k_data


class StockConcept(Base):
    __tablename__ = 'stock_concept'

    # 概念分类ID
    code = Column(String, primary_key=True)
    # 概念分类名称
    name = Column(String)

    @staticmethod
    def transfer(row):
        stock_concept = StockConcept()
        stock_concept.code = row['gn_code']
        stock_concept.name = row['gn_name']
        return stock_concept


class StockConceptDetails(Base):
    __tablename__ = 'stock_concept_stock'

    # 概念分类ID
    gn_code = Column(String)
    # 概念对应股票代码
    code = Column(String)
    # 主键ID，由代码和概念分类ID组成
    id = Column(String, Sequence("STOCK_CONCEPT_DETAILS_SEQ"), primary_key=True)

    @staticmethod
    def transfer(row):
        stock_concept_details = StockConceptDetails()
        stock_concept_details.gn_code = row['concept_code']
        stock_concept_details.code = row['code']
        return stock_concept_details


class StockCommonDetails(Base):
    __tablename__ = 'stock_common_info'

    # 概念对应股票代码
    code = Column(String, primary_key=True)
    # 概念对应股票代码
    name = Column(String)
    # 收盘价
    close = Column(Float)
    # 涨跌幅
    pct_change = Column(Float)
    # 涨跌
    price_change = Column(Float)
    # 换手率
    turn = Column(Float)
    # 振幅
    amplitude = Column(Float)
    # 成交额
    amount = Column(Float)
    # 流通股票
    circulating_shares = Column(Float)
    # 流通市值
    circulating_marking_value = Column(Float)
    # 市盈率
    pe = Column(Float)
    # 更新时间
    update_time = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def transfer(row):
        stock_common_details = StockCommonDetails()
        stock_common_details.code = row['code']
        stock_common_details.name = row['name']
        stock_common_details.close = row['close']
        stock_common_details.pct_change = row['pct_change']
        stock_common_details.price_change = row['price_change']
        stock_common_details.turn = row['turn']
        stock_common_details.amplitude = row['amplitude']
        stock_common_details.amount = tv.get_ths_float_have_chinese(row['amount'])
        stock_common_details.circulating_shares = tv.get_ths_float_have_chinese(row['circulating_shares'])
        stock_common_details.circulating_marking_value = tv.get_ths_float_have_chinese(row['circulating_marking_value'])
        stock_common_details.pe = tv.get_ths_float(row['pe'])
        stock_common_details.update_time = datetime.now()
        return stock_common_details
