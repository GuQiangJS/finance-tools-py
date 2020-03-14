import talib

from . import CallBack


class DEMA(CallBack):
    """调用 `talib.DEMA`_ 方法生成双指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.DEMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.DEMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.DEMA`_ 方法中的 `timeperiod` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.DEMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.DEMA`_ 在 `data` 中增加 ``dema_x_y`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为参数 :attr:`timeperiod` )。示例：`dema_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.DEMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 'dema_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.DEMA(data[self.close_name].values,
                             timeperiod=self.timeperiod)


class T3(CallBack):
    """调用 `talib.T3`_ 方法生成双指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.T3`_ 方法中的 `timeperiod` 参数。
        vfactor: 参考 `talib.T3`_ 方法中的 `vfactor` 参数。

    .. _talib.T3:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, vfactor, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.T3`_ 方法中的 `timeperiod` 参数。
            vfactor: 参考 `talib.T3`_ 方法中的 `vfactor` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.DEMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod
        self.vfactor = vfactor

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 和 :attr:`vfactor` 调用 `talib.T3`_ 在 `data` 中增加 ``t3_x_y_z`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为参数 :attr:`timeperiod`，`z` 为参数 :attr:`vfactor` )。
        示例：`t3_close_30_0` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.T3:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 't3_{}_{}_{}'.format(self.close_name, self.timeperiod,
                                 self.vfactor)
        data[n] = talib.T3(data[self.close_name].values,
                           timeperiod=self.timeperiod,
                           vfactor=self.vfactor)


class TEMA(CallBack):
    """调用 `talib.TEMA`_ 方法生成双指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.TEMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.TEMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.TEMA`_ 方法中的 `timeperiod` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.TEMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.TEMA`_ 在 `data` 中增加 ``tema_x_y`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为参数 :attr:`timeperiod` )。
        示例：`tema_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.TEMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 'tema_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.TEMA(data[self.close_name].values,
                             timeperiod=self.timeperiod)


class TRIMA(CallBack):
    """调用 `talib.TRIMA`_ 方法生成双指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.TRIMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.TRIMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.TRIMA`_ 方法中的 `timeperiod` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.TRIMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.TRIMA`_ 在 `data` 中增加 ``trima_x_y`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为参数 :attr:`timeperiod` )。
        示例：`trima_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.TRIMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 'trima_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.TRIMA(data[self.close_name].values,
                              timeperiod=self.timeperiod)


class WMA(CallBack):
    """调用 `talib.WMA`_ 方法生成双指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.WMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.WMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.WMA`_ 方法中的 `timeperiod` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.WMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.WMA`_ 在 `data` 中增加 ``wma_x_y`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为参数 :attr:`timeperiod` )。
        示例：`wma_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.WMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 'wma_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.WMA(data[self.close_name].values,
                            timeperiod=self.timeperiod)


class MomentumCallBcak(CallBack):
    """动量型指标基类

    Attributes:
        high_name (str): 计算时 `high` 参数取值的列名。默认为 `high`。
        low_name (str): 计算时 `low` 参数取值的列名。默认为 `low`。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.high_name = kwargs.get('high_name', 'high')
        self.low_name = kwargs.get('low_name', 'low')


class ADX(MomentumCallBcak):
    """平均趋向指数

    Attributes:
        timeperiod (int): 计算时 `timeperiod` 参数取值的列名。默认为 `14`。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timeperiod = kwargs.pop('timeperiod', 14)

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` , :attr:`high_name` , :attr:`low_name` , :attr:`close_name`
        调用 `talib.ADX`_ 在 `data` 中增加 ``adx_x_y_m_n`` , ``boll_x_y_m_n`` , ``boll_x_y_m_n`` 列。
        (`x` 为参数 :attr:`high_name` ，`y` 为 :attr:`low_name` ，`m` 为 :attr:`close_name` ，`n` 为 :attr:`timeperiod` )。
        示例：`adx_high_low_close_14` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.ADX:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        n = 'adx_{}_{}_{}_{}'.format(self.high_name, self.low_name,
                                     self.close_name, self.timeperiod)
        data[n] = talib.ADX(high=data[self.high_name].values,
                            low=data[self.low_name].values,
                            close=data[self.close_name].values,
                            timeperiod=self.timeperiod)


