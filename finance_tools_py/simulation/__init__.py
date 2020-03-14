class Simulation():
    """模拟类

    Attributes:
        data: 数据源。调用 :func:`simulate` 方法后，会返回处理后的数据集，否则返回原始数据集。
        symbol: 股票代码
        callbacks: 处理数据时会使用到的回调 :class:`callbacks.CallBack` 集合。

    """

    def __init__(
            self,
            data,
            symbol,
            callbacks=[],
    ):
        """初始化

        Args:
            data (:class:`pandas.DataFrame`): 数据源，
            symbol (str): 股票代码。
            callbacks: 处理数据时会使用到的回调 :class:`callbacks.CallBack` 集合。
        """
        self.data = data.copy()
        self.symbol = symbol
        self.callbacks = callbacks

    def simulate(self, **kwargs):
        """执行模拟计算。默认使用 :attr:`callbacks` 回调生成的数据。

        Args:
            reset_index (bool): 是否对 :attr:`data` 做 :meth:`pandas.DataFrame.reset_index` 处理。
                默认为 `True`。
        """
        self.__parse_data()
        if not self.data.empty:
            if kwargs.pop('reset_index', True):
                self.data = self.data.reset_index()

    # def plot_sns(self, **kwargs) -> plt.axes:
    #     """绘制买入卖出信号图像
    #
    #     Args:
    #         data: 数据。默认为 :py:attr:`data` 。
    #         x: x轴。默认为 `date` 。
    #         y: y轴。可以传入列表。默认为 `[close]` 、
    #         buys: 买入点。时间集合。默认为当前模拟计算后的买入时间点集合。
    #         sells: 卖出点。时间集合。默认为当前模拟计算后的卖出时间点集合。
    #         figsize: 图片大小。默认为 `(20,10)`。
    #         annotate_fontsize： 买入点卖出点的文字大小。默认为 `x-large` 。
    #     """
    #
    #
    #     for cb in self.callbacks:
    #         cb.on_before_plot(**kwargs)
    #
    #     return self.__plot_sns(data, x=x, y=y,
    #                            buys=buys, sells=sells,
    #                            figsize=figsize,
    #                            annotate_fontsize=annotate_fontsize)
    #
    def __parse_data(self):
        """读取指定股票的数据"""
        context = {}
        for cb in self.callbacks:
            cb.on_preparing_data(self.symbol, self.data, context)
        # self.__query['buy'] = context['buy_query']
        # self.__query['sell'] = context['sell_query']

    # #
    # # def __plot_sns(self, df, x='date', y=['close'], buys=[], sells=[], figsize=(20, 10),
    # #                annotate_fontsize='x-large') -> plt.axes:
    # #     ax = df.plot(x=x, y=y, figsize=figsize)
    # #     for buy in df[df['date'].isin(buys)][['date', 'close']].values:
    # #         ax.scatter(x=buy[0], y=buy[1], c='r')
    # #         ax.annotate('Buy:{:.2f}\n{}'.format(buy[1], buy[0].strftime('%Y-%m-%d')), buy, fontsize=annotate_fontsize,
    # #                     c='r')
    # #     for sell in df[df['date'].isin(sells)][['date', 'close']].values:
    # #         ax.scatter(x=sell[0], y=sell[1], c='g')
    # #         ax.annotate('Sell:{:.2f}\n{}'.format(sell[1], sell[0].strftime('%Y-%m-%d')), sell,
    # #                     fontsize=annotate_fontsize)
    # #     return ax
