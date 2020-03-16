import talib

from . import CallBack


class BBANDS(CallBack):
    """附加计算布林带数据。

        执行后会对数据源中附加如下的列：

        * bbands_x_up: n日布林带上线
        * bbands_x_mean: n日布林带中线
        * bbands_x_low: n日布林带下线
        * bbands_x_up/close: n日布林带上线/close的比率
        * bbands_x_up/bbands_x_low: n日布林带上线/n日布林带下线的比率
        * close/bbands_x_low: close/n日布林带下线的比率

        `x` 生成规则为 `timeperiod_nbdevup_nbdevup` 。

    Attributes:
        timeperiod: 参考 `talib.BBANDS` 中的相关参数。
        nbdevup: 参考 `talib.BBANDS` 中的相关参数。
        nbdevup: 参考 `talib.BBANDS` 中的相关参数。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import BBANDS
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})
        >>> print(data['close'].values)
        [0. 1. 2. 3. 4. 5. 6. 7.]
        >>> t = 3
        >>> u = 2.4
        >>> d = 2.7
        >>> s = Simulation(data,'',callbacks=[BBANDS(t, u, d)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'bbands' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        bbands_3_2.4_2.7_up:[ nan  nan 2.96 3.96 4.96 5.96 6.96 7.96]
        bbands_3_2.4_2.7_mean:[nan nan  1.  2.  3.  4.  5.  6.]
        bbands_3_2.4_2.7_low:[ nan  nan -1.2 -0.2  0.8  1.8  2.8  3.8]
        bbands_3_2.4_2.7_up/close:[ nan  nan 1.48 1.32 1.24 1.19 1.16 1.14]
        bbands_3_2.4_2.7_up/bbands_3_2.4_2.7_low:[   nan    nan  -2.46 -19.36   6.23   3.32   2.49   2.1 ]
        close/bbands_3_2.4_2.7_low:[   nan    nan  -1.66 -14.67   5.03   2.78   2.15   1.84]
    """
    def __init__(self, timeperiod, nbdevup, nbdevdn, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = timeperiod
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn

    def on_preparing_data(self, data, **kwargs):
        """附加布林带数据"""
        col_up = 'bbands_{}_{}_{}_up'.format(self.timeperiod, self.nbdevup,
                                             self.nbdevdn)  # 布林带上线
        col_mean = 'bbands_{}_{}_{}_mean'.format(self.timeperiod, self.nbdevup,
                                                 self.nbdevdn)  # 布林带中线
        col_low = 'bbands_{}_{}_{}_low'.format(self.timeperiod, self.nbdevup,
                                               self.nbdevdn)  # 布林带下线
        data[col_up], data[col_mean], data[col_low] = talib.BBANDS(
            data[self.col_close].values, self.timeperiod, self.nbdevup,
            self.nbdevdn)
        data['{}/{}'.format(
            col_up, self.col_close
        )] = data[col_up] / data[self.col_close]  # 上线相对于收盘价线的比率
        data['{}/{}'.format(
            col_up, col_low)] = data[col_up] / data[col_low]  # 上线相对于下线的比率
        data['{}/{}'.format(
            self.col_close,
            col_low)] = data[self.col_close] / data[col_low]  # 收盘价线相对于上线的比率


class WILLR(CallBack):
    """附加计算威廉指标。

        执行后会对数据源中附加如下的列：

        * willr_x: x日威廉指标。（ `x` 为 `timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.WILLR` 中的相关参数。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import WILLR
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)],
                                'high': [y for y in range(0.1, 8.2)],
                                'low': [y for y in range(0.2, 8.2)]})
        >>> print(data)
           close  high  low
        0    0.0   0.1  0.2
        1    1.0   1.1  1.2
        2    2.0   2.1  2.2
        3    3.0   3.1  3.2
        4    4.0   4.1  4.2
        5    5.0   5.1  5.2
        6    6.0   6.1  6.2
        7    7.0   7.1  7.2
        >>> t=3
        >>> s = Simulation(data,'',callbacks=[WILLR(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'willr' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        willr_3:[  nan   nan -5.26 -5.26 -5.26 -5.26 -5.26 -5.26]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算威廉指标"""
        willr = 'willr_{}'.format(self.timeperiod)
        data[willr] = talib.WILLR(data[self.col_high].values,
                                  data[self.col_low].values,
                                  data[self.col_close].values, self.timeperiod)


class DEMA(CallBack):
    """附加计算双移动平均线。

        执行后会对数据源中附加如下的列：

        * dema_x: x日双移动平均线。（ `x` 为 `col_name_timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.DEMA` 中的相关参数。
        col_name: 计算时使用的数据列。默认为 `col_close`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import DEMA
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})
        >>> print(data['close'].values)
        [0. 1. 2. 3. 4. 5. 6. 7.]
        >>> t=3
        >>> s = Simulation(data,'',callbacks=[DEMA(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'dema' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        dema_close_3:[nan nan nan nan  4.  5.  6.  7.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_name = kwargs.pop('col_name', self.col_close)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算双移动平均线"""
        real = 'dema_{}_{}'.format(self.col_name, self.timeperiod)
        data[real] = talib.DEMA(data[self.col_name].values, self.timeperiod)
