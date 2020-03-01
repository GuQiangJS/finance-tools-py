from finance_tools_py.parameters import DEFAULT_VALUE
from finance_tools_py.parameters import MARKET_TYPE
from finance_tools_py.parameters import ORDER_DIRECTION
from finance_tools_py.parameters import ORDER_STATUS
from finance_tools_py.util import Random
import pandas as pd
import numpy as np

class Order():
    """单次交易记录

    Attributes:
        code (str): 交易代码。一般为证券代码。
        price (float): 成交价格。
        date (datetime): 成交时间。
        amount (int): 成交数量。
        direction: 交易方向。默认为买入。
        market_type: 交易账户类型。默认为中国股票。
        commission_coeff (float): 交易手续费率。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.COMMISSION_COEFF`。
        min_commisssion_coeff (float): 交易手续费率最小值。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.MIN_COMMISSION_COEFF`。
        tax_coeff (float): 印花税费率。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.TAX_COEFF`。
        order_id (str) : 订单ID。订单的唯一编号。默认调用 :py:func:`finance_tools_py.util.Random.random_with_topic` 生成随机值。
    """

    def __init__(self,
                 code,
                 price,
                 date,
                 amount,
                 direction=ORDER_DIRECTION.BUY,
                 market_type=MARKET_TYPE.STOCK_CN,
                 commission_coeff=DEFAULT_VALUE.COMMISSION_COEFF,
                 min_commisssion_coeff=DEFAULT_VALUE.MIN_COMMISSION_COEFF,
                 tax_coeff=DEFAULT_VALUE.TAX_COEFF,
                 order_id=None):
        """初始化交易。默认交易状态为 `ORDER_STATUS.SUCCESS`。

        当前这个类的作用只作为交易记录用。所以默认认为所有的交易都是成功的。

        Args:
            code (str): 交易代码。一般为证券代码。
            price (float): 成交价格。
            date (datetime): 成交时间。
            amount (int): 成交数量。
            direction: 交易方向。默认为买入。
            market_type: 交易账户类型。默认为中国股票。
            commission_coeff (float): 交易手续费率。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.COMMISSION_COEFF`。
            min_commisssion_coeff (float): 交易手续费率最小值。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.MIN_COMMISSION_COEFF`。
            tax_coeff (float): 印花税费率。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.TAX_COEFF`。
            order_id (str) : 订单ID。订单的唯一编号。默认调用 :py:func:`finance_tools_py.util.Random.random_with_topic` 生成随机值。
        """

        self.code = code
        self.amount = amount
        self.date = date
        self.price = price
        self.direction = direction
        self.market_type = market_type
        self._status = ORDER_STATUS.SUCCESS
        self.commission_coeff = commission_coeff
        self.min_commisssion_coeff = min_commisssion_coeff
        self.tax_coeff = tax_coeff
        self.order_id = Random.random_with_topic() if not order_id else order_id

    @property
    def __dict__(self):
        return {
            'code': self.code,
            'price': self.price,
            'date': self.date,
            'amount': self.amount,
            'direction': self.direction,
            'market_type': self.market_type,
        }

    @property
    def total_money(self):
        """总发生金额"""
        return self.price * self.amount + self.calc_commission() + self.calc_tax()

    def calc_tax(self, trade_price=None, trade_amount=None):
        """

        Args:
            trade_price: 成交金额。默认取当前订单中的成交价格。
            trade_amount: 成交数量。默认取当前订单中的成交数量。

        Returns:
            float: 印花税。
        """
        if not trade_price:
            trade_price = self.price
        if not trade_amount:
            trade_amount = self.amount
        if self.market_type == MARKET_TYPE.STOCK_CN:
            return trade_amount * trade_price * self.tax_coeff
        else:
            raise NotImplementedError("暂不支持其他类型的印花税计算。")

    def calc_commission(self, trade_price=None, trade_amount=None):
        """计算佣金

        Args:
            trade_price (float): 成交金额。默认取当前订单中的成交价格。
            trade_amount (int): 成交数量。默认取当前订单中的成交数量。

        Returns:
            float: 佣金。
        """
        if not trade_price:
            trade_price = self.price
        if not trade_amount:
            trade_amount = self.amount
        if self.market_type == MARKET_TYPE.STOCK_CN:
            commission_fee = trade_price * trade_amount * self.commission_coeff
            return max(commission_fee, self.min_commisssion_coeff)
        else:
            raise NotImplementedError("暂不支持其他类型的交易佣金计算。")

    @property
    def status(self):
        return self._status

    def __repr__(self):
        return '< Order datetime:{} code:{} direction:{} price:{} amount:{}'.format(
            self.date, self.code, self.direction, self.price, self.amount
        )

    def to_dict(self):
        """转换为字典类型

        Returns:
            dict:
        """
        return vars(self)

    def to_df(self):
        """转换为 :py:class: `pandas.DataFrame` 类型对象

        Returns:
            :py:class: `pandas.DataFrame`
        """
        return pd.DataFrame([
            vars(self),
        ])

    def from_dict(self, d: dict):
        self.price = d['price']
        self.date = d['date']
        self.amount = d['amount']
        self.direction = d['direction']
        self.code = d['code']
        self.market_type = d['market_type']


class OrderQueue():
    """交易队列"""

    def __init__(self):
        self.order_list = {}

    def insert_order(self, order: Order):
        """将交易插入成交队列或更新队列中的交易

        Args:
            order (py:class:: finance_tools_py.order.Order): 订单

        """
        if order:
            self.order_list[order.order_id] = order

    @property
    def total_commission(self):
        """总手续费

        Returns:
            float
        """
        return np.array([x.calc_commission() for x in self.order_list.values()]).sum()

    @property
    def total_tax(self):
        """总印花税

        Returns:
            float
        """
        try:
            return np.array([x.calc_tax() for x in self.order_list.values()]).sum()
        except:
            return 0

    @property
    def order_ids(self):
        return list(self.order_list.keys())

    @property
    def len(self):
        return len(self.order_list)

    def to_df(self):
        """转换为 :py:class: `pandas.DataFrame` 类型对象

        Returns:
            :py:class: `pandas.DataFrame`
        """
        try:
            return pd.concat([x.to_df() for x in self.order_list.values()])
        except:
            pass

    def to_dict(self):
        return vars(self.order_list)

    def from_dict(self, d):
        self.order_list = d
