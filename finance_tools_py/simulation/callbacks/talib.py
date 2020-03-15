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
        >>> print(data)
              close      high       low
        0  0.469006  0.171093  0.917249
        1  0.878187  0.006180  0.113431
        2  0.653001  0.723537  0.502946
        3  0.852284  0.827910  0.496305
        4  0.603522  0.894394  0.020531
        >>> t=3
        >>> u=2.4
        >>> d=2.7
        >>> print(BBANDS(t, u, d).on_preparing_data(data))
        >>> cols=[col for col in data.columns if 'bbands' in col]
        >>> print(data[cols].info())
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 5 entries, 0 to 4
        Data columns (total 6 columns):
        bbands_3_2.4_2.7_up                         3 non-null float64
        bbands_3_2.4_2.7_mean                       3 non-null float64
        bbands_3_2.4_2.7_low                        3 non-null float64
        bbands_3_2.4_2.7_up/close                   3 non-null float64
        bbands_3_2.4_2.7_up/bbands_3_2.4_2.7_low    3 non-null float64
        close/bbands_3_2.4_2.7_low                  3 non-null float64
        dtypes: float64(6)
        memory usage: 320.0 bytes
        None
        >>> print(data[cols])
           bbands_3_2.4_2.7_up  ...  close/bbands_3_2.4_2.7_low
        0                  NaN  ...                         NaN
        1                  NaN  ...                         NaN
        2             1.068322  ...                    3.038042
        3             1.035945  ...                    1.630058
        4             0.960984  ...                    1.462615
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
        >>> print(data)
              close      high       low
        0  0.199431  0.192223  0.800428
        1  0.028853  0.778810  0.482552
        2  0.107672  0.468091  0.663075
        3  0.996489  0.252303  0.370167
        4  0.021458  0.663419  0.706077
        >>> t=3
        >>> print(WILLR(t).on_preparing_data(data))
        >>> cols=[col for col in data.columns if 'willr' in col]
        >>> print(data[cols].info())
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 5 entries, 0 to 4
        Data columns (total 1 columns):
        willr_3    3 non-null float64
        dtypes: float64(1)
        memory usage: 120.0 bytes
        None
        >>> print(data[cols])
              willr_3
        0         NaN
        1         NaN
        2 -226.538462
        3   53.268973
        4 -218.911650
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
