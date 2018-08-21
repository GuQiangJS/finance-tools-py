# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import numpy as np
import pandas as pd


def _check_dataframe(df: pd.DataFrame):
    """检查 `df` 。如果为 `None` 或 为空，抛出 `ValueError`。

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
        按照*正序排序*计算后计算结果。

    """
    _check_dataframe(df)
    df = df.sort_index()
    return df[1:].values / df[:-1] - 1


def daily_returns_avg(df: pd.DataFrame = None) -> pd.DataFrame:
    """计算平均日收益

    Args:
        df: 待计算的数据表。（未进行过 `daily_returns` 计算的数据）

    Returns:
        按照*正序排序*计算后计算结果。

    """
    return daily_returns(df).mean()


def daily_returns_std(df: pd.DataFrame = None) -> pd.DataFrame:
    """计算日收益标准差

    Args:
        df: 待计算的数据表。（未进行过 `daily_returns` 计算的数据）

    Returns:
        按照*正序排序*计算后计算结果。

    """
    return daily_returns(df).std()


def cum_returns(df: pd.DataFrame = None,
                column_name: str = None) -> pd.DataFrame:
    """计算累积收益

    Args:
        df: 待计算的数据表。
        column_name: 计算用的列名。默认为 None。
                     如果此值为 None，则默认取 `df` 的第一列。

    Returns:
        按照*正序排序*计算后计算结果。

    """
    _check_dataframe(df)
    df = df.sort_index()
    if not column_name:
        column_name = df.columns[0]
    return (df[column_name].iloc[-1] / df[column_name].iloc[0]) - 1


def sharpe_ratio(daily_returns: pd.DataFrame = None, daily_rf: float = 0):
    """计算夏普比率

    Args:
        daily_returns (pd.DataFrame): 日收益数据表
        daily_rf (float): 日化无风险收益率

    Returns:

    """
    raise NotImplementedError()
    return (daily_returns - daily_rf).mean() / daily_returns.std()


def beta(returns_symbol: pd.DataFrame = None,
         returns_market: pd.DataFrame = None):
    """计算 `Beta系数`_。

    Args:
        returns_symbol (pd.DataFrame): 单支股票日回报率数据。
        returns_market (pd.DataFrame): 市场日回报率数据

    .. _Beta系数:
        https://zh.wikipedia.org/wiki/Beta%E7%B3%BB%E6%95%B0
    """
    raise NotImplementedError()
    # Create a matrix of [returns, market]
    m = np.matrix([returns_symbol, returns_market])
    # Return the covariance of m divided by the standard deviation of the market returns
    return np.cov(m)[0][1] / np.var(returns_market)
