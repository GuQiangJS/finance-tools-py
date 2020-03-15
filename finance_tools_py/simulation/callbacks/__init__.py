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

class Rolling_Future(CallBack):
    """取未来 n 天的最低，最高，平均，中位数价格。

        执行后会对数据源中附加如下的列：

        * rolling_x_min: 未来n日取值最低
        * rolling_x_max: 未来n日取值最高
        * rolling_x_mean: 未来n日取值平均
        * rolling_x_mean: 未来n日取值中位数
        * rolling_x_mean/col_name: 未来n日取值平均/当前取值
        * rolling_x_med/col_name: 未来n日取值中位数/当前取值
        * rolling_x_max/col_name: 未来n日取值最高/当前取值
        * rolling_x_min/col_name: 未来n日取值最低/当前取值

        `x` 生成规则为 `col_name_timeperiod` 。

    Attributes:
        timeperiod:
        skip: 跳过的日期数。默认取 `timeperiod`。
            与其他回调方法方法共同使用时，需要保证 `timeperiod` 参数给值一致。
        col_name:计算时使用的列名。默认使用 `col_close` 。

    Examples:
        >>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})
        >>> print(data['close'].values)
        [0 1 2 3 4 5 6 7]
        >>> t=3
        >>> print(Rolling_Future(t).on_preparing_data(data))
        >>> cols=[col for col in data.columns if col!='close']
        >>> for col in cols:
        >>>     print('{}\\n{}'.format(col,np.round(data[col].values,2)))
        rolling_close_3_min
        [nan nan  3.  4.  5. nan nan nan]
        rolling_close_3_max
        [nan nan  5.  6.  7. nan nan nan]
        rolling_close_3_mean
        [nan nan  4.  5.  6. nan nan nan]
        rolling_close_3_med
        [nan nan  4.  5.  6. nan nan nan]
        rolling_close_3_mean/close
        [ nan  nan 2.   1.67 1.5   nan  nan  nan]
        rolling_close_3_med/close
        [ nan  nan 2.   1.67 1.5   nan  nan  nan]
        rolling_close_3_max/close
        [ nan  nan 2.5  2.   1.75  nan  nan  nan]
        rolling_close_3_min/close
        [ nan  nan 1.5  1.33 1.25  nan  nan  nan]
    """
    def __init__(self,timeperiod,skip=None,col_name=None):
        """构造

        Args:
            skip (int): 跳过的日期数。默认取 `timeperiod`。
            与其他回调方法方法共同使用时，需要保证 `timeperiod` 参数给值一致。
            col_name (int): 计算时使用的列名。默认使用 `col_close` 。
        """
        super().__init__()
        self.timeperiod=timeperiod
        self.skip=timeperiod if skip is None else skip
        self.col_name=self.col_close if col_name is None else col_name

    def on_preparing_data(self, data, **kwargs):
        col_min = 'rolling_{}_{}_min'.format(self.col_name,self.timeperiod)
        col_max = 'rolling_{}_{}_max'.format(self.col_name,self.timeperiod)
        col_mean = 'rolling_{}_{}_mean'.format(self.col_name,self.timeperiod)
        col_med = 'rolling_{}_{}_med'.format(self.col_name,self.timeperiod)
        r = data.shift(-self.timeperiod)[self.col_name].rolling(self.timeperiod)
        data[col_min] = r.min()
        data[col_max] = r.max()
        data[col_mean] = r.mean()
        data[col_med] = r.median()
        n_mean='{}/{}'.format(col_mean, self.col_name)
        n_med='{}/{}'.format(col_med, self.col_name)
        n_max='{}/{}'.format(col_max, self.col_name)
        n_min='{}/{}'.format(col_min, self.col_name)
        data[n_mean] = data[col_mean] / data[self.col_name]  # 未来n日的平均价。>1表示上涨，<1表示下跌
        data[n_med] = data[col_med] / data[self.col_name]  # 未来n日的中位数。>1表示上涨，<1表示下跌
        data[n_max] = data[col_max] / data[self.col_name]
        data[n_min] = data[col_min] / data[self.col_name]