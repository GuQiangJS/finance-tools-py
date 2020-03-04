import numpy as np
import pandas as pd
import datetime


class CallBack():
    def __init__(self):
        pass

    def on_calc_buy_check(self, date: datetime.datetime, code: str):
        """检查是否需要买入"""
        return False

    def on_calc_sell_check(self, date: datetime.datetime, code: str):
        """检查是否需要卖出"""
        return False


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
                 col_name='close',
                 callback=[CallBack()]):
        """初始化

        Args:
            data (:py:class:`pandas.DataFrame`): 完整的日线数据。数据中需要包含 `date` 列，用来标记日期。
                数据中至少需要包含 `date` 列、 `code` 列和 `close` 列，其中 `close` 列可以由参数 `colname` 参数指定。
            init_cash (float): 初始资金。
            trade_amount (int): 每次交易数量。默认100。
            tax_coeff (float): 印花税费率。默认0.001。
            commission_coeff (float): 手续费率。默认0.001。
            min_commission (float): 最小印花税费。默认5。
            col_name (str): 计算用的列名。默认为 `close` 。
                这个列名必须包含在参数 `data` 中。是用来进行回测计算的列，用来标记回测时使用的价格数据。
            callback ([:py:class: `finance_tools_py.backtest.CallBack`]): 回调函数集合。
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
        self._init_hold = pd.Series([], name='amount')
        self._init_hold.index.name = 'code'
        self._calced = False
        self._colname = col_name
        self._calbacks = callback
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
        # self.hold_amount=[]#当前持仓数量
        # self.hold_price=[]#当前持仓金额

    @property
    def history_df(self):
        """获取成交历史的 :py:class:`pandas.DataFrame` 格式。"""
        if len(self.history) > 0:
            lens = len(self.history[0])
        else:
            lens = len(self._history_headers)

        return pd.DataFrame(
            data=self.history,
            columns=self._history_headers[:lens]
        ).sort_index()

    @property
    def available_hold_df(self):
        """获取可用持仓

        Returns:
            :py:class:`pandas.DataFrame`
        """
        return self.history_df.groupby('code').amount.sum().replace(
            0,
            np.nan
        ).dropna().sort_index()

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
    def hold_price_cur(self):
        """计算目前持仓的成本  如果给的是日期,则返回当日开盘前的持仓

        Returns:
            :py:class:`pandas.Series`
        """

        def weights(x):
            n = len(x)
            res = 1
            while res > 0 or res < 0:
                res = sum(x[:n]['amount'])
                n = n - 1

            x = x[n + 1:]

            if sum(x['amount']) != 0:
                return np.average(x['price'], weights=x['amount'], returned=True)
            else:
                return np.nan

        return self.history_df.set_index('datetime', drop=False).sort_index().groupby('code').apply(weights).dropna()

    def hold_time(self, dt=None):
        """持仓时间。根据参数 `dt` 查询截止时间之前的交易，并与当前时间计算差异。

        Args:
            dt (datetime): 交易截止时间。如果为 `None` 则表示计算所有交易。默认为 `None` 。

        Returns:
            :py:class:`pandas.DataFrame`
        """

        def weights(x):
            if sum(x['amount']) != 0:
                return pd.Timestamp(datetime.datetime.today()) - pd.to_datetime(x.datetime.max())
            else:
                return np.nan

        if datetime is None:
            return self.history_df.set_index(
                'datetime',
                drop=False
            ).sort_index().groupby('code').apply(weights).dropna()
        else:
            return self.history_df.set_index(
                'datetime',
                drop=False
            ).sort_index().loc[:dt].groupby('code').apply(weights).dropna()

    @property
    def total_assets_cur(self):
        """获取当前总资产

        当前可用资金+当前持仓。
        """
        return self.available_cash + sum([x[0] * x[1] for x in self.hold_price_cur])

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

    def _check_callback_buy(self, date, code):
        for cb in self._calbacks:
            if cb.on_calc_buy_check(date, code):
                return True
        return False

    def _check_callback_sell(self, date, code):
        for cb in self._calbacks:
            if cb.on_calc_sell_check(date, code):
                return True
        return False

    def calc_trade_history(self, verbose=0, allin=False):
        """计算交易记录

        Args:
            verbose (int): 是否显示计算过程。0（不显示），1（显示部分），2（显示全部）。默认为0。
            allin (bool): 是否每次都全下（所有资金买入或所有持仓卖出）。默认为 ``False``。
                如果为 ``True`` ，则不使用构造函数中传入的 `trade_amount` 属性。
        """

        def update_history(history, date, code, price, amount, available_cash, commission, tax, toward):
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

        for index, row in self.data.iterrows():
            date = row['date']
            code = row['code']
            if self._check_callback_buy(date, code):
                price = row['close']  # 买入价格
                amount = self._calc_availble_buy(price) if allin else self.trade_amount  # 买入数量
                commission = self._calc_commission(price, amount)
                tax = self._calc_tax(price, amount)
                value = price * amount + commission + tax
                if value <= self.available_cash and amount > 0:
                    self.cash.append(self.available_cash - value)
                    update_history(self.history,
                                   date,
                                   code,
                                   price,
                                   amount,
                                   self.cash[-1],
                                   commission,
                                   tax,
                                   1, )
                    if verbose > 0:
                        print('{} 买入 {:.2f}/{:.2f}，剩余资金 {:.2f}'.format(date, price, amount, self.available_cash))
                else:
                    if verbose > 1:
                        print('{} 可用资金不足，跳过购买。'.format(date))
            if self._check_callback_sell(date, code):
                amount = self.available_hold_df[code] if allin else self.trade_amount  # 卖出数量
                if amount <= self.available_hold_df[code] and amount > 0:
                    price = row['close']
                    commission = self._calc_commission(price, amount)
                    tax = self._calc_tax(price, amount)
                    value = price * amount - commission - tax
                    self.cash.append(self.available_cash + value)
                    update_history(self.history,
                                   date,
                                   code,
                                   price,
                                   amount,
                                   self.cash[-1],
                                   commission,
                                   tax,
                                   -1, )
                    if verbose > 0:
                        print('{} 卖出 {:.2f}/{:.2f}，剩余资金 {:.2f}'.format(date, price, amount, self.available_cash))
                else:
                    if verbose > 1:
                        print('{} 没有持仓，跳过卖出。'.format(date))
        print('计算完成！')
        self._calced = True

    def _calc_total_tax(self):
        return np.asarray(self.history).T[6].sum()

    def _calc_total_commission(self):
        return np.asarray(self.history).T[5].sum()

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
        result = result + '\n初始资金:{:.2f}'.format(self.init_cash)
        result = result + '\n交易次数:{} (买入/卖出各算1次)'.format(len(self.history))
        result = result + '\n可用资金:{:.2f}'.format(self.available_cash)
        result = result + '\n当前持仓:'
        if not self.hold_price_cur.empty:
            result = result + self.hold_price_cur.to_string()
        else:
            result = result + '无'
        result = result + '\n当前总资产:{:.2f}'.format(self.total_assets_cur)
        result = result + '\n资金变化率:{:.2%}'.format(self.available_cash / self.init_cash)
        result = result + '\n资产变化率:{:.2%}'.format(self.total_assets_cur / self.init_cash)
        result = result + '\n总手续费:{:.2f}'.format(self._calc_total_commission())
        result = result + '\n总印花税:{:.2f}'.format(self._calc_total_tax())
        result = result + '\n交易历史：'
        result = result + self.history_df.to_string()
        return result
