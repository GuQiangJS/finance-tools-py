# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import numpy as np
import pandas as pd
from pandas import DataFrame


def _check_dataframe(df: pd.DataFrame):
    """检查参数 *df* 。
    如果为 ``None`` 或 为空，抛出 :exc:`ValueError` 异常。

    Args:
        df: 待检查的数据表。

    """
    if df is None or df.empty:
        raise ValueError()
    pass


def daily_returns(df: pd.DataFrame = None) -> pd.DataFrame:
    """计算日收益率

    Args:
        df: 待计算的数据表。

    Returns:
        按照 **正序排序** 计算后计算结果。

    """
    df_sort = _prepare_dataframe(df, sort=True)
    return ((df_sort - df_sort.shift(1)) / df_sort.shift(1)).dropna()


def daily_returns_avg(df: pd.DataFrame = None) -> pd.DataFrame:
    """计算平均日收益

    Args:
        df: 待计算的数据表。
            （未进行过 :func:`daily_returns` 计算的数据）

    Returns:
        按照 **正序排序** 计算后计算结果。

    """
    return daily_returns(df).mean()


def daily_returns_std(df: pd.DataFrame = None) -> pd.DataFrame:
    """计算日收益标准差

    Args:
        df: 待计算的数据表。
            （未进行过 :func:`daily_returns` 计算的数据）

    Returns:
        按照 **正序排序** 计算后计算结果。

    """
    return daily_returns(df).std()


def cum_returns(df: pd.DataFrame = None,
                column_name: str = None) -> pd.DataFrame:
    """计算累积收益

    Args:
        df: 待计算的数据表。
        column_name: 计算用的列名。默认为 ``None``。
                     如果此值为 ``None``，则默认取 参数 `df` 的第一列。

    Returns:
        按照 **正序排序** 计算后计算结果。

    """
    df = _prepare_dataframe(df, sort=True)
    if not column_name:
        column_name = df.columns[0]
    return (df[column_name].iloc[-1] / df[column_name].iloc[0]) - 1


def risk_free_interest_rate(sr: float = 0, cycle: int = 365) -> float:
    """根据 年化收益率 计算 指定周期的收益率

    Args:
        sr: 年化收益率。如果年化收益率为 4%，则传入 0.04。
        cycle: 计算周期。默认值为365。
            假设使用的是每日采样，一年共有 365 个交易日。
            假设使用的是每周采样，一年共有 52 个交易周。
            假设使用的是每月采样，一年共有 12 个交易月

    Returns:
        根据参数 `cycle` 返回不同采样周期的收益率。默认返回 *日化收益率*。
    """
    # 即便某支股票一年只交易了80天，在以每日采样计算调整因子时，还是应该是用365来进行计算
    return sr / cycle


def sharpe_ratio(r=None, rf=None, r_std: float = None) -> float:
    """计算 `夏普比率`_

    Args:
        r: 收益数据表( `DataFrame` )或均值(`float`)。
        rf: 无风险收益率表( `pandas.DataFrame` )或均值( `float` )。
        r_std: 参数 `r` 的标准差。如果 `r` 传入的是 `pd.DataFrame` 则无需传入此参数。

    Returns:
        计算后的夏普比率。

    .. _夏普比率:
        https://zh.wikipedia.org/wiki/%E8%AF%81%E5%88%B8%E6%8A%95%E8%B5%84%E5%9F%BA%E9%87%91#%E5%A4%8F%E6%99%AE%E6%AF%94%E7%8E%87
    """
    # 夏普比率是回报与风险的比率。公式为：
    # （Rp - Rf） / ？p
    # 其中：
    #
    # Rp = 投资者投资组合的预期回报率
    # Rf = 无风险回报率
    # ？p = 投资组合的标准差，风险度量

    r_mean = r
    rf_mean = rf
    rf_std = r_std
    if isinstance(r, pd.DataFrame):
        r_mean = r.mean()
        rf_std = r.std()
    if isinstance(rf, pd.DataFrame):
        rf_mean = rf.mean()

    result = (r_mean - rf_mean) / rf_std
    return result if isinstance(result, float) else result[0]


