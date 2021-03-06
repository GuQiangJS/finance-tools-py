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


class MFI(CallBack):
    """附加顺势指标。

        执行后会对数据源中附加如下的列：

        * cci_x: x日顺势指标。（ `x` 为 `timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.CCI` 中的相关参数。
        col_vol: 计算时取值的列名。默认为 `volume`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import MFI
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],
                                'high': [y for y in range(10.1, 15.0)],
                                'low': [y for y in range(0.0, 4.9)],
                                'volume': [y for y in range(50.0, 100.0, 10.0)]})
        >>> print(data)
           close  high  low  volume
        0    5.0  10.1  0.0    50.0
        1    6.0  11.1  1.0    60.0
        2    7.0  12.1  2.0    70.0
        3    8.0  13.1  3.0    80.0
        4    9.0  14.1  4.0    90.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[MFI(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'mfi' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        mfi_3:[ nan  nan  nan 100. 100.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_vol = kwargs.get('low_close', 'volume')
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算顺势指标"""
        real = 'mfi_{}'.format(self.timeperiod)
        data[real] = talib.MFI(data[self.col_high].values,
                               data[self.col_low].values,
                               data[self.col_close].values,
                               data[self.col_vol].values, self.timeperiod)


class CCI(CallBack):
    """附加顺势指标。

        执行后会对数据源中附加如下的列：

        * cci_x: x日顺势指标。（ `x` 为 `col_high`_`col_low`_`col_close`_`timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.CCI` 中的相关参数。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import CCI
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],
                                'high': [y for y in range(10.1,15.0)],
                                'low': [y for y in range(0.0, 4.9)]})
        >>> print(data)
           close  high  low
        0    5.0  10.1  0.0
        1    6.0  11.1  1.0
        2    7.0  12.1  2.0
        3    8.0  13.1  3.0
        4    9.0  14.1  4.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[CCI(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'cci' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        cci_high_low_close_3:[ nan  nan 100. 100. 100.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算顺势指标"""
        real = 'cci_{}_{}_{}_{}'.format(self.col_high, self.col_low,
                                        self.col_close, self.timeperiod)
        data[real] = talib.CCI(data[self.col_high].values,
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


class RSI(CallBack):
    """附加计算Relative Strength Index 相对强弱指数。

        执行后会对数据源中附加如下的列：

        * rsi_x: x日双移动平均线。（ `x` 为 `col_name_timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.RSI` 中的相关参数。
        col_name: 计算时使用的数据列。默认为 `col_close`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import RSI
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})
        >>> print(data['close'].values)
        [0. 1. 2. 3. 4. 5. 6. 7.]
        >>> t=3
        >>> s = Simulation(data,'',callbacks=[RSI(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'rsi' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        rsi_close_3:[ nan  nan  nan 100. 100. 100. 100. 100.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_name = kwargs.pop('col_name', self.col_close)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算Relative Strength Index 相对强弱指数"""
        real = 'rsi_{}_{}'.format(self.col_name, self.timeperiod)
        data[real] = talib.RSI(data[self.col_name].values, self.timeperiod)


class SMA(CallBack):
    """附加计算SMA - 简单移动均线指标

        执行后会对数据源中附加如下的列：

        * sma_x: x日简单移动均线。（ `x` 为 `col_name_timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.SMA` 中的相关参数。
        col_name: 计算时使用的数据列。默认为 `col_close`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import SMA
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)]})
        >>> print(data)
           close
        0    5.0
        1    6.0
        2    7.0
        3    8.0
        4    9.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[SMA(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'sma' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        sma_close_3:[nan nan  6.  7.  8.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_name = kwargs.pop('col_name', self.col_close)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算SMA - 简单移动均线指标"""
        real = 'sma_{}_{}'.format(self.col_name, self.timeperiod)
        data[real] = talib.SMA(data[self.col_name].values, self.timeperiod)


class EMA(CallBack):
    """附加计算EMA - 指数移动平均线

        执行后会对数据源中附加如下的列：

        * ema_x: x日简单移动均线。（ `x` 为 `col_name_timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.EMA` 中的相关参数。
        col_name: 计算时使用的数据列。默认为 `col_close`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import EMA
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)]})
        >>> print(data)
           close
        0    5.0
        1    6.0
        2    7.0
        3    8.0
        4    9.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[EMA(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'ema' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        ema_close_3:[nan nan  6.  7.  8.]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_name = kwargs.pop('col_name', self.col_close)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算EMA - 指数移动平均线"""
        real = 'ema_{}_{}'.format(self.col_name, self.timeperiod)
        data[real] = talib.EMA(data[self.col_name].values, self.timeperiod)


class WMA(CallBack):
    """附加计算WMA - 加权移动平均线

        执行后会对数据源中附加如下的列：

        * wma_x: x日简单移动均线。（ `x` 为 `col_name_timeperiod` ）。

    Attributes:
        timeperiod: 参考 `talib.WMA` 中的相关参数。
        col_name: 计算时使用的数据列。默认为 `col_close`。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import WMA
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})
        >>> print(data['close'].values)
        [0. 1. 2. 3. 4. 5. 6. 7.]
        >>> t=3
        >>> s = Simulation(data,'',callbacks=[WMA(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'dema' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        wma_close_3:[ nan  nan 1.33 2.33 3.33 4.33 5.33 6.33]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.col_name = kwargs.pop('col_name', self.col_close)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算WMA - 加权移动平均线"""
        real = 'wma_{}_{}'.format(self.col_name, self.timeperiod)
        data[real] = talib.WMA(data[self.col_name].values, self.timeperiod)


class ATR(CallBack):
    """附加计算ATR - 平均真实波幅指标

        执行后会对数据源中附加如下的列：

        * atr_x: x日平均真实波幅指标。（ `x` 为 `timeperiod` ）。

    Warnings:
        根据 talib 官网说明，ATR功能的周期并不稳定。

    Attributes:
        timeperiod: 参考 `talib.ATR` 中的相关参数。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import ATR
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],
                                'high': [y for y in range(10.1,15.0)],
                                'low': [y for y in range(0.0, 4.9)]})
        >>> print(data)
           close  high  low
        0    5.0  10.1  0.0
        1    6.0  11.1  1.0
        2    7.0  12.1  2.0
        3    8.0  13.1  3.0
        4    9.0  14.1  4.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[ATR(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'atr' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        atr_3:[ nan  nan  nan 10.1 10.1]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算平均真实波幅指标"""
        real = 'atr_{}'.format(self.timeperiod)
        data[real] = talib.ATR(data[self.col_high].values,
                               data[self.col_low].values,
                               data[self.col_close].values, self.timeperiod)


class NATR(CallBack):
    """附加计算NATR - 归一化平均真实波幅

        执行后会对数据源中附加如下的列：

        * natr_x: x日平均真实波幅指标。（ `x` 为 `timeperiod` ）。

    Warnings:
        根据 talib 官网说明，NATR功能的周期并不稳定。

    Attributes:
        timeperiod: 参考 `talib.NATR` 中的相关参数。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import NATR
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],
                                'high': [y for y in range(10.1,15.0)],
                                'low': [y for y in range(0.0, 4.9)]})
        >>> print(data)
           close  high  low
        0    5.0  10.1  0.0
        1    6.0  11.1  1.0
        2    7.0  12.1  2.0
        3    8.0  13.1  3.0
        4    9.0  14.1  4.0
        >>> t = 3
        >>> s = Simulation(data,'',callbacks=[NATR(t)])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'atr' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        natr_3:[   nan    nan    nan 126.25 112.22]
    """
    def __init__(self, timeperiod, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """附加计算归一化平均真实波幅"""
        real = 'natr_{}'.format(self.timeperiod)
        data[real] = talib.NATR(data[self.col_high].values,
                                data[self.col_low].values,
                                data[self.col_close].values, self.timeperiod)


class TRANGE(CallBack):
    """附加计算TRANGE - 真正的范围

        执行后会对数据源中附加如下的列：

        * trange: 真正的范围。

    Examples:
        >>> from finance_tools_py.simulation.callbacks.talib import TRANGE
        >>> from finance_tools_py.simulation import Simulation
        >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],
                                'high': [y for y in range(10.1,15.0)],
                                'low': [y for y in range(0.0, 4.9)]})
        >>> print(data)
           close  high  low
        0    5.0  10.1  0.0
        1    6.0  11.1  1.0
        2    7.0  12.1  2.0
        3    8.0  13.1  3.0
        4    9.0  14.1  4.0
        >>> s = Simulation(data,'',callbacks=[TRANGE()])
        >>> s.simulate()
        >>> cols = [col for col in data.columns if 'trange' in col]
        >>> for col in cols:
        >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
        trange:[ nan 10.1 10.1 10.1 10.1]
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_preparing_data(self, data, **kwargs):
        """附加计算真正的范围"""
        data['trange'] = talib.TRANGE(data[self.col_high].values,
                                      data[self.col_low].values,
                                      data[self.col_close].values)


class LINEARREG_SLOPE(CallBack):
    """计算线性角度

        执行后会对数据源中附加如下的列：

        * x_lineSlope_y: 线性角度。（ `x` 为 `colname`；`y` 为 `timeperiod` ）。

        Examples:
            >>> from finance_tools_py.simulation.callbacks.talib import ATR
            >>> from finance_tools_py.simulation import Simulation
            >>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)]})
            >>> print(data)
               close
            0    5.0
            1    6.0
            2    7.0
            3    8.0
            4    9.0
            >>> t = 3
            >>> s = Simulation(data,'',callbacks=[LINEARREG_SLOPE('close',t)])
            >>> s.simulate()
            >>> cols = [col for col in data.columns if 'lineSlope' in col]
            >>> for col in cols:
            >>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))
            close_lineSlope_3:[nan nan  1.  1.  1.]
    """
    def __init__(self, colname, timeperiod, **kwargs):
        """

        Args:
            colname: 计算角度的列名。
            timeperiod: 计算角度时使用的时间窗口。
        """
        super().__init__(**kwargs)
        self.colname = colname
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        col_name = '{}_lineSlope_{}'.format(self.colname, self.timeperiod)
        data[col_name] = talib.LINEARREG_SLOPE(data[self.colname],
                                               self.timeperiod)
