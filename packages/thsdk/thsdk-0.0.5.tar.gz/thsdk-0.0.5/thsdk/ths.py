#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .quote_lib import QuoteLib
from .util import *
from .guest_account import rand_account
from .model import Reply
from .constants import *
import re
import datetime
import random


class ThsQuote:
    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', zhu_addr)
        account = rand_account()
        ops.setdefault("username", account[0])
        ops.setdefault("password", account[1])

        self.ops = ops
        self._lib = QuoteLib(ops)
        self._login = False
        self.__share_instance = random.randint(6666666, 8888888)

    @property
    def zip_version(self):
        return 2

    @property
    def share_instance(self):
        self.__share_instance += 1
        return self.__share_instance

    def connect(self):
        """
        连接到行情服务器
        :return:
        """
        response = self._lib.connect()
        if response == "" or response is None or response == b'':
            raise ValueError("No data found.")

        rs = Reply(response)
        if rs.err_code == 0:
            self._login = True
        return rs

    def disconnect(self):
        """
        断开与行情服务器的连接
        :return:
        """
        self._login = False

        response = self._lib.disconnect()
        rs = Reply(response)
        return rs

    def about(self):
        """
        关于信息
        :return:
        """
        about = self._lib.about()
        return about.decode('utf-8')

    @staticmethod
    def login_required(func):
        def wrapper(self, *args, **kwargs):
            if not self._login:
                print("请先登录.")
                reply = Reply("{}")
                return reply
            return func(self, *args, **kwargs)

        return wrapper

    @login_required
    def history_minute_time_data(self, code: str, date: str, fields: list = None):
        # 检查code的长度和前四位         # if len(code) != 10 or not (code.startswith('USHA') or code.startswith('USZA')):
        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        # 检查date的格式
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date must be in the format YYYYMMDD, e.g. 20241220.")

        data_type = "1,10,13,19,40"
        market = code[:4]
        short_code = code[4:]
        req = f"id=207&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&datatype={data_type}&date={date}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No history data found.")

        reply = Reply(response)
        reply.convert_data()

        for entry in reply.resp.data:
            if "time" in entry:  # 检查是否存在 "time" 键
                entry["time"] = ths_int2time(entry["time"])

        if fields:
            reply.resp.data = [entry for entry in reply.resp.data if all(field in entry for field in fields)]

        return reply

    @login_required
    def security_bars(self, code: str, start: int, end: int, adjust: str, period: int):
        """
        获取k线数据。

        :param code: 证券代码，必须是10个字符长，并以'USHA'或'USZA'开头。
        :param start: 开始时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param end: 结束时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param adjust: 复权类型，必须是有效的复权值之一。
        :param period: 周期类型，必须是有效的周期值之一。
        """

        valid_fuquan = {Fuquanqian, Fuquanhou, FuquanNo}
        valid_periods = {Kline1m, Kline5m, Kline15m, Kline30m, Kline60m, Kline120m, KlineDay, KlineWeek, KlineMoon,
                         KlineQuarterly, KlineYear}

        if adjust not in valid_fuquan:
            raise ValueError("Invalid adjust.")

        if period not in valid_periods:
            raise ValueError("Invalid period.")

        m_period = {Kline1m, Kline5m, Kline15m, Kline30m, Kline60m, Kline120m}

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,7,8,9,11,13,19"
        market = code[:4]
        short_code = code[4:]
        req = f"id=210&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&fuquan={adjust}&datatype={data_type}&period={period}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No history data found.")

        reply = Reply(response)
        reply.convert_data()

        if period in m_period:
            for entry in reply.resp.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = ths_int2time(entry["time"])
        else:
            for entry in reply.resp.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = datetime.datetime.strptime(str(entry["time"]), "%Y%m%d")

        return reply

    @login_required
    def get_block_data(self, block_id: int):
        """
        :param block_id: 板块代码，必须是有效的板块代码。
            0xC6A6 # 全部A股
            0xE # 沪深A股
            0x15 # 沪市A股
            0x1B # 深市A股
            0xC5E3 # 北京A股
            0xCFE4 # 创业板
            0xCBE5 # 科创板
            0xDBC6 # 风险警示
            0xDBC7 # 退市整理
            0xF026 # 行业和概念
            0xCE5E # 概念
            0xCE5F # 行业
            0xc4b5 # 行业二级 0xc4b5/0xcd1a/ 0xf04c
            0xc4b7 # 行业一二级 0xc4b7
            0xdffb # 地域
            0xD385 # 国内外重要指数
            0xDB5E # 股指期货
            0xCBBE # 科创板
            0xCBBD #blockDataFromBlockServer(
            0xD2 # 全部指数
            0xCE3F # 上证系列指数
            0xCE3E # 深证系列指数
            0xCE3D # 中证系列指数
            0xC2B0 # 北证系列指数
            0xCFF3 # ETF基金
            0x6 # 沪深封闭式基金
            0x4 # 沪封闭式基金
            0x5 # 深封闭式基金
            0xEF8C # LOF基金
            0xD811 # 分级基金
            0xD90C # T+0 基金
            0xC7B1 # 沪REITs
            0xC7A0 # 深REITs
            0xC89C # 沪深REITs
            0xCE14 # 可转债
            0xCE17 # 国债
            0xCE0B # 上证债券
            0xCE0A # 深证债券
            0xCE12 # 回购
            0xCE11 # 贴债
            0xCE16 # 地方债
            0xCE15 # 企业债
            0xD8D4 # 小公募
        :return: 包含成分股信息的 Reply 对象。
        """
        if not block_id:
            raise ValueError("Block Id must be provided.")

        if 'addr' in self.ops:
            addr = self.ops['addr']
            if addr != block_addr:
                raise ValueError("Block data can only be queried from block server.")

        req = f"id=7&instance={self.share_instance}&zipversion={self.zip_version}&sortbegin=0&sortcount=0&sortorder=D&sortid=55&blockid={block_id:x}&reqflag=blockserver"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No sector components data found.")

        reply = Reply(response)
        reply.convert_data()

        return reply

    @login_required
    def get_block_components(self, block_code: str):
        """
        获取板块成分股数据

        :param block_code: 板块代码 eg:URFI881273
        :return:
        """
        if not block_code:
            raise ValueError("Block code must be provided.")

        req = f"id=7&instance={self.share_instance}&zipversion={self.zip_version}&sortbegin=0&sortcount=0&sortorder=D&sortid=55&linkcode={block_code}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No sector components data found.")

        reply = Reply(response)
        reply.convert_data()

        return reply

    @login_required
    def get_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票3秒tick成交数据
        :param code: 股票代码
        :param start: 时间戳/倒序
        :param end: 时间戳/倒序
        :return:  Reply 对象。
        """

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,5,10,12,18,49"
        market = code[:4]
        short_code = code[4:]
        req = f"id=205&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}&TraceDetail=0"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Reply(response)
        reply.convert_data()

        return reply

    @login_required
    def get_super_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票3秒超级盘口数据，带委托档位
        :param code: 股票代码
        :param start: 时间戳
        :param end: 时间戳
        :return:  Reply 对象。
        """
        if start >= end:
            raise ValueError("Start timestamp must be less than end timestamp.")

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,5,7,10,12,13,14,18,19,20,21,25,26,27,28,29,31,32,33,34,35,49,69,70,92,123,125,150,151,152,153,154,155,156,157,45,66,661,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,123,125"
        market = code[:4]
        short_code = code[4:]
        req = f"id=205&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}&TraceDetail=0"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Reply(response)
        reply.convert_data()

        return reply

    @login_required
    def get_l2_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票l2成交数据

        :param code: 股票代码
        :param start: 时间戳
        :param end: 时间戳
        :return:  Reply 对象。
        """

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "5,10,12,13"
        market = code[:4]
        short_code = code[4:]
        req = f"id=220&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Reply(response)
        reply.convert_data()

        return reply

    def query_ths_industry(self):
        """
        获取行业板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE5F)

    def query_ths_sub_industry(self):
        """
        获取细分三级行业板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xc4b5)

    def query_ths_concept(self):
        """
        获取概念板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE5E)

    def query_ths_bond(self):
        """
        获取可转债板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE14)

    def query_ths_index(self):
        """
        获取指数板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xD2)

    def query_ths_etf(self):
        """
        获取ETF板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCFF3)

    def query_ths_etf_t0(self):
        """
        获取ETF T0板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xD90C)

    @login_required
    def query_data(self, req: str, ):
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Reply(response)
        reply.convert_data()

        return reply


class ZhuThsQuote(ThsQuote):
    """
        ZhuThsQuote 主行情数据
        """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', zhu_addr)
        super().__init__(ops)


class FuThsQuote(ThsQuote):
    """
    FuThsQuote 副行情数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', fu_addr)
        super().__init__(ops)


class InfoThsQuote(ThsQuote):
    """
    InfoThsQuote 获取资讯信息类型数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', info_addr)
        super().__init__(ops)


class BlockThsQuote(ThsQuote):
    """
    BlockThsQuote 获取板块类型数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', block_addr)
        super().__init__(ops)
