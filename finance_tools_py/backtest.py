import numpy as np
import pandas as pd
import datetime
import abc
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import logging
import statistics


class CallBack():
    """回测时的回调。"""
    def __init__(self):
        pass

    @abc.abstractmethod
    def on_check_buy(self, date: datetime.datetime.timestamp, code: str,
                     price: float, cash: float, **kwargs) -> bool:
        """检查是否需要买入。

        Args:
            date: 检查时间。
            code: 股票代码。
            price: 当前价格。
            cash: 持有现金。
            row: 当前处理的数据行。参见 :py:func:`pandas.DataFrame.iterrows` 方法。

        Returns:
            bool: 是否买入。返回 `False`。
        """
        return False

    @abc.abstractmethod
    def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
                      price: float, cash: float, hold_amount: float,
                      hold_price: float, **kwargs) -> bool:
        """检查是否需要卖出。

        Args:
            date: 检查时间。
            code: 股票代码。
            price: 当前价格。
            cash: 持有现金。
            hold_amount: 当前持仓数量。
            hold_price: 当前持仓成本。
            row: 当前处理的数据行。参见 :py:func:`pandas.DataFrame.iterrows` 方法。

        Returns:
            bool: 是否卖出。返回 `False`。
        """
        return False

    @abc.abstractmethod
    def on_calc_buy_amount(self, date: datetime.datetime.timestamp, code: str,
                           price: float, cash: float, **kwargs) -> float:
        """计算买入数量

        Args:
            date: 当前时间。
            code: 股票代码。
            price: 当前价格。
            cash: 持有现金。
            row: 当前处理的数据行。参见 :py:func:`pandas.DataFrame.iterrows` 方法。

        Return:
            float: 返回买入数量。返回 `0`。
        """
        return 0

    @abc.abstractmethod
    def on_calc_sell_amount(self, date: datetime.datetime.timestamp, code: str,
                            price: float, cash: float, hold_amount: float,
                            hold_price: float, **kwargs) -> float:
        """计算卖出数量

        Args:
            date: 当前时间。
            code: 股票代码。
            price: 当前价格。
            cash: 持有现金。
            hold_amount: 当前持仓数量。
            hold_price: 当前持仓成本。
            row: 当前处理的数据行。参见 :py:func:`pandas.DataFrame.iterrows` 方法。

        Return:
            float: 返回卖出数量。返回 `0`。
        """
        return 0

    def on_buy_sell_on_same_day(self, date, code, price, **kwargs):
        """同一天出现买入和卖出信号时的操作

        可能由于止盈/止损或其他自定义事件，造成了买卖同天
        """
        if kwargs.get('verbose', 0) == 2:
            print('{:%Y-%m-%d}-{}-同天买卖.买入价格:{:.2f},卖出价格:{:.2f}.'.format(
                date, code, kwargs.pop('buy_price', -1),
                kwargs.pop('sell_price', -1)))


class MinAmountChecker(CallBack):
    """每次买入和卖出数量都是最小数量（数量为 `min_amount` 定义）的回调。

    Attributes:
        buy_dict ({str,[datetime.datetime]}): 购买日期字典。key值为股票代码，value值为日期集合。
        sell_dict ({str,[datetime.datetime]}): 卖出日期字典。key值为股票代码，value值为日期集合。
        tax_coeff (float): 印花税费率。默认为 `0.001` 。
        commission_coeff (float): 手续费费率。默认为 `0.001` 。
        min_commission (float): 最小手续费费率。默认为 `5` 。
        min_amount (dict): 每次交易最小交易数量。。
    """
    def __init__(self, buy_dict={}, sell_dict={}, **kwargs):
        """初始化

        Args:
            buy_dict ({str,[datetime.datetime]}): 购买日期字典。key值为股票代码，value值为日期集合。
            sell_dict ({str,[datetime.datetime]}): 卖出日期字典。key值为股票代码，value值为日期集合。
            tax_coeff (float): 印花税费率。默认为 `0.001` 。
            commission_coeff (float): 手续费费率。默认为 `0.001` 。
            min_commission (float): 最小手续费费率。默认为 `5` 。
            min_amount (dict): 每次交易最小交易数量。。

        Example:
            直接传入日期字典

            >>> from datetime import date
            >>> import pandas as pd
            >>> data = pd.DataFrame({'code': ['1234' for x in range(3)],
            >>>                      'date': [date(1998, 1, 1),date(1999, 1, 1),date(2000, 1, 1)],
            >>>                      'close': [4.5, 7.9, 6.7]})
            >>> MinAmountChecker(buy_dict={'1234':[date(1998, 1, 1)]},
            >>>                 sell_dict={'1234':[date(2000, 1, 1)]})

            对于日期字典的处理。当准备直接使用 `Series` 类型对象时，可以使用 `to_pydatetime` 方法转换日期值。

            >>> from datetime import date
            >>> import pandas as pd
            >>> data = pd.DataFrame({'code': ['1234' for x in range(3)],
            >>>                      'date': [date(1998, 1, 1),date(1999, 1, 1),date(2000, 1, 1)],
            >>>                      'close': [4.5, 7.9, 6.7]})
            >>> MinAmountChecker(buy_dict={'1234':data[data['date'] < '1999-1-1']['date'].dt.to_pydatetime()},
            >>>                 sell_dict={'1234':data[data['date'] > '1999-1-1']['date'].dt.to_pydatetime()})

        """
        self.buy_dict = buy_dict
        self.sell_dict = sell_dict
        self.tax_coeff = kwargs.pop('tax_coeff', 0.001)
        self.commission_coeff = kwargs.pop('commission_coeff', 0.001)
        self.min_commission = kwargs.pop('min_commission', 5)
        self._min_amount = kwargs.pop('min_amount', {})

    def min_amount(self, code):
        """最小购买量，默认为100"""
        result = None
        if self._min_amount and code in self._min_amount:
            result = self._min_amount[code]
        return result if result else 100

    def on_check_buy(self, date: datetime.datetime.timestamp, code: str,
                     price: float, cash: float, **kwargs) -> bool:
        """当 `date` 及 `code` 包含在参数 :py:attr:`buy_dict` 中时返回 `True` 。否则返回 `False` 。"""
        if code in self.buy_dict.keys() and date in self.buy_dict[code]:
            return True
        else:
            return False

    def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
                      price: float, cash: float, hold_amount: float,
                      hold_price: float, **kwargs) -> bool:
        """当 `date` 及 `code` 包含在参数 :py:attr:`sell_dict` 中时返回 `True` 。否则返回 `False` 。"""
        if code in self.sell_dict.keys() and date in self.sell_dict[code]:
            return True
        else:
            return False

    def _calc_commission(self, price: float, amount: int) -> float:
        """计算交易手续费"""
        return max(price * amount * self.commission_coeff, self.min_commission)

    def _calc_tax(self, price: float, amount: int) -> float:
        """计算印花税"""
        return price * amount * self.tax_coeff

    def on_calc_buy_amount(self, date: datetime.datetime.timestamp, code: str,
                           price: float, cash: float, **kwargs) -> float:
        """计算买入数量。当交易实际花费金额小于 `cash` （可用现金） 时，返回参数 :py:attr: `min_amount` （每次交易数量）。"""
        amount = self.min_amount(code)
        if price * amount + self._calc_commission(
                price, amount) + self._calc_tax(price, amount) <= cash:
            return amount
        return 0

    def on_calc_sell_amount(self, date: datetime.datetime.timestamp, code: str,
                            price: float, cash: float, hold_amount: float,
                            hold_price: float, **kwargs) -> float:
        """计算卖出数量。
            当 `hold_amount` （当前可用持仓） 大于等于参数 :py:attr:`min_amount` （每次交易数量）时返回参数 :py:attr:`min_amount`（每次交易数量）。
            否则返回 `0`。"""
        if hold_amount >= self.min_amount(code):
            return self.min_amount(code)
        return 0


