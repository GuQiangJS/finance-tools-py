"""模拟"""

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import abc
import talib


class CallBack():
    """读取数据时的回调。次类型为基类，所有回调需要派生自此基类"""

    @abc.abstractmethod
    def on_preparing_data(self, symbol, data, context: {}):
        """数据读取完成后的准备事件

        Args:
            context (dict): 不同的回调之间传递数据用的上下文字典。
        """
        pass


class Bolling(CallBack):
    """调用 `talib.BBANDS`_ 方法生成布林线。并根据布林线计算简单的买入卖出点

    .. _talib.BBANDS:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, nbdevup, nbdevdn, difupstd, diflowstd):
        """构造。

        Args:
            timeperiod: 参考 `talib.BBANDS`_ 方法中的 `timeperiod` 参数。
            nbdevup: 参考 `talib.BBANDS`_ 方法中的 `nbdevup` 参数。
            nbdevdn: 参考 `talib.BBANDS`_ 方法中的 `nbdevdn` 参数。

        .. _talib.BBANDS:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        self.timeperiod = timeperiod
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn
        self.difupstd = difupstd
        self.diflowstd = diflowstd

    def on_preparing_data(self, symbol, data, context: {}):
        """根据 `timeperiod` , `nbdevup` , `nbdevdn` 调用 `talib.BBANDS`_
            生成 ``bool_x_up`` , ``bool_x_mean`` , ``bool_x_low`` 列；

            再分别除以 `close` 列，生成 ``diff_up`` , ``diff_mean`` , ``diff_low``；

            最后分别生成简易的买入/卖出比较价格，存放在 ``context`` 中，key值分别对应为 `m1` 和 `m2`

        .. _talib.BBANDS:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        up = 'boll_{}_up'.format(self.timeperiod)
        mean = 'boll_{}_mean'.format(self.timeperiod)
        low = 'boll_{}_low'.format(self.timeperiod)
        data[up], data[mean], data[low] = talib.BBANDS(data['close'].values,
                                                       timeperiod=self.timeperiod,
                                                       nbdevup=self.nbdevup,
                                                       nbdevdn=self.nbdevdn)
        data['diff_up'] = data[up] / data['close']
        data['diff_mean'] = data[mean] / data['close']
        data['diff_low'] = data[low] / data['close']

        context['m1'] = data['diff_up'].min() + data['diff_up'].std() * self.difupstd  # 卖出点
        context['m2'] = data['diff_low'].max() - data['diff_low'].std() * self.diflowstd  # 买入点


class Pandas_Rolling(CallBack):
    """根据 pandas 中的简单移动平均函数，计算平均值和标准差"""

    def __init__(self, min_periods=30, window=250):
        """构造函数

        Args:
            window : 参考 :py:class:`pandas.DataFrame.rolling` 方法中的 window 参数。
            min_periods : 参考 :py:class:`pandas.DataFrame.rolling` 方法中的 min_periods 参数。

        """
        self.min_periods = min_periods
        self.window = window

    def on_preparing_data(self, symbol, data, context: {}):
        """
        根据 `min_periods` 和 `window` 分别生成 ``rolling_mean`` 列和 ``rolling_std`` 列。
        """
        data['rolling_mean'] = data['close'].rolling(self.window,
                                                     min_periods=self.min_periods).mean()  # x日均价
        data['rolling_std'] = data['close'].rolling(self.window,
                                                    min_periods=self.min_periods).std()  # x日均价


class Linear_Angle(CallBack):
    """调用 `talib.LINEARREG_ANGLE`_ 线性角度

    .. _talib.LINEARREG_ANGLE:
        https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    """

    def __init__(self, max_linear_angle="MED", linear_angle=[3, 5, 10, 30]):
        """

        Args:
            max_linear_angle (str): 计算角度最大值取值时的参数。
                可以取平均值（MEAN）为最大值，也可以取中位数（MED）为最大值
            linear_angle ([int]): 计算角度的日期区间。默认会分别计算 `3,5,10,30` 日的线性角度。
        """
        self.linear_angle = linear_angle
        self.max_linear_angle = max_linear_angle

    def on_preparing_data(self, symbol, data, context: {}):
        """循环对 :py:attr:`linear_angle` 指定的日期区间，调用 `talib.LINEARREG_ANGLE`_ ，生成角度值。
            所有计算得到的值取绝对值，对没有值的内容填充 `99` （以示角度超大）。
            取到的所有值会放在 ``context`` 中，key值为 `angle` ；
            根据 :py:attr:`max_linear_angle` 设置的值对每隔日期区间的角度制取平均值或中位数。
            取得的值会放在 ``context`` 中，key值为 `max_angles` ；

        .. _talib.LINEARREG_ANGLE:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        angles = []
        max_angles = {}
        for angle in self.linear_angle:
            col = 'angle_{}'.format(angle)
            angles.append(col)
            data[col] = talib.LINEARREG_ANGLE(data['close'], angle).abs().fillna(99)  # 日均线角度
            if self.max_linear_angle == "MEAN":
                v = talib.LINEARREG_ANGLE(data['close'], angle).abs().mean()  # 日均线角度平均值
            else:
                v = talib.LINEARREG_ANGLE(data['close'], angle).abs().median()  # 日均线角度中位数
            if np.isnan(v):
                raise ValueError('{} LINEARREG_ANGLE is NaN'.format(angle))
            max_angles[col] = v
        context['angles'] = angles
        context['max_angles'] = max_angles


