from finance_tools_py.order import OrderQueue
from finance_tools_py.parameters import DEFAULT_VALUE
from finance_tools_py.parameters import MARKET_TYPE
import pandas as pd
import copy

class _Account():
    """账户类"""
    pass


class StockAccount(_Account):
    """股票账户类

    Attributes:
        market_type: 交易账户类型。默认为中国股票。
        init_cash(float) : 初始化资金。默认为100000。
        cash_available (float): 可用资金。
        history (:py:class: `finance_tools_py.order.OrderQueue`): 交易历史。
        init_hold: 初始化股票持仓。默认为空。
        commission_coeff (float): 交易佣金。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.COMMISSION_COEFF`。
        min_commission_coeff (float): 最低交易佣金。默认为 :py:attribue:`finance_tools_py.parameters.DEFAULT_VALUE.MIN_COMMISSION_COEFF`。
        tax_coeff (float): 印花税。默认为 :py:attribue:`finance_tools_py.parameters.DEFAULT_VALUE.TAX_COEFF`。
    """

    def __init__(self,
                 market_type=MARKET_TYPE.STOCK_CN,
                 init_cash=100000,
                 init_hold={},
                 commission_coeff=DEFAULT_VALUE.COMMISSION_COEFF,
                 min_commission_coeff=DEFAULT_VALUE.MIN_COMMISSION_COEFF,
                 tax_coeff=DEFAULT_VALUE.TAX_COEFF):
        """

        Args:
            market_type: 交易账户类型。默认为中国股票。
            init_cash: 初始化资金。默认为100000。
            init_hold: 初始化股票持仓。默认为空。类似 {'000001':100}。
            commission_coeff (float): 交易佣金。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.COMMISSION_COEFF`。
            min_commission_coeff (float): 最低交易佣金。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.MIN_COMMISSION_COEFF`。
            tax_coeff (float): 印花税。默认为 :py:attr:`finance_tools_py.parameters.DEFAULT_VALUE.TAX_COEFF`。
        """
        self.init_cash = init_cash
        self.init_hold = init_hold
        self.market_type = market_type
        self.commission_coeff = commission_coeff
        self.min_commission_coeff = min_commission_coeff
        self.tax_coeff = tax_coeff
        self.history = OrderQueue()  # 历史交易记录
        self._cash = [self.init_cash] # 资金记录列表
        self.init_hold = pd.Series(
            init_hold,
            name='amount'
        ) if isinstance(init_hold,
                        dict) else init_hold
        self.init_hold.index.name = 'code'
        self.sell_available = copy.deepcopy(self.init_hold)
        self.buy_available = copy.deepcopy(self.init_hold)

    @property
    def cash_available(self):
        """当前可用资金

        Returns:
            float:
        """
        self._cash[-1]

    @property
    def freecash_precent(self):
        """剩余资金比率

        Returns:
            float
        """
        return self.cash_available / self.init_cash

    @property
    def total_commission(self):
        """总手续费

        Returns:
            float
        """
        return self.history.total_commission

    @property
    def total_tax(self):
        """总手续费

        Returns:
            float
        """
        return self.history.total_tax
