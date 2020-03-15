import abc


class CallBack:
    """读取数据时的回调。此类型为基类，所有回调需要派生自此基类

    Attributes:
        col_close: 计算时取值的列名。默认为 `close`。
        col_high: 计算时取值的列名。默认为 `high`。
        col_low: 计算时取值的列名。默认为 `low`。
    """

    def __init__(self, **kwargs):
        """构造。

        Args:
            close_name (str): 计算时取值的列名。默认为 `close`。
        """
        self.col_close = kwargs.get('col_close', 'close')
        self.col_high = kwargs.get('high_close', 'high')
        self.col_low = kwargs.get('low_close', 'low')

    @abc.abstractmethod
    def on_preparing_data(self, data, **kwargs):
        """数据读取完成后的准备事件

        Args:
            data (:py:class:`pandas.DataFrame`): 待处理的数据。
        """
        pass