class AllInChecker(MinAmountChecker):
    """全部资金进入及全部持仓卖出的回调"""
    def on_calc_buy_amount(self, date: datetime.datetime.timestamp, code: str,
                           price: float, cash: float, **kwargs) -> float:
        """计算买入数量。
            根据 `cash` （可用现金）及 `price` （当前价格）计算实际可以买入的数量（参数 :py:attr: `min_amount` 的倍数）
            （计算时包含考虑了交易时可能产生的印花税和手续费）
        """
        amount = self.min_amount(code)
        while price * amount + self._calc_commission(
                price, amount) + self._calc_tax(price, amount) <= cash:
            amount = amount + self.min_amount(code)
        amount = amount - self.min_amount(code)
        return amount

    def on_calc_sell_amount(self, date: datetime.datetime.timestamp, code: str,
                            price: float, cash: float, hold_amount: float,
                            hold_price: float, **kwargs) -> float:
        """计算买入数量
        直接返回 `hold_amount` 。表示全部可以卖出。"""
        return hold_amount


class TurtleStrategy(MinAmountChecker):
    """海龟交易法则适用的交易策略。可以计算止盈/止损/加仓的价位，并且按照这些价位进行仓位控制。
    """
    class Hold():
        """持仓记录

        Attributes:
            symbol: 股票代码。
            date: 买入日期。
            price: 买入价格。
            amount: 买入数量。
            stoploss_price: 止损价格。
            stopprofit_price: 止盈价格。
            next_price: 加仓价位。
        """
        def __init__(self, symbol, date, price, amount, stoploss_price,
                     stopprofit_price, next_price):
            """
            Args:
                symbol: 股票代码。
                date: 买入日期。
                price: 买入价格。
                amount: 买入数量。
                stoploss_price: 止损价格。
                stopprofit_price: 止盈价格。
                next_price: 加仓价位。
            """
            self.symbol = symbol
            self.date = date
            self.price = price
            self.amount = amount
            self.stoploss_price = stoploss_price
            self.stopprofit_price = stopprofit_price
            self.next_price = next_price

        def __str__(self):
            return '{}-{:%Y-%m-%d}:价格:{:.2f},数量:{:.2f},止损价格:{:.2f},止盈价格:{:.2f},下一个仓位价格:{:.2f}'.format(
                self.symbol, self.date, self.price, self.amount,
                self.stoploss_price, self.stopprofit_price, self.next_price)

    def __init__(self,
                 colname,
                 buy_dict={},
                 sell_dict={},
                 max_amount={},
                 **kwargs):
        """构造函数

        Args:
            buy_dict:
            sell_dict:
            colname (str): 计算止盈/止损/加仓等价格的列名。调用时会尝试从参数`row`中找到这个数值。
            stoploss_point (float): 止损点。根据`colname`指定的数据进行计算。默认为2。设置为None时，表示不计算。
                计算止损价格`stoploss_price=price-stoploss_point*row[colname]`。
            stopprofit_point (float): 止盈点。根据`colname`指定的数据进行计算。默认为10。设置为None时，表示不计算。
                计算止损价格`stopprofit_price=price+stoploss_point*row[colname]`。
            next_point (float): 下一个可买点。根据`colname`指定的数据进行计算。默认为1。设置为None时，表示不计算。
                计算下一个可买点`next_price=price+next_point*row[colname]`。
            max_amount (dict): 最大持仓数量。默认为400。
            holds (dict): 初始持仓。{symbol:[:py:class:`TurtleStrategy.Hold`]}
            update_price_onsameday (float): 当买卖在同天发生时，是否允许更新最后一笔持仓的止盈价及下一个可买价。
            max_days (int): 最大持仓天数。默认为0。表示不判断。
        """
        super().__init__(buy_dict, sell_dict, **kwargs)
        self.colname = colname
        self.stoploss_point = kwargs.pop('stoploss_point', 2)
        self.stopprofit_point = kwargs.pop('stopprofit_point', 10)
        self.next_point = kwargs.pop('next_point', 1)
        self._max_amount = max_amount
        self.holds = kwargs.pop('holds', {})
        self.update_price_onsameday = kwargs.pop('update_price_onsameday',
                                                 True)
        self.max_days = kwargs.pop('max_days', 0)
        self._max_days_timedelta = datetime.timedelta(
            days=self.max_days) if self.max_days > 0 else None

    def _add_hold(self, symbol, date, price, amount, stoploss_price,
                  stopprofit_price, next_price):
        """记录新增持仓"""
        if symbol not in self.holds:
            self.holds[symbol] = []
        self.holds[symbol].append(
            TurtleStrategy.Hold(symbol, date, price, amount, stoploss_price,
                                stopprofit_price, next_price))

    def max_amount(self, code):
        return (self._max_amount[code] if self._max_amount
                and code in self._max_amount else self.min_amount(code) * 4)

    def on_check_buy(self, date, code, price, cash, **kwargs):
        result = super().on_check_buy(date, code, price, cash, **kwargs)
        verbose = kwargs.get('verbose', 0)
        if result and code in self.holds and len(self.holds[code]) > 0:
            hold = self.holds[code][-1]
            if hold and hold.next_price > 0 and price < hold.next_price:
                if verbose == 2:
                    print(
                        '{:%Y-%m-%d}-{}-当前价位:{:.2f}小于上次购买价位:{:.2f}的下一个价位:{:.2f},不再购买.当前持仓数量:{}'
                        .format(date, code, price, hold.price, hold.next_price,
                                sum(h.amount for h in self.holds[code])))
                return False
        h = sum([h.amount
                 for h in self.holds[code]]) if code in self.holds else 0
        if h >= self.max_amount(code):
            """超过最大持仓线时不再购买"""
            if verbose == 2:
                print('{:%Y-%m-%d}-{}-超过最大持仓线时不再购买.当前持仓数量:{}'.format(
                    date, code, h))
            return False
        return result

    def calc_price(self, price, **kwargs):
        '''计算止损/止盈价格

        Examples:
            >>> from finance_tools_py.backtest import TurtleStrategy
            >>> ts = TurtleStrategy(colname='atr5')
            >>> row = pd.Series({'atr5': 0.05})
            >>> ts.calc_price(1, row=row)
            (0.9, 1.5, 1.05)

        Returns:
            (float,float,float): 止损价，止盈价，加仓价
        '''
        row = kwargs.get('row', None)
        stoploss_price = -1
        stopprofit_price = -1
        next_price = -1
        if self.colname and not row.empty:
            v = row[self.colname]
            if v:
                if self.stoploss_point:
                    stoploss_price = price - self.stoploss_point * v
                if self.stopprofit_point:
                    stopprofit_price = price + self.stopprofit_point * v
                if self.next_point:
                    next_price = price + self.next_point * v
        return stoploss_price, stopprofit_price, next_price

    def _update_last_price(self, date, code, price, **kwargs):
        stoploss_price, stopprofit_price, next_price = self.calc_price(
            price, **kwargs)
        if stopprofit_price != -1:
            if kwargs.get('verbose', 0) == 2:
                print('{:%Y-%m-%d}-{}-同天买卖.更新止盈价:{:.2f}->{:.2f}.'.format(
                    date, code, self.holds[code][-1].stopprofit_price,
                    stopprofit_price))
            self.holds[code][-1].stopprofit_price = stopprofit_price
        if next_price != -1:
            if kwargs.get('verbose', 0) == 2:
                print('{:%Y-%m-%d}-{}-同天买卖.更新加仓价:{:.2f}->{:.2f}.'.format(
                    date, code, self.holds[code][-1].next_price, next_price))
            self.holds[code][-1].next_price = next_price

    def on_buy_sell_on_same_day(self, date, code, price, **kwargs):
        """同一天出现买入和卖出信号时的操作

        可能由于止盈/止损或其他自定义事件，造成了买卖同天
        """
        super().on_buy_sell_on_same_day(date, code, price, **kwargs)
        if self.update_price_onsameday:
            self._update_last_price(date, code, price, **kwargs)

    def on_calc_buy_amount(self, date, code, price, cash, **kwargs):
        """计算买入数量


        Args:
            date:
            code:
            price:
            cash:
            **kwargs:

        Returns:

        """
        result = super().on_calc_buy_amount(date, code, price, cash, **kwargs)
        if result:
            stoploss_price, stopprofit_price, next_price = self.calc_price(
                price, **kwargs)
            self._add_hold(code, date, price, result, stoploss_price,
                           stopprofit_price, next_price)
        return result

    def on_calc_sell_amount(self, date, code, price, cash, hold_amount,
                            hold_price, **kwargs):
        if code in self.holds:
            result = 0
            for h in reversed(self.holds[code]):
                if h.stoploss_price >= price:
                    result = result + h.amount
                    self.holds[code].remove(h)
            if result > 0:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-止损.止损数量:{},当前金额:{:.2f},持仓金额:{:.2f}'.
                          format(date, code, result, price, hold_price))
                return result
            for h in reversed(self.holds[code]):
                if h.stopprofit_price <= price:
                    result = result + h.amount
                    self.holds[code].remove(h)
            if result > 0:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-止盈.止盈数量:{},当前金额:{:.2f},持仓金额:{:.2f}'.
                          format(date, code, result, price, hold_price))
                return result
            hs = self._get_overdue(code, date)
            if hs:
                result = sum([h.amount for h in hs])
                if result > 0:
                    for h in hs:
                        if  kwargs.get('verbose', 0) == 2:
                            print(
                            '{:%Y-%m-%d}-{}-达到持仓期限.{}Days,购买日期:{:%Y-%m-%d},数量:{},当前金额:{:.2f},持仓金额:{:.2f}'
                            .format(date, code, self.max_days, h.date,
                                    h.amount, price, h.price))
                        self.holds[code].remove(h)
                return result
        result = super().on_calc_sell_amount(date, code, price, cash,
                                             hold_amount, hold_price, **kwargs)
        result_temp = result
        while result_temp > 0:
            if result_temp >= self.holds[code][0].amount:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-正常卖出.数量:{},当前金额:{:.2f},持仓金额:{:.2f}'.
                          format(date, code, self.holds[code][0].amount, price,
                                 self.holds[code][0].price))
                a = self.holds[code][0]
                result_temp = result_temp - a.amount
                self.holds[code].remove(a)
            else:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-正常卖出.数量:{},当前金额:{:.2f},持仓金额:{:.2f}'.
                          format(date, code, self.holds[code][0].amount, price,
                                 self.holds[code][0].price))
                self.holds[code][
                    0].amount = self.holds[code][0].amount - result_temp
                result_temp = 0
        return result

    def on_check_sell(self, date, code, price, cash, hold_amount, hold_price,
                      **kwargs):
        result = super().on_check_sell(date, code, price, cash, hold_amount,
                                       hold_price, **kwargs)
        if not result and code in self.holds:
            result = sum([
                h.amount for h in self.holds[code]
                if h.stoploss_price != -1 and h.stoploss_price >= price
            ])
            if result:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-触及止损线.当前可卖数量:{}.'.format(
                    date, code, result))
                return True
            result = sum([
                h.amount for h in self.holds[code]
                if h.stopprofit_price != -1 and h.stopprofit_price <= price
            ])
            if result:
                if kwargs.get('verbose', 0) == 2:
                    print('{:%Y-%m-%d}-{}-触及止盈线.当前可卖数量:{}.'.format(
                    date, code, result))
                return True
            if self._get_overdue(code, date):
                return True
        return result

    def _get_overdue(self, code, date):
        if self._max_days_timedelta and code in self.holds:
            return [
                h for h in self.holds[code]
                if (h.date + self._max_days_timedelta) <= date
            ]
        return None


