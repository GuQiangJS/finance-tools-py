def position_unit(price, v, funds):
    """计算头寸单位

    Args:
        price (float): 当前价格。
        v (float): 计算指标。海龟交易法则中常用ATR指标。
        funds (float): 最大可亏损资金。根据海龟交易法则，最大可亏损为1%。假设总金额为10万，那么这里就是1000。

    Examples:
        当前价格为6.39；ATR指标为0.08；最大可亏损资金1000（总金额10万，最大允许亏损1%）。
        
        >>> from finance_tools_py.calc import position_unit
        >>> position_unit(6.39,0.08,1000)
        1956

    See Also:
        [详解：头寸单位限制规模法则的——（海龟交易法则）](https://www.fmz.com/bbs-topic/715)

    Returns:
        int:
    """
    return int(funds / price / v)


def fluidity(data):
    """计算流动性。

    计算规则：取成交量平均值倒序排序（由大到小）+日回报标准差正向排序（由小到大），后的排名。

    Args:
        data (:py:class:`pandas.DataFrame`): 数据源。

    Examples:
        >>> from finance_tools_py.calc import fluidity
        >>> print(df)
          code  amount  rets
        0  001     100  0.01
        1  001     100  0.23
        2  002     200  0.02
        3  002     400  0.55
        4  003    1000  0.10
        5  003    3000  0.45
        >>> print(fluidity(df))
              amount_mean_sorted  amount  rets_std_sorted      rets  v
        code
        003                    0    2000                1  0.247487  1
        001                    2     100                0  0.155563  2
        002                    1     300                2  0.374767  3

    Returns:
        :py:class:`pandas.DataFrame`: 按照v值正向排序后的结果。
    """
    df_amount_mean = data.groupby('code').agg({'amount':'mean'}).sort_values('amount', ascending=False)
    df_amount_mean = df_amount_mean.reset_index().reset_index().set_index('code').rename(columns={'index': 'amount_mean_sorted'})
    df_ret_std = data.groupby('code').agg({'rets':'std'}).sort_values('rets')
    df_ret_std = df_ret_std.reset_index().reset_index().set_index('code').rename(columns={'index': 'rets_std_sorted'})
    df = df_amount_mean.join(df_ret_std)
    df['v'] = df['amount_mean_sorted'] + df['rets_std_sorted']
    return df.sort_values('v')
