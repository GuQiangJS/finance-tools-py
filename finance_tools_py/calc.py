
def position_unit(price,v,funds):
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
    return int(funds/price/v)