class BackTest():
    """简单的回测系统。根据传入的购买日期和卖出日期，计算收益。

    Example:
        >>> from datetime import date
        >>> import pandas as pd
        >>> from finance_tools_py.backtest import BackTest
        >>> from finance_tools_py.backtest import MinAmountChecker
        >>> 
        >>> data = pd.DataFrame({
        >>>     'code': ['000001' for x in range(4)],
        >>>     'date': [date(1998, 1, 1), date(1999, 1, 1), date(2000, 1, 1), date(2001, 1, 1)],
        >>>     'close': [4.5, 7.9, 6.7, 10],
        >>> })
        >>> bt = BackTest(data, init_cash=1000, callbacks=[MinAmountChecker(
        >>>     buy_dict={'000001': [date(1998, 1, 1), date(2000, 1, 1)]},
        >>>     sell_dict={'000001': [date(1999, 1, 1)]})])
        >>> bt.calc_trade_history()
        >>> print(bt.report())
        数据时间:1998-01-01~2001-01-01（可交易天数4）
        初始资金:1000.00
        交易次数:3 (买入/卖出各算1次)
        可用资金:653.09
        当前持仓:code
        000001    (6.7, 100.0)
        当前总资产:1323.09
        资金变化率:65.31%
        资产变化率:132.31%
        总手续费:15.00
        总印花税:1.91
        交易历史：
             datetime    code  price  amount     cash  commission   tax   total  toward
        0  1998-01-01  000001    4.5     100   544.55           5  0.45  455.45       1
        1  1999-01-01  000001    7.9    -100  1328.76           5  0.79  795.79      -1
        2  2000-01-01  000001    6.7     100   653.09           5  0.67  675.67       1

    """
    def __init__(self,
                 data,
                 init_cash=10000,
                 tax_coeff=0.001,
                 commission_coeff=0.001,
                 min_commission=5,
                 col_name='close',
                 callbacks=[CallBack()],
                 **kwargs):
        """初始化

        Args:
            data (:py:class:`pandas.DataFrame`): 完整的日线数据。数据中需要包含 `date` 列，用来标记日期。
                数据中至少需要包含 `date` 列、 `code` 列和 `close` 列，其中 `close` 列可以由参数 `colname` 参数指定。
            init_cash (float): 初始资金。
            init_hold (:py:class:`pandas.DataFrame`): 初始持仓。
                数据中需要包含 'code', 'amount', 'price', 'buy_date', 'stoploss_price',
                'stopprofit_price', 'next_price' 列。
            tax_coeff (float): 印花税费率。默认0.001。
            commission_coeff (float): 手续费率。默认0.001。
            min_commission (float): 最小印花税费。默认5。
            live_start_date (date): 回测起始时间。默认为 data 中的第一行的 `date` 数据。
            col_name (str): 计算用的列名。默认为 `close` 。
                这个列名必须包含在参数 `data` 中。是用来进行回测计算的列，用来标记回测时使用的价格数据。
            callbacks ([:py:class:`finance_tools_py.backtest.CallBack`]): 回调函数集合。
        """
        self._min_buy_amount = 100  # 单次可买最小数量
        self.data = data
        self.init_cash = init_cash
        self.cash = [init_cash]  # 资金明细
        self.tax_coeff = tax_coeff
        self.commission_coeff = commission_coeff
        self.min_commission = min_commission
        self.history = []  # 交易历史
        self._init_hold = kwargs.pop(
            'init_hold',
            pd.DataFrame(columns=[
                'code', 'amount', 'price', 'buy_date', 'stoploss_price',
                'stopprofit_price', 'next_price'
            ]))
        self._calced = False
        self._colname = col_name
        self._calbacks = callbacks
        self._buy_price_cur = {}  #购买成本。
        if not self._init_hold.empty:
            for index, row in self._init_hold.iterrows():
                self.__update_buy_price(row['buy_date'], row['code'],
                                        row['amount'], row['price'], 1)
        self._history_headers = [
            'datetime',  # 时间
            'code',  # 代码
            'price',  # 成交价
            'amount',  # 成交量
            'cash',  # 剩余现金
            'commission',  # 手续费
            'tax',  # 印花税
            'total',  # 总金额
            'toward',  # 方向
        ]
        self.__start_date = self.data.iloc[0]['date']  #数据起始日期
        self._live_start_date = kwargs.pop('live_start_date',
                                           self.__start_date)
        self._init_hold['datetime'] = self.__start_date + datetime.timedelta(
            days=-1)
        self._init_assets = self.init_cash + (
            (sum(self._init_hold['price'] * self._init_hold['amount']))
            if not self._init_hold.empty else 0)  #期初资产
        # self.hold_amount=[]#当前持仓数量
        # self.hold_price=[]#当前持仓金额

    @property
    def history_df(self):
        """获取成交历史的 :py:class:`pandas.DataFrame` 格式。"""
        if len(self.history) > 0:
            lens = len(self.history[0])
        else:
            lens = len(self._history_headers)

        his = pd.DataFrame(data=self.history,
                           columns=self._history_headers[:lens])
        hold = self._init_hold.reset_index().drop(columns=['index'])
        return his.append(hold).sort_values('datetime')

    @property
    def available_hold_df(self):
        """获取可用持仓

        Returns:
            :py:class:`pandas.Series`
        """
        return self.history_df.groupby('code').amount.sum().replace(
            0, np.nan).dropna().sort_index()

    # @property
    # def trade(self):
    #     """每次交易的pivot表
    #     Returns:
    #         pd.DataFrame
    #         此处的pivot_table一定要用np.sum
    #     """
    #
    #     return self.history_df.pivot_table(
    #         index=['datetime'],
    #         columns='code',
    #         values='amount',
    #         aggfunc=np.sum
    #     ).fillna(0).sort_index()

    @property
    def hold_price_cur_df(self):
        """当前持仓成本附加最新价格的 DataFrame 格式数据

        Examples:
            >>>
                    buy_price  amount  price_cur
            code
            000001       13.4   100.0       15.3

        Returns:
            :class:`pandas.DataFrame` : 结果数据
        """
        if self._hold_price_cur.empty:
            return pd.DataFrame(
                columns=['buy_price', 'amount', 'price_cur']).sort_index()
        d = self.data.sort_values('date')
        df = pd.DataFrame(self._hold_price_cur.values.tolist(),
                          columns=['buy_price', 'amount'],
                          index=self._hold_price_cur.index)
        df['price_cur'] = df.apply(
            lambda row: d.loc[d['code'] == row.name, 'close'].iloc[-1]
            if not d.loc[d['code'] == row.name, 'close'].empty else 0,
            axis=1)
        return df.sort_index()

    @property
    def _hold_price_cur(self):
        """目前持仓的成本。是 :py:class:`pandas.Series` 类型或 :py:class:`pandas.DataFrame` 类型。
            其中 `code` 是索引，通过索引访问会返回一个数组（price,amount）"""
        def weights(x):
            n = len(x)
            res = 1
            while res > 0 or res < 0:
                res = sum(x[:n]['amount'])
                n = n - 1

            x = x[n + 1:]

            if sum(x['amount']) != 0:
                return np.average(x['price'].to_list(),
                                  weights=x['amount'].to_list(),
                                  returned=True)
            else:
                return np.nan

        df = self.history_df.set_index('datetime')
        return df.sort_index().groupby('code').apply(weights).dropna()

    def hold_time(self, dt=None):
        """持仓时间。根据参数 `dt` 查询截止时间之前的交易，并与当前时间计算差异。

        Args:
            dt (datetime): 交易截止时间。如果为 `None` 则表示计算所有交易。默认为 `None` 。

        Returns:
            :py:class:`pandas.DataFrame`
        """
        def weights(x):
            if sum(x['amount']) != 0:
                return pd.Timestamp(
                    datetime.datetime.today()) - pd.to_datetime(
                        x.datetime.max())
            else:
                return np.nan

        if datetime is None:
            return self.history_df.set_index(
                'datetime', drop=False).sort_index().groupby('code').apply(
                    weights).dropna()
        else:
            return self.history_df.set_index(
                'datetime', drop=False).sort_index().loc[:dt].groupby(
                    'code').apply(weights).dropna()

    @property
    def total_assets_cur(self) -> float:
        """获取当前总资产

        当前可用资金+当前持仓现价。
        """
        if self.hold_price_cur_df.empty:
            return self.available_cash
        else:
            return self.available_cash + sum(
                self.hold_price_cur_df['amount'] *
                self.hold_price_cur_df['price_cur'])

    # def hold_table(self, datetime=None):
    #     """到某一个时刻的持仓 如果给的是日期,则返回当日开盘前的持仓"""
    #     if datetime is None:
    #         hold_available = self.history_df.set_index(
    #             'datetime'
    #         ).sort_index().groupby('code').amount.sum().sort_index()
    #     else:
    #         hold_available = self.history_df.set_index(
    #             'datetime'
    #         ).sort_index().loc[:datetime].groupby('code').amount.sum().sort_index()
    #
    #     return pd.concat([self._init_hold,
    #                       hold_available]).groupby('code').sum().sort_index(
    #     )

    @property
    def available_cash(self) -> float:
        """获取当前可用资金"""
        return self.cash[-1]

    def _calc_commission(self, price, amount) -> float:
        """计算交易手续费"""
        return max(price * amount * self.commission_coeff, self.min_commission)

    def _calc_tax(self, price, amount) -> float:
        """计算印花税"""
        return price * amount * self.tax_coeff

    def _check_callback_buy(self, date, code, price, **kwargs) -> bool:
        for cb in self._calbacks:
            if cb.on_check_buy(date, code, price, self.available_cash,
                               **kwargs):
                return True
        return False

    def _on_buy_sell_on_same_day(self, date, code, price, **kwargs):
        """同一天出现买入和卖出信号时的操作

        可能由于止盈/止损或其他自定义事件，造成了买卖同天
        """
        for cb in self._calbacks:
            cb.on_buy_sell_on_same_day(date, code, price, **kwargs)

    def __get_buy_avg_price(self, code):
        """当前买入平均成本

        Returns:
            (float,float): (成本,数量)
        """
        if code in self._buy_price_cur:
            hold_amount, hold_price = self._buy_price_cur[code]
            if hold_amount and hold_price:
                return np.average(hold_price,
                                  weights=hold_amount,
                                  returned=True)
        return (0.0, 0.0)

    # def __get_hold_price(self,code):
    #     pass

    def __update_buy_price(self, date, code, amount, price, toward):
        """更新买入成本"""
        if toward == 1:
            #买入
            hold_amount = []
            hold_price = []
            if code not in self._buy_price_cur:
                self._buy_price_cur[code] = [hold_amount, hold_price]
            else:
                hold_amount, hold_price = self._buy_price_cur[code]
            logging.debug(
                '__update_buy_price-{:%Y-%m-%d}:toward:{},code:{},amount:{},price:{:.2f}'
                .format(date, toward, code, amount, price))
            self._buy_price_cur[code] = [
                hold_amount + [amount], hold_price + [price]
            ]
        elif toward == -1:
            #卖出
            hold_amount = []
            hold_price = []
            if code not in self._buy_price_cur:
                self._buy_price_cur[code] = [hold_amount, hold_price]
            else:
                hold_amount, hold_price = self._buy_price_cur[code]

            while amount > 0:
                if amount >= hold_amount[0]:
                    logging.debug(
                        '__update_buy_price-{:%Y-%m-%d}:toward:{},code:{},amount:{},price:{:.2f},hold_amount:{}'
                        .format(date, toward, code, amount, price,
                                hold_amount))
                    a = hold_amount[0]
                    hold_amount.remove(a)
                    hold_price.remove(hold_price[0])
                    amount = amount - a
                else:
                    logging.debug(
                        '__update_buy_price:toward:{},code:{},amount:{},price:{:.2f}'
                        .format(toward, code, amount, price))
                    hold_amount[0] = hold_amount[0] - amount
                    amount = 0

    def _check_callback_sell(self, date, code, price, **kwargs) -> bool:
        for cb in self._calbacks:
            hold_price, hold_amount = self.__get_buy_avg_price(code)
            if cb.on_check_sell(date, code, price, self.available_cash,
                                hold_amount, hold_price, **kwargs):
                return True
        return False

    def _calc_buy_amount(self, date, code, price, **kwargs) -> float:
        for cb in self._calbacks:
            amount = cb.on_calc_buy_amount(date, code, price,
                                           self.available_cash, **kwargs)
            if amount:
                return amount
        return 0

    def _calc_sell_amount(self, date, code, price, **kwargs) -> float:
        for cb in self._calbacks:
            hold_price, hold_amount = self.__get_buy_avg_price(code)
            if hold_amount > 0:
                amount = cb.on_calc_sell_amount(date, code, price,
                                                self.available_cash,
                                                hold_amount, hold_price,
                                                **kwargs)
                if amount:
                    return amount
        return 0

    def calc_trade_history(self, verbose=0, **kwargs):
        """计算交易记录

        Args:
            verbose (int): 是否显示计算过程。0（不显示），1（显示部分），2（显示全部）。默认为0。
            bssd_buy (bool): 买卖发生在同一天，是否允许买入。默认False。
            bssd_sell (bool): 买卖发生在同一天，是否允许买入。默认False。

        """
        def update_history(history, date, code, price, amount, available_cash,
                           commission, tax, toward):
            history.append([
                date,  # 时间
                code,  # 代码
                price,  # 成交价
                amount * toward,  # 成交量
                available_cash,  # 剩余现金
                commission,  # 手续费
                tax,  # 印花税
                price * amount + commission + tax,  # 总金额
                toward,  # 方向
            ])

        _bssd_buy = kwargs.pop('bssd_buy', False)  #买卖发生在同一天，是否允许买入。默认False
        _bssd_sell = kwargs.pop('bssd_sell', False)  #买卖发生在同一天，是否允许卖出。默认False

        for index, row in tqdm(self.data.iterrows(),
                               total=len(self.data),
                               desc='回测计算中...'):
            date = row['date']
            if date < self._live_start_date:
                if verbose ==2:
                    print('{:%Y-%m-%d} < 起始日期:{:%Y-%m-%d} 跳过判断。'.format(
                        date, self._live_start_date))
                continue
            code = row['code']
            price = row['close']  # 价格
            _buy = self._check_callback_buy(date,
                                            code,
                                            price,
                                            row=row,
                                            verbose=verbose)
            _sell = self._check_callback_sell(date,
                                              code,
                                              price,
                                              row=row,
                                              verbose=verbose)
            if _buy and _sell:
                self._on_buy_sell_on_same_day(date,
                                              code,
                                              price,
                                              row=row,
                                              verbose=verbose)
                _buy = _bssd_buy
                _sell = _bssd_sell
                if verbose == 2:
                    print('{:%Y-%m-%d}-{}-同天买卖.允许买入:{},允许卖出:{}.'.format(
                        date, code, _bssd_buy, _bssd_sell))

            if _buy:
                amount = self._calc_buy_amount(date,
                                               code,
                                               price,
                                               row=row,
                                               verbose=verbose)  # 买入数量
                commission = self._calc_commission(price, amount)
                tax = self._calc_tax(price, amount)
                value = price * amount + commission + tax
                if value <= self.available_cash and amount > 0:
                    self.cash.append(self.available_cash - value)
                    update_history(
                        self.history,
                        date,
                        code,
                        price,
                        amount,
                        self.cash[-1],
                        commission,
                        tax,
                        1,
                    )
                    self.__update_buy_price(date, code, amount, price, 1)
                    if verbose ==2:
                        print('{:%Y-%m-%d} {} 买入 {:.2f}/{:.2f}，剩余资金 {:.2f}'.
                              format(date, code, price, amount,
                                     self.available_cash))
                else:
                    if verbose ==2:
                        print('{:%Y-%m-%d} {} {:.2f} 可用资金不足，跳过购买。'.format(
                            date, code, price))
            if _sell:
                amount = self._calc_sell_amount(date,
                                                code,
                                                price,
                                                row=row,
                                                verbose=verbose)
                if amount > 0:
                    commission = self._calc_commission(price, amount)
                    tax = self._calc_tax(price, amount)
                    value = price * amount - commission - tax
                    self.cash.append(self.available_cash + value)
                    update_history(
                        self.history,
                        date,
                        code,
                        price,
                        amount,
                        self.cash[-1],
                        commission,
                        tax,
                        -1,
                    )
                    self.__update_buy_price(date, code, amount, price, -1)
                    if verbose ==2:
                        print('{:%Y-%m-%d} {} 卖出 {:.2f}/{:.2f}，剩余资金 {:.2f}'.
                              format(date, code, price, amount,
                                     self.available_cash))
                else:
                    if verbose ==2:
                        print('{:%Y-%m-%d} {} 没有持仓，跳过卖出。'.format(date, code))
        if verbose ==2:
            print('计算完成！')
        self._calced = True

    def _calc_total_tax(self) -> float:
        return np.asarray(
            self.history).T[6].sum() if len(self.history) > 0 else 0

    def _calc_total_commission(self) -> float:
        return np.asarray(
            self.history).T[5].sum() if len(self.history) > 0 else 0

    def report(self, **kwargs):
        """获取计算结果

        Args:
            show_history (bool): 是否包含交易明细。默认为True。
            show_hold (bool): 是否包含当前持仓明细。默认为True。

        Returns:
            str: 返回计算结果。
        """
        result = ''
        if not self._calced:
            result = '没有经过计算。请先调用 `calc_trade_history` 方法进行计算。'
            return result
        result = '数据时间:{}~{}（可交易天数{}）'.format(self.data.iloc[0]['date'],
                                              self.data.iloc[-1]['date'],
                                              len(self.data['date'].unique()))
        result = result + '\n初始资金:{:.2f}'.format(self.init_cash)
        result = result + '\n期初资产:{:.2f}'.format(self._init_assets)
        result = result + '\n期末资产:{:.2f}(现金+持股现价值)'.format(
            self.total_assets_cur)
        result = result + '\n资产变化率:{:.2%}'.format(
            (self.total_assets_cur /
             self._init_assets) if self._init_assets != 0 else 0)
        result = result + '\n交易次数:{} (买入/卖出各算1次)'.format(len(self.history))
        result = result + '\n可用资金:{:.2f}'.format(self.available_cash)
        if kwargs.pop('show_hold', True):
            result = result + '\n当前持仓:'
            if not self.hold_price_cur_df.empty:
                result = result + self.hold_price_cur_df.to_string()
            else:
                result = result + '无'
        result = result + '\n资金变化率:{:.2%}'.format(
            self.available_cash / self.init_cash)
        result = result + '\n总手续费:{:.2f}'.format(self._calc_total_commission())
        result = result + '\n总印花税:{:.2f}'.format(self._calc_total_tax())
        if kwargs.pop('show_history', True):
            result = result + '\n交易历史：\n'
            result = result + self.history_df.sort_values(
                'datetime').to_string()
        return result

    def profit_loss_df(self):
        """按照 **先进先出** 的方式计算并返回 PNL（profit and loss）损益表

        Examples:
            >>> history_df
            code  amount  price    datetime
            0  000001     100    6.3  2020-04-11
            1  000001     200    5.4  2020-05-12
            2  000001    -200    7.1  2020-05-14
            3  000001    -100    4.3  2020-07-11
            >>> BackTest._pnl_fifo(history_df,[1])
                     buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
            code
            000001 2020-04-11 2020-05-14        6.3         7.1     100   0.126984       80.0  33 days
            000001 2020-05-12 2020-05-14        5.4         7.1     100   0.314815      170.0   2 days
            000001 2020-05-12 2020-07-11        5.4         4.3     100  -0.203704     -110.0  60 days

            >>> history_df
                 code  amount  price    datetime
            0  000001     100   6.30  2020-04-11
            1  000001     200   5.40  2020-05-12
            2  000002     400   3.30  2020-05-12
            3  000001    -200   7.10  2020-05-14
            4  000002    -200   3.51  2020-05-14
            5  000003     100   1.09  2020-07-11
            6  000001    -100   4.30  2020-07-11
            >>> BackTest._pnl_fifo(history_df, history_df.code.unique())
                     buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
            code
            000001 2020-04-11 2020-05-14        6.3        7.10     100   0.126984       80.0  33 days
            000001 2020-05-12 2020-05-14        5.4        7.10     100   0.314815      170.0   2 days
            000002 2020-05-12 2020-05-14        3.3        3.51     200   0.063636       42.0   2 days
            000001 2020-05-12 2020-07-11        5.4        4.30     100  -0.203704     -110.0  60 days
        """
        return BackTest._pnl_fifo(self.history_df,
                                  self.history_df.code.unique())

    @staticmethod
    def _pnl_fifo(history_df, code):
        """按照 **先进先出** 的方式计算并返回 PNL（profit and loss）损益表

        Examples:
            >>> history_df
            code  amount  price    datetime
            0  000001     100    6.3  2020-04-11
            1  000001     200    5.4  2020-05-12
            2  000001    -200    7.1  2020-05-14
            3  000001    -100    4.3  2020-07-11
            >>> BackTest._pnl_fifo(history_df,[1])
                     buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
            code
            000001 2020-04-11 2020-05-14        6.3         7.1     100   0.126984       80.0  33 days
            000001 2020-05-12 2020-05-14        5.4         7.1     100   0.314815      170.0   2 days
            000001 2020-05-12 2020-07-11        5.4         4.3     100  -0.203704     -110.0  60 days

            >>> history_df
                 code  amount  price    datetime
            0  000001     100   6.30  2020-04-11
            1  000001     200   5.40  2020-05-12
            2  000002     400   3.30  2020-05-12
            3  000001    -200   7.10  2020-05-14
            4  000002    -200   3.51  2020-05-14
            5  000003     100   1.09  2020-07-11
            6  000001    -100   4.30  2020-07-11
            >>> BackTest._pnl_fifo(history_df, history_df.code.unique())
                     buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
            code
            000001 2020-04-11 2020-05-14        6.3        7.10     100   0.126984       80.0  33 days
            000001 2020-05-12 2020-05-14        5.4        7.10     100   0.314815      170.0   2 days
            000002 2020-05-12 2020-05-14        3.3        3.51     200   0.063636       42.0   2 days
            000001 2020-05-12 2020-07-11        5.4        4.30     100  -0.203704     -110.0  60 days
        """
        from collections import deque
        X = dict(
            zip(code, [{
                'buy': deque(),
                'sell': deque()
            } for i in range(len(code))]))
        pair_table = []
        for _, data in history_df.iterrows():
            if abs(data.amount) < 1:
                pass
            else:
                while True:
                    if data.amount > 0:
                        X[data.code]['buy'].append(
                            (data.datetime, data.amount, data.price, 1))
                        break
                    elif data.amount < 0:
                        rawoffset = 'buy'
                        l = X[data.code][rawoffset].popleft()
                        if abs(l[1]) > abs(data.amount):
                            """
                            if raw> new_close:
                            """
                            temp = (l[0], l[1] + data.amount, l[2])
                            X[data.code][rawoffset].appendleft(temp)
                            if data.amount < 0:
                                pair_table.append([
                                    data.code, data.datetime, l[0],
                                    abs(data.amount), data.price, l[2],
                                    rawoffset
                                ])
                                break
                            else:
                                pair_table.append([
                                    data.code, l[0], data.datetime,
                                    abs(data.amount), l[2], data.price,
                                    rawoffset
                                ])
                                break

                        elif abs(l[1]) < abs(data.amount):
                            data.amount = data.amount + l[1]

                            if data.amount < 0:
                                pair_table.append([
                                    data.code, data.datetime, l[0], l[1],
                                    data.price, l[2], rawoffset
                                ])
                            else:
                                pair_table.append([
                                    data.code, l[0], data.datetime, l[1], l[2],
                                    data.price, rawoffset
                                ])
                        else:
                            if data.amount < 0:
                                pair_table.append([
                                    data.code, data.datetime, l[0],
                                    abs(data.amount), data.price, l[2],
                                    rawoffset
                                ])
                                break
                            else:
                                pair_table.append([
                                    data.code, l[0], data.datetime,
                                    abs(data.amount), l[2], data.price,
                                    rawoffset
                                ])
                                break
        pair_title = [
            'code', 'sell_date', 'buy_date', 'amount', 'sell_price',
            'buy_price', 'rawdirection'
        ]
        pnl = pd.DataFrame(pair_table, columns=pair_title)

        pnl = pnl.assign(
            # unit=1,
            pnl_ratio=(pnl.sell_price / pnl.buy_price) - 1,  #盈利比率
            sell_date=pd.to_datetime(pnl.sell_date),
            buy_date=pd.to_datetime(pnl.buy_date))
        pnl = pnl.assign(
            pnl_money=(pnl.sell_price - pnl.buy_price) * pnl.amount * 1,  #盈利金额
            hold_gap=abs(pnl.sell_date - pnl.buy_date),  #持仓时间
            # if_buyopen=pnl.rawdirection == 'buy'
        )
        # pnl = pnl.assign(
        #     openprice=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        #               pnl.buy_price +
        #               pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) * pnl.sell_price,
        #     opendate=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        #              pnl.buy_date.map(str) +
        #              pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        #              pnl.sell_date.map(str),
        #     closeprice=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        #                pnl.buy_price +
        #                pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) * pnl.sell_price,
        #     closedate=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        #               pnl.buy_date.map(str) +
        #               pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        #               pnl.sell_date.map(str)
        # )
        return pnl[[
            'code', 'buy_date', 'sell_date', 'buy_price', 'sell_price',
            'amount', 'pnl_ratio', 'pnl_money', 'hold_gap'
        ]].set_index('code')