class BBANDS(CallBack):
    """调用 `talib.BBANDS`_ 方法生成布林线。

    Attributes:
        timeperiod: 参考 `talib.BBANDS`_ 方法中的 `timeperiod` 参数。
        nbdevup: 参考 `talib.BBANDS`_ 方法中的 `nbdevup` 参数。
        nbdevdn: 参考 `talib.BBANDS`_ 方法中的 `nbdevdn` 参数。

    .. _talib.BBANDS:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, nbdevup, nbdevdn, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.BBANDS`_ 方法中的 `timeperiod` 参数。
            nbdevup: 参考 `talib.BBANDS`_ 方法中的 `nbdevup` 参数。
            nbdevdn: 参考 `talib.BBANDS`_ 方法中的 `nbdevdn` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.BBANDS:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` , :attr:`nbdevup` , :attr:`nbdevdn`
        调用 `talib.DEMA`_ 在 `data` 中增加 ``boll_x_y_m_n_up`` , ``boll_x_y_m_n_mean`` , ``boll_x_y_m_n_low`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为 :attr:`timeperiod` ，`m` 为 :attr:`nbdevup` ，`n` 为 :attr:`nbdevdn` )。
        示例：`boll_close_30_2_2_mean` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.BBANDS:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        up = 'boll_{}_{}_{}_{}_up'.format(self.close_name, self.timeperiod,
                                          self.nbdevup, self.nbdevdn)
        mean = 'boll_{}_{}_{}_{}_mean'.format(self.close_name, self.timeperiod,
                                              self.nbdevup, self.nbdevdn)
        low = 'boll_{}_{}_{}_{}_low'.format(self.close_name, self.timeperiod,
                                            self.nbdevup, self.nbdevdn)
        data[up], data[mean], data[low] = talib.BBANDS(
            data[self.close_name].values,
            timeperiod=self.timeperiod,
            nbdevup=self.nbdevup,
            nbdevdn=self.nbdevdn)


class EMA(CallBack):
    """调用 `talib.EMA`_ 方法生成指数移动平均。

    Attributes:
        timeperiod: 参考 `talib.EMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.EMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.EMA`_ 方法中的 `timeperiod` 参数。
            kwargs: 其他请参考 :meth:`.callbacks.CallBack.__init__` 中的参数。

        .. _talib.EMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.EMA`_ 在 `data` 中增加 ``ema_x_y`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为 :attr:`timeperiod` )。示例：`ema_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.EMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        data['ema_{}_{}'.format(self.close_name, self.timeperiod)] = talib.EMA(
            data[self.close_name].values, timeperiod=self.timeperiod)


class MA(CallBack):
    """调用 `talib.MA`_ 方法生成移动平均。

    Attributes:
        timeperiod: 参考 `talib.MA`_ 方法中的 `timeperiod` 参数。
        matype: 参考 `talib.MA`_ 方法中的 `matype` 参数。

    .. _talib.MA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, matype=0, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.EMA`_ 方法中的 `timeperiod` 参数。
            matype: 参考 `talib.MA`_ 方法中的 `matype` 参数。

        .. _talib.MA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod
        self.matype = matype

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 和 :attr:`matype` 调用 `talib.MA`_ 在 `data` 中增加 ``ma_x_y_z`` 列。
        (`x` 为参数 :attr:`close_name` ，`y` 为 :attr:`timeperiod` ，`z` 为 :attr:`matype` )。
        示例：`ma_close_30_0` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.MA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        data['ma_{}_{}_{}'.format(self.close_name, self.timeperiod,
                                  self.matype)] = talib.MA(
            data[self.close_name].values,
            timeperiod=self.timeperiod,
            matype=self.matype)