class CalcTradePoint(CallBack):
    """计算交易时间点"""

    def on_preparing_data(self, symbol, data, context: {}):
        """计算买入点和卖出点。分别标记在 ``opt`` 列中，卖出为 ``1`` ，买入为 ``2`` 。"""
        data['opt'] = 0

        m1 = context.pop('m1', None)
        m2 = context.pop('m2', None)

        data.loc[data['diff_up'] < m1, 'opt'] = 1  # 卖出点

        # 买入点计算开始
        # 买入条件：股价偏离30日均线上限或下线(diff_up,diff_low)
        query = 'diff_low>{:.2f}'.format(m2)
        # 买入条件：当前价格需要小于250日均价+标准差的上限
        data['rolling_mean'] = data['rolling_mean'] + data['rolling_std']
        query = query + ' & close<rolling_mean & '

        angles = context.pop('angles', None)
        max_angles = context.pop('max_angles', None)
        # 买入条件：均线角度绝对值小于平均值
        if angles and max_angles:
            query = query + (' & '.join(['{}<{:.2f}'.format(a, max_angles[a]) for a in angles]))
        #         print(query)
        data.loc[data.query(query).index, 'opt'] = 2
        # 买入点计算结束


class Simulation():
    """模拟类

    Example:
        >>> from finance_tools_py.simulation import Simulation
        >>> import matplotlib.pyplot as plt
        >>> import datetime
        >>> import QUANTAXIS as QA
        >>>
        >>> symbol='300378'
        >>> start = '2016-01-01'
        >>> end = datetime.date(2020, 3, 9)
        >>> data = QA.QA_fetch_stock_day_adv(symbol, start=start, end=end).to_qfq().data
        >>> sim = Simulation(data,symbol)
        >>> sim.simulate()
        >>> print(sim.lastest_signal)
        (False, Timestamp('2019-04-10 00:00:00'))
        >>> print(sim.signaldf)
                  date    code       open  ...    angle_5    angle_3  opt
        792 2019-04-04  300378  19.424380  ...  53.300611  59.359946    1
        793 2019-04-08  300378  21.370790  ...  59.448386  61.697846    1
        794 2019-04-09  300378  23.039142  ...  61.774397  63.894428    1
        795 2019-04-10  300378  24.826661  ...  63.982287  65.983814    1
        >>> sim.plot_sns()
        >>> plt.show()

    """

    def __init__(self, data: pd.DataFrame, symbol: str):
        """初始化

        Args:
            data (:py:class:`pandas.DataFrame`): 日线数据源，
            symbol (str): 股票代码。

        """
        self.__data = data.copy()
        self.__symbol = symbol

    def simulate(self,
                 callbacks=[Bolling(30, 2.6, 2.6, 0.3, 0.3),
                            Pandas_Rolling(30, 250),
                            Linear_Angle('MEAN', [60, 30, 10, 5, 3]),
                            CalcTradePoint()
                            ]):
        """执行模拟计算。默认使用 :py:class:`finance_tools_py.simulation.Bolling` ,
            :py:class:`finance_tools_py.simulation.Pandas_Rolling` ,
            :py:class:`finance_tools_py.simulation.Linear_Angle` 回调生成的数据。并最终由
            :py:class:`finance_tools_py.simulation.CalcTradePoint` 对数据进行合并计算，生成买入信号和卖出信号。
            可以在计算后，通过调用 :py:attr:`signaldf` 来获取信号表或
            通过调用 :py:attr:`lastest_signal` 来获取最后信号日期。
        """
        self.__df = self.__parse_data(callbacks=callbacks)
        if not self.__df.empty:
            self.__df = self.__df.reset_index()
            self.__buys = self.__df[self.__df['opt'] == 2]['date']
            self.__sells = self.__df[self.__df['opt'] == 1]['date']
        else:
            self.__df = None

    @property
    def lastest_signal(self):
        """获取最后信号日期

        Returns:
            [bool,Timestamp]: 第一个参数返回true表示当前返回的时间时买入信号的时间，否则为卖出信号的时间。
            第二个参数为信号点的时间。**注意：当信号点的时间为 `1970-01-01` 这个特殊时间时，
            返回数据是无意义的，表示卖出和买入均无信号点。**
        """
        s, d = self.__get_max_date(self.__buys, self.__sells)
        return s, d

    def plot_sns(self) -> plt.axes:
        """绘制买入卖出信号图像"""
        return self.__plot_sns(self.__df, buys=self.__buys, sells=self.__sells)

    @property
    def signaldf(self) -> pd.DataFrame:
        """根据模拟计算的结果，返回只包含买入卖出信号的数据表"""
        return self.__parse_df(self.__df, self.__buys, self.__sells)

    def __parse_data(self, callbacks=[]) -> pd.DataFrame:
        """读取指定股票的数据
        Args:
            fq (str): 是否复权。`00`:不复权，`01`:前复权，`02`:后复权
            callbacks  :CallBack的派生类集合。
        """
        context = {}
        for cb in callbacks:
            cb.on_preparing_data(self.__symbol, self.__data, context)
        return self.__data

    def __plot_sns(self, df, x='date', y=['close'], buys=[], sells=[], figsize=(20, 10),
                   fontsize='x-large') -> plt.axes:
        ax = df.plot(x=x, y=y, figsize=figsize)
        for buy in df[df['date'].isin(buys)][['date', 'close']].values:
            ax.scatter(x=buy[0], y=buy[1], c='r')
            ax.annotate('Buy:{:.2f}\n{}'.format(buy[1], buy[0].strftime('%Y-%m-%d')), buy, fontsize=fontsize)
        for sell in df[df['date'].isin(sells)][['date', 'close']].values:
            ax.scatter(x=sell[0], y=sell[1], c='g')
            ax.annotate('Sell:{:.2f}\n{}'.format(sell[1], sell[0].strftime('%Y-%m-%d')), sell, fontsize=fontsize)
        return ax

    def __parse_df(self, df, buys, sells, cols=None):
        """根据买入，卖出时间点，筛选df，并根据cols指定的列返回"""
        d = df[(df['date'].isin(buys)) | (df['date'].isin(sells))].sort_values('date')
        if cols:
            return d[cols]
        return d

    def __get_max_date(self, buys, sells):
        """获取最后信号日期

        Returns:
            [bool,Timestamp]: 第一个参数返回true表示当前返回的时间时买入信号的时间，否则为卖出信号的时间。
                第二个参数为信号点的时间。注意：当信号点的时间为 `1970-01-01` 这个特殊时间时，
                返回数据是无意义的，表示卖出和买入均无信号点。
        """
        if not buys.empty:
            mb = max(buys)
        else:
            mb = pd.to_datetime(datetime.datetime(1970, 1, 1))
        if not sells.empty:
            ms = max(sells)
        else:
            ms = pd.to_datetime(datetime.datetime(1970, 1, 1))
        return mb > ms, max(mb, ms)
