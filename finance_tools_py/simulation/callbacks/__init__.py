import abc


class CallBack:
    """读取数据时的回调。次类型为基类，所有回调需要派生自此基类

    Atrributes:
        close_name (str): 计算时取值的列名。默认为 `close`。
    """

    def __init__(self, **kwargs):
        """构造。

        Args:
            close_name (str): 计算时取值的列名。默认为 `close`。
        """
        self.close_name = kwargs.get('close_name', 'close')

    @abc.abstractmethod
    def on_preparing_data(self, data, **kwargs):
        """数据读取完成后的准备事件

        Args:
            data (:py:class:`pandas.DataFrame`): 待处理的数据。
        """
        pass