class Utils():
    @staticmethod
    def plt_pnl(data, v, x, y, subplot_kws={}, line_kws={}, **kwargs):
        """绘制持仓图。会自动按照红色/绿色，区分盈亏。

        线形图的基础上叠加交易盈亏。

        Examples:
            >>> data
                    date  close
            0 2020-04-10   6.25
            1 2020-04-11   6.30
            2 2020-04-12   6.35
            3 2020-04-13   6.40
            4 2020-04-14   6.30
            5 2020-04-15   6.20
            6 2020-04-16   6.15
            7 2020-04-17   6.10
            >>> profit_df
                     buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
            code
            000001 2020-04-11 2020-04-13        6.3         6.4     100   0.015873       10.0   2 days
            000001 2020-04-15 2020-04-17        6.2         6.1     100  -0.016129      -10.0   2 days
            >>> Utils.plt_pnl(data=data,
                              v=profit_df,
                              x='date',
                              y='close',
                              subplot_kws={'title': 'test'},
                              line_kws={'c': 'b'})

        Args:
            data: 完整数据。
            v: 数据源。可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            x: data中的列名，用来绘制X轴。
            y: data中的列名，用来绘制Y轴。
            line_kws (dict): 绘制线性图时的参数。
            subplot_kws (dict): 绘制线性图时的参数。

        Returns:
            :py:class:`matplotlib.axes.Axes`:

        """
        d = Utils._get_profit_loss_df(v).copy()
        pnl_col = kwargs.pop('pnl_col', 'pnl_money')
        pnl_bd_col = kwargs.pop('pnl_bd_col', 'buy_date')
        pnl_sd_col = kwargs.pop('pnl_sd_col', 'sell_date')
        ax = kwargs.pop('ax', None)
        if ax is None:
            ax = plt.subplot(**subplot_kws)
        ax.plot(data[x], data[y], **line_kws)
        for i, r in d.iterrows():
            l = data[(data[x] <= r[pnl_sd_col]) & (data[x] >= r[pnl_bd_col])]
            plt.fill_between(l[x],
                             0,
                             l[y],
                             facecolor='r' if r[pnl_col] > 0 else 'g',
                             alpha=0.5)
        return ax

    @staticmethod
    def win_rate(v):
        """胜率

        盈利次数/总次数

        Examples:

        >>> profit_df
                 buy_date  sell_date  buy_price  sell_price  amount  pnl_ratio  pnl_money hold_gap
        code
        000001 2020-04-11 2020-05-14        6.3        7.10     100   0.126984       80.0  33 days
        000001 2020-05-12 2020-05-14        5.4        7.10     100   0.314815      170.0   2 days
        000002 2020-05-12 2020-05-14        3.3        3.51     200   0.063636       42.0   2 days
        000001 2020-05-12 2020-07-11        5.4        4.30     100  -0.203704     -110.0  60 days
        >>> Utils.win_rate(profit_df)
        0.75

        Args:
            v: 可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
        """
        data = Utils._get_profit_loss_df(v)
        try:
            return round(len(data.query('pnl_money>0')) / len(data), 2)
        except ZeroDivisionError:
            return 0

    @staticmethod
    def plt_win_rate(v, **kwargs):
        """按照饼图方式绘制胜率

        See Also:
            :py:func:`Utils.win_rate`

        Args:
            v: 数据源。可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            colors: 默认会自动按照红色/绿色，区分盈亏。

        Returns:
            :py:class:`matplotlib.axes.Axes`:

        """
        ax = kwargs.pop('ax', None)
        colors = kwargs.pop('colors', ['r', 'g'])
        if ax is None:
            ax = plt.subplot(**kwargs)
        rate = Utils.win_rate(v)
        ax.pie([rate, 1 - rate],
               labels=['盈利', '亏损'],
               colors=colors,
               autopct='%1.1f%%')
        return ax

    @staticmethod
    def _get_profit_loss_df(v):
        if isinstance(v, BackTest):
            return v.profit_loss_df()
        elif isinstance(v, pd.DataFrame):
            return v
        else:
            raise ValueError('不支持的类型')

    @staticmethod
    def plt_pnl_ratio(v, kind='bar', **kwargs):
        """画出 PNL（profit and loss）损益表中的比率。

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 数据源。可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            kind: 绘图类型。支持（`bar`或`scatter`）。默认为 `bar`。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        kind = kind.upper()
        if kind == 'BAR':
            return Utils._bar_pnl_ratio(v, **kwargs)
        elif kind == 'SCATTER':
            return Utils._scatter_pnl_ratio(v, **kwargs)

    @staticmethod
    def plt_pnl_money(v, kind='bar', **kwargs):
        """绘制 PNL（profit and loss）损益表中的金额.

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 数据源。可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            kind: 绘图类型。支持（`bar`或`scatter`）。默认为 `bar`。
            ax (:py:class:`matplotlib.axes.Axes`): 绘图对象。可以为None。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        kind = kind.upper()
        if kind == 'BAR':
            return Utils._bar_pnl_money(v, **kwargs)
        elif kind == 'SCATTER':
            return Utils._scatter_pnl_money(v, **kwargs)

    @staticmethod
    def _bar_pnl_ratio(v, **kwargs):
        """绘制pnl比率柱状图。会自动按照红色/绿色，区分盈亏。

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            ax (:py:class:`matplotlib.axes.Axes`): 绘图对象。可以为None。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        ax = kwargs.pop('ax', None)
        if ax is None:
            ax = plt.subplot(**kwargs)
        data = Utils._get_profit_loss_df(v).copy()
        data['c'] = 'g'
        data.loc[data['pnl_ratio'] > 0, 'c'] = 'r'
        data['sell_date'] = pd.to_datetime(data['sell_date'])
        ax.bar(x=data.sell_date.dt.strftime('%Y-%m-%d'),
               height=data.pnl_ratio,
               color=data['c'].values,
               **kwargs)
        return ax

    @staticmethod
    def _scatter_pnl_ratio(v, **kwargs):
        """绘制比率散点图。会自动按照红色/绿色，区分盈亏。

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            ax (:py:class:`matplotlib.axes.Axes`): 绘图对象。可以为None。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        ax = kwargs.pop('ax', None)
        if ax is None:
            ax = plt.subplot(**kwargs)
        data = Utils._get_profit_loss_df(v)
        data['c'] = 'g'
        data.loc[data['pnl_ratio'] > 0, 'c'] = 'r'
        data['sell_date'] = pd.to_datetime(data['sell_date'])
        ax.scatter(x=data.sell_date.dt.strftime('%Y-%m-%d'),
                   y=data.pnl_ratio,
                   color=data['c'].values,
                   **kwargs)
        return ax

    @staticmethod
    def _bar_pnl_money(v, **kwargs):
        """绘制pnl盈亏额柱状图。会自动按照红色/绿色，区分盈亏。

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            ax (:py:class:`matplotlib.axes.Axes`): 绘图对象。可以为None。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        ax = kwargs.pop('ax', None)
        if ax is None:
            ax = plt.subplot(**kwargs)
        data = Utils._get_profit_loss_df(v).copy()
        data['c'] = 'g'
        data.loc[data['pnl_ratio'] > 0, 'c'] = 'r'
        data['sell_date'] = pd.to_datetime(data['sell_date'])
        ax.bar(x=data.sell_date.dt.strftime('%Y-%m-%d'),
               height=data.pnl_money,
               color=data['c'].values,
               **kwargs)
        return ax

    @staticmethod
    def _scatter_pnl_money(v, **kwargs):
        """绘制pnl盈亏额散点图

        See Also:
            :py:func:`BackTest.profit_loss_df`

        Args:
            v: 可以接受 :py:class:`BackTest` 对象实例，也可以接受 :py:class:`pandas.DataFrame` 对象实例。
                如果传入 :py:class:`pandas.DataFrame` 时需要为 :py:func:`BackTest.profit_loss_df` 所返回的数据结构。
            ax (:py:class:`matplotlib.axes.Axes`): 绘图对象。可以为None。

        Returns:
            :py:class:`matplotlib.axes.Axes`:
        """
        ax = kwargs.pop('ax', None)
        if ax is None:
            ax = plt.subplot(**kwargs)
        data = Utils._get_profit_loss_df(v)
        data['sell_date'] = pd.to_datetime(data['sell_date'])
        ax.scatter(x=data.sell_date.dt.strftime('%Y-%m-%d'),
                   y=data.pnl_money,
                   **kwargs)
        return ax