def mo(df: pd.DataFrame = None, n: int = 0,
       dropna: bool = False) -> pd.DataFrame:
    """计算 `MO运动量震荡指标 (Momentum Oscillator)`_

    Args:
        df: 数据表
        n: 待计算的天数
        dropna: 是否丢弃结果中为 `NaN` 的数据。默认为 `False`。

    Returns:
        计算后的数据表。

    .. _MO运动量震荡指标 (Momentum Oscillator):
        https://zh.wikipedia.org/wiki/%E9%81%8B%E5%8B%95%E9%87%8F%E9%9C%87%E7%9B%AA%E6%8C%87%E6%A8%99
    """
    # MOt = (Pt / Pt-n) * 100
    # 其中n為天數，Pt為當日股價，Pt-n為n日前的股價
    if n <= 0:
        raise ValueError('n<=0')
    df_sort = _prepare_dataframe(df)
    df_result = df_sort / df_sort.shift(n) * 100
    return df_result.dropna() if dropna else df_result


def beta_alpha(df: DataFrame = None, **kwargs):
    """计算 `beta系数`_ , `alpha系数`_

    Args:
        df: 收益表。
        kwargs:
            * m_name: 市场收益数据列列名。
            * s_name: 单支股票收益数据列列名。
            当 以上数据均不存在或有某项不存在时，
            取 `df` 的第一列为 `市场收益数据列` ；第二列为 `单支股票收益数据列`。

    Returns:
        (:obj:`float`): (beta,alpha)

    .. hint::
        `beta系数`_ , `alpha系数`_ 的计算也可以使用
        `numpy.polyfit <https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html>`_
        方法。

    .. _beta系数:
        https://zh.wikipedia.org/wiki/Beta%E7%B3%BB%E6%95%B0

    .. _alpha系数:
        https://zh.wikipedia.org/wiki/%E8%AF%81%E5%88%B8%E6%8A%95%E8%B5%84%E5%9F%BA%E9%87%91#%E9%98%BF%E5%B0%94%E6%B3%95%E7%B3%BB%E6%95%B0
    """
    dfsm = _prepare_dataframe(df, False, '')
    dfsm = dfsm.dropna()
    market_col = dfsm.columns[0]
    symbol_col = dfsm.columns[1]
    if 'm_name' in kwargs and kwargs['m_name'] in dfsm.columns:
        market_col = kwargs['m_name']
    if 's_name' in kwargs and kwargs['s_name'] in dfsm.columns:
        symbol_col = kwargs['s_name']
    covmat = np.cov(dfsm[symbol_col], dfsm[market_col])

    beta = covmat[0, 1] / covmat[1, 1]
    alpha = np.mean(dfsm[symbol_col]) - beta * np.mean(dfsm[market_col])
    return (beta, alpha)


def _prepare_dataframe(df: DataFrame, sort: bool = True, fillna: str = None):
    _check_dataframe(df)
    df_r = df.copy()
    if sort:
        df_r = df_r.sort_index()
    if fillna:
        df_r = df_r.fillna(method=fillna)
    return df_r


def sma(df: DataFrame = None, window: int = 10, fillna: str = 'ffill') -> \
        DataFrame:
    """计算 `简单移动平均`_

    Args:
        df: 待计算的数据表。
        window: 天数。默认值为 `10`。
        fillna: 填充空白数据的方式。默认为 `ffill`。为空表示不填充。
        参考 `pandas.DataFrame.fillna <https://pandas.pydata.org/pandas-docs/stable/generated/pandasDataFrame.fillna.html>`_ 中的 `method` 属性。

    Returns:
        计算后的数据表。

    .. _简单移动平均:
        https://zh.wikipedia.org/wiki/%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87#%E7%B0%A1%E5%96%AE%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87
    """
    return _prepare_dataframe(df, True, fillna).rolling(window=window).mean()


def ema(df: DataFrame = None, window=10) -> DataFrame:
    """计算 `指数移动平均`_

    Args:
        df: 待计算的数据表。
        window: 天数。默认值为 `10`。

    Returns:
        计算后的数据表。

    .. _指数移动平均:
        https://zh.wikipedia.org/wiki/%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87#%E6%8C%87%E6%95%B8%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87

    .. seealso::
        * `pandas.DataFrame.ewm <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.ewm.html>`_
    """
    return _prepare_dataframe(df, sort=True).ewm(span=window).mean()
