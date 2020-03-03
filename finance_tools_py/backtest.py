import numpy as np
import pandas as pd


class BackTest():
    """简单的回测系统。根据传入的购买日期和卖出日期，计算收益。

    Example:
        >>> from datetime import date
        >>> import pandas as pd
        >>> from finance_tools_py.backtest import BackTest
        >>> data=pd.DataFrame({
        >>>     'date':[date(1998,1,1),date(1999,1,1),date(2000,1,1),date(2001,1,1),date(2002,1,1)],
        >>>     'close':[4.5,7.9,6.7,13.4,15.3]
        >>> })
        >>> bt=BackTest(data)
        >>> buysignal=[date(1999,1,1),date(2001,1,1)]
        >>> sellsignal=[date(2000,1,1),date(2002,1,1)]
        >>> bt.calc_trade_history(buysignal,sellsignal)
        >>> bt.report()
        数据时间:1998-01-01~2002-01-01（可交易天数5）
        交易次数:4 (买入/卖出各算1次)
        当前持仓:0,可用资金:10045.67
        资金变化率:100.46%
        总手续费:20.00
        总印花税:4.33
        交易历史：
           amount  commission        date  price   tax    total towards
        0     100           5  1999-01-01    7.9  0.79   795.79     buy
        1     100           5  2000-01-01    6.7  0.67   664.33    sell
        2     100           5  2001-01-01   13.4  1.34  1346.34     buy
        3     100           5  2002-01-01   15.3  1.53  1523.47    sell

    """

    def __init__(self,
                 data,
                 init_cash=10000,
                 trade_amount=100,
                 tax_coeff=0.001,
                 commission_coeff=0.001,
                 min_commission=5,
                 col_name='close'):
        """初始化

        Args:
            data (:py:class:`pandas.DataFrame`): 完整的日线数据。数据中需要包含 `date` 列，用来标记日期。
                数据中至少需要包含 `date` 列和 `close` 列，其中 `close` 列可以由参数 `colname` 参数指定。
            init_cash (float): 初始资金。
            trade_amount (int): 每次交易数量。默认100。
            tax_coeff (float): 印花税费率。默认0.001。
            commission_coeff (float): 手续费率。默认0.001。
            min_commission (float): 最小印花税费。默认5。
            col_name (str): 计算用的列名。默认为 `close` 。
                这个列名必须包含在参数 `data` 中。是用来进行回测计算的列，用来标记回测时使用的价格数据。
        """
        self._min_buy_amount = 100  # 单次可买最小数量
        self.data = data
        self.init_cash = init_cash
        self.cash = [init_cash]  # 资金明细
        self.trade_amount = trade_amount
        self.tax_coeff = tax_coeff
        self.commission_coeff = commission_coeff
        self.min_commission = min_commission
        self.history = []  # 交易历史
        self.available_sell = 0  # 当前可卖数量
        self._calced = False
        self._colname = col_name
        # self.hold_amount=[]#当前持仓数量
        # self.hold_price=[]#当前持仓金额

    @property
    def history_df(self):
        """获取成交历史的 :py:class:`pandas.DataFrame` 格式。"""
        return pd.DataFrame(self.history)

    @property
    def available_cash(self):
        """获取当前可用资金"""
        return self.cash[-1]

    def _calc_commission(self, price, amount):
        """计算交易手续费"""
        return max(price * amount * self.commission_coeff, self.min_commission)

    def _calc_tax(self, price, amount):
        """计算印花税"""
        return price * amount * self.tax_coeff

    def _calc_availble_buy(self, price):
        """计算可买数量"""
        count = 0
        value = price * count
        while (value < self.available_cash):
            count = count + self._min_buy_amount
            value = price * count
        return count - self._min_buy_amount if count > 0 else count

    def calc_trade_history(self, signal_buy_date, signal_sell_date, verbose=0, allin=False):
        """计算交易记录

        Args:
            signal_buy_date ([datetime.datetime]): 计划买入日期的集合。
            signal_sell_date ([datetime.datetime]): 计划卖出日期的集合。
            verbose (int): 是否显示计算过程。0（不显示），1（显示部分），2（显示全部）。默认为0。
            allin (bool): 是否每次都全下（所有资金买入或所有持仓卖出）。默认为 ``False``。
                如果为 ``True`` ，则不使用构造函数中传入的 `trade_amount` 属性。
        """

        sorted_buy_date = sorted(signal_buy_date)
        sorted_sell_date = sorted(signal_sell_date)

        for index, row in self.data.iterrows():
            date = row['date']
            if date in sorted_buy_date:
                price = row['close']  # 买入价格
                amount = self._calc_availble_buy(price) if allin else self.trade_amount  # 买入数量
                commission = self._calc_commission(price, amount)
                tax = self._calc_tax(price, amount)
                value = price * amount + commission + tax
                if value <= self.available_cash and amount > 0:
                    self.history.append({
                        'date': date,
                        'towards': 'buy',
                        'price': row[self._colname],
                        'amount': amount,
                        'total': value,
                        'commission': commission,
                        'tax': tax
                    })
                    self.cash.append(self.available_cash - value)
                    self.available_sell = self.available_sell + amount
                    # self.hold_amount=self.hold_amount+amount
                    # self.hold_price=self.hold_price+value
                    if verbose > 0:
                        print('{} 买入 {:.2f}/{:.2f}，剩余资金 {:.2f}'.format(date, price, amount, self.available_cash))
                else:
                    if verbose > 1:
                        print('{} 可用资金不足，跳过购买。'.format(date))
            if date in sorted_sell_date:
                amount = self.available_sell if allin else self.trade_amount  # 卖出数量
                if amount <= self.available_sell and amount > 0:
                    price = row['close']
                    commission = self._calc_commission(price, amount)
                    tax = self._calc_tax(price, amount)
                    value = price * amount - commission - tax
                    self.history.append({
                        'date': date,
                        'towards': 'sell',
                        'price': row[self._colname],
                        'amount': amount,
                        'total': value,
                        'commission': commission,
                        'tax': tax
                    })
                    self.cash.append(self.available_cash + value)
                    self.available_sell = self.available_sell - amount
                    # self.hold_amount=self.hold_amount-amount
                    # self.hold_price=self.hold_price-value
                    if verbose > 0:
                        print('{} 卖出 {:.2f}/{:.2f}，剩余资金 {:.2f}'.format(date, price, amount, self.available_cash))
                else:
                    if verbose > 1:
                        print('{} 没有持仓，跳过卖出。'.format(date))
        print('计算完成！')
        self._calced = True

    def _calc_total_tax(self):
        return np.array([x['tax'] for x in self.history]).sum()

    def _calc_total_commission(self):
        return np.array([x['commission'] for x in self.history]).sum()

    def report(self):
        """获取计算结果

        Returns:
            str: 返回计算结果。
        """
        result = ''
        if not self._calced:
            result = '没有经过计算。请先调用 `calc_trade_history` 方法进行计算。'
            return result
        result = '数据时间:{}~{}（可交易天数{}）'.format(self.data.iloc[0]['date'], self.data.iloc[-1]['date'], len(self.data))
        result = result + '\n交易次数:{} (买入/卖出各算1次)'.format(len(self.history))
        result = result + '\n当前持仓:{},可用资金:{:.2f}'.format(self.available_sell, self.available_cash)
        result = result + '\n资金变化率:{:.2%}'.format(self.available_cash / self.init_cash)
        result = result + '\n总手续费:{:.2f}'.format(self._calc_total_commission())
        result = result + '\n总印花税:{:.2f}'.format(self._calc_total_tax())
        result = result + '\n交易历史：'
        result = result + self.history_df.to_string()
        return result