class MAMA(CallBack):
    """调用 `talib.MAMA`_ 方法生成MESA自适应移动平均。

    Warning:
        按照talib网站介绍。这个方法并不稳定。

    Attributes:
        fastlimit: 参考 `talib.MAMA `_ 方法中的 `fastlimit` 参数。
        slowlimit: 参考 `talib.MAMA`_ 方法中的 `slowlimit` 参数。

    .. _talib.MAMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

    """

    def __init__(self, fastlimit=0, slowlimit=0, **kwargs):
        """构造。

        Args:
            fastlimit: 参考 `talib.MAMA`_ 方法中的 `fastlimit` 参数。
            slowlimit: 参考 `talib.MAMA`_ 方法中的 `slowlimit` 参数。

        .. _talib.MAMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.fastlimit = fastlimit
        self.slowlimit = slowlimit

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`fastlimit` 和 :attr:`slowlimit` 调用 `talib.MAMA`_ 在 `data` 中增加 ``mama_x_y_z``
        列和 ``fama_x_y_z``。(`x` 为参数 :attr:`close_name` ，`y` 为 :attr:`fastlimit` ，`z` 为 :attr:`slowlimit` )。
        示例：`mama_close_0_0` 或 `fama_close_0_0` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.MAMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        mama = 'mama_{}_{}_{}'.format(self.close_name, self.fastlimit,
                                      self.slowlimit)
        fama = 'fama_{}_{}_{}'.format(self.close_name, self.fastlimit,
                                      self.slowlimit)
        data[mama], data[fama] = talib.MAMA(data[self.close_name].values,
                                            fastlimit=self.fastlimit,
                                            slowlimit=self.slowlimit)


class KAMA(CallBack):
    """调用 `talib.KAMA`_ 方法生成考夫曼自适应移动平均。

    Attributes:
        timeperiod: 参考 `talib.KAMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.KAMA:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造。

        Args:
            timeperiod: 参考 `talib.KAMA`_ 方法中的 `timeperiod` 参数。

        .. _talib.KAMA:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """根据 :attr:`timeperiod` 调用 `talib.KAMA`_ 在 `data` 中增加 ``kama_x_y`` 列.
            (`x` 为参数 :attr:`close_name` ，`y` 为 :attr:`timeperiod` )。示例：`kama_close_30` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.kama:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        data['kama_{}_{}'.format(self.close_name,
                                 self.timeperiod)] = talib.KAMA(
            data[self.close_name].values,
            timeperiod=self.timeperiod)


class HT_TRENDLINE(CallBack):
    """调用 `talib.HT_TRENDLINE`_ 方法生成希尔伯特变换-瞬时趋势。

    .. _talib.HT_TRENDLINE:
        https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
    """

    def on_preparing_data(self, data, **kwargs):
        """调用 `talib.HT_TRENDLINE`_ 在 `data` 中增加 ``ht_trendline_x`` 列.
            (`x` 为参数 :attr:`close_name` )。示例：`ht_trendline_close` 。

        Args:
            data (:class:`pandas.DataFrame`): 待处理的数据。

        .. _talib.HT_TRENDLINE:
            https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html
        """
        data['ht_trendline_{}'.format(self.close_name)] = talib.HT_TRENDLINE(
            data[self.close_name].values)


class MIDPOINT(CallBack):
    """调用 `talib.MIDPOINT`_ 线性角度。

    Attributes:
        timeperiod: 计算角度的日期区间。参考 `talib.MIDPOINT`_ 方法中的 `timeperiod` 参数。

    .. _talib.MIDPOINT:
        https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造

        Args:
            timeperiod: 参考 `talib.MIDPOINT`_ 方法中的 `timeperiod` 参数。

        .. _talib.MIDPOINT:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """对 :attr:`timeperiod` 指定的日期区间，调用 `talib.MIDPOINT`_
        在 `data` 中增加 ``midpoint_x_y`` 列（`x` 为参数 :attr:`close_name` ，y表示 :attr:`timeperiod` ）。
        示例：`midpoint_close_30` 。

        .. _talib.MIDPOINT:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        n = 'midpoint_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.MIDPOINT(data[self.close_name], self.timeperiod)


class SMA(CallBack):
    """调用 `talib.SMA`_。

    Attributes:
        timeperiod: 参考 `talib.SMA`_ 方法中的 `timeperiod` 参数。

    .. _talib.SMA:
        https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造

        Args:
            timeperiod: 参考 `talib.SMA`_ 方法中的 `timeperiod` 参数。

        .. _talib.SMA:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """对 :attr:`timeperiod` 指定的日期区间，调用 `talib.SMA`_
        在 `data` 中增加 ``sma_x_y`` 列（`x` 为参数 :attr:`close_name` ，y表示 :attr:`timeperiod` ）。
        示例：`sma_close_30` 。

        .. _talib.SMA:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        n = 'sma_{}_{}'.format(self.close_name, self.timeperiod)
        data[n] = talib.SMA(data[self.close_name], self.timeperiod)


class Linear_Angle(CallBack):
    """调用 `talib.LINEARREG_ANGLE`_ 线性角度。

    Attributes:
        timeperiod: 计算角度的日期区间。参考 `talib.LINEARREG_ANGLE`_ 方法中的 `timeperiod` 参数。

    .. _talib.LINEARREG_ANGLE:
        https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
    """

    def __init__(self, timeperiod, **kwargs):
        """构造

        Args:
            timeperiod (int): 计算角度的日期区间。
        """
        super().__init__(**kwargs)
        self.timeperiod = timeperiod

    def on_preparing_data(self, data, **kwargs):
        """对 :attr:`timeperiod` 指定的日期区间，调用 `talib.LINEARREG_ANGLE`_ ，生成角度值。
        在 `data` 中增加 ``linear_angle_x_y`` 列（`x` 为参数 :attr:`close_name` ，y表示 :attr:`timeperiod` ）。
        示例：`linear_angle_close_30` 。

        .. _talib.LINEARREG_ANGLE:
            https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html
        """
        data['linear_angle_{}_{}'.format(
            self.close_name,
            self.timeperiod)] = talib.LINEARREG_ANGLE(data[self.close_name],
                                                      self.timeperiod)
