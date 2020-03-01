"""常量定义"""


class ORDER_DIRECTION():
    """订单买卖方向

    Attributes:
        BUY: 股票 买入
        SELL: 股票 卖出

    """
    BUY = 1
    SELL = -1


class ORDER_STATUS():
    """订单状态

    Attributes:
        NEW
        SUCCESS
    """
    NEW = 'new'
    SUCCESS = 'success'


class AMOUNT_MODEL():
    """订单的成交量

    Attributes:
        BY_MONEY: 是按固定成交总额下单,动态计算成交量
        BY_AMOUNT: 按固定数量下单
    """

    BY_MONEY = 'by_money'
    BY_AMOUNT = 'by_amount'


class MARKET_TYPE():
    """市场种类

    Attributes:
        STOCK_CN: 中国A股
        INDEX_CN: 中国指数
    """
    STOCK_CN = 'stock_cn'  # 中国A股
    INDEX_CN = 'index_cn'  # 中国指数


class CURRENCY_TYPE():
    """货币种类

    Attributes:
        RMB: 人民币
    """
    RMB = 'rmb'  # 人民币


class DEFAULT_VALUE():
    """默认数据

    Attributes:
        COMMISSION_COEFF (float): 印花税费率。默认为 0.001。
        MIN_COMMISSION_COEFF (float): 印花税最低费率。默认为 5。
        TAX_COEFF (float): 税费。默认为 0.001。
    """
    COMMISSION_COEFF = 0.001  # 印花税费率
    MIN_COMMISSION_COEFF = 5  # 印花税最低费率
    TAX_COEFF = 0.001  # 税费
