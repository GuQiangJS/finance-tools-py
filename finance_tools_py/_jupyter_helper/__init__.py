import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from IPython.display import clear_output
from finance_tools_py.backtest import BackTest
from finance_tools_py.simulation.callbacks import CallBack
import datetime
from finance_tools_py.backtest import AllInChecker
import logging

IN_COLAB = 'google.colab' in sys.modules

if not IN_COLAB:
    logging.warning('Colab用。如果不是在Colab下可能会有各种各样的问题！！！')


class Checker(AllInChecker):
    """测试用回测CallBack。每次最多买1/5，当价格超过持仓成本的15%时卖出"""
    def on_calc_buy_amount(self, date: datetime.datetime.timestamp, code: str,
                           price: float, cash: float) -> float:
        # 每次最多买1/5
        return super().on_calc_buy_amount(date, code, price, cash * 0.2)

    def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
                      price: float, cash: float, hold_amount: float,
                      hold_price: float) -> bool:
        """当 `date` 及 `code` 包含在参数 :py:attr:`sell_dict` 中时返回 `True` 。否则返回 `False` 。"""
        if hold_amount > 0 and hold_price * 1.15 > price:
            return False
        if code in self.sell_dict.keys() and date in self.sell_dict[code]:
            return True
        else:
            return False


def RANDMON_TEST_BASIC(symbol, times=100, buy_times=50):
    """随机执行 `times` 次回测。默认调用 :class:`Checker` 来执行回测。

    Args:
        symbol: 股票代码
        times: 随机执行总次数
        buy_times: 从所有数据中随机选择购买的次数。

    Returns:
        总价值平均值,总现金平均值
    """
    data = read_data_QFQ(symbol)
    data['code'] = symbol
    hs = []  # 总价值
    cs = []  # 可用资金
    for i in range(times):
        buys = data.iloc[np.random.choice(
            len(data),
            buy_times)].sort_values('date')['date'].dt.to_pydatetime()
        bt = BackTest(data, callbacks=[Checker({symbol: buys}, {})])
        bt.calc_trade_history()
        print(bt.total_assets_cur)
        hs.append(bt.total_assets_cur)
        cs.append(bt.available_cash)
    clear_output(True)
    print('{}'.format(symbol))
    print('测试区间：{}-{}。总交易天数:{}'.format(data.iloc[0]['date'],
                                       data.iloc[-1]['date'], len(data)))
    print('测试{}次后，平均总价值:{}'.format(times, np.average(hs)))
    print('测试{}次后，平均总现金:{}'.format(times, np.average(cs)))
    return np.average(hs), np.average(cs)


def read_data_QFQ(symbol='600036') -> pd.DataFrame:
    """读取前复权数据"""
    if not IN_COLAB:
        raise NotImplementedError()
    data = pd.read_csv(
        'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
        format(symbol),
        parse_dates=True,
        usecols=[
            'date', 'open_qfq', 'high_qfq', 'low_qfq', 'close_qfq',
            'volume_qfq'
        ])
    data['date'] = pd.to_datetime(data['date'])
    data.rename(columns={
        'open_qfq': 'open',
        'high_qfq': 'high',
        'low_qfq': 'low',
        'close_qfq': 'close',
        'volume_qfq': 'volume'
    },
                inplace=True)
    # data['preclose']=data['close'].shift()
    # data['nextclose']=data['close'].shift(-1)
    # data['nextchange']=data['nextclose']-data['close']
    # data['nextchange_sign']=np.sign(data['nextchange'])
    return data


def read_data_HFQ(symbol='600036') -> pd.DataFrame:
    """读取后复权数据"""
    if not IN_COLAB:
        raise NotImplementedError()
    data = pd.read_csv(
        'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
        format(symbol),
        parse_dates=True,
        usecols=[
            'date', 'open_hfq', 'high_hfq', 'low_hfq', 'close_hfq',
            'volume_hfq'
        ])
    data['date'] = pd.to_datetime(data['date'])
    data.rename(columns={
        'open_hfq': 'open',
        'high_hfq': 'high',
        'low_hfq': 'low',
        'close_hfq': 'close',
        'volume_hfq': 'volume'
    },
                inplace=True)
    # data['preclose']=data['close'].shift()
    # data['nextclose']=data['close'].shift(-1)
    # data['nextchange']=data['nextclose']-data['close']
    # data['nextchange_sign']=np.sign(data['nextchange'])
    return data


def plot_backtest(data, x, y, buy=None, sell=None):
    if isinstance(y, str):
        y = [y]
    plot_backtest_plotly(data, x, y, buy, sell).show()
    plot_backtest_seaborn(data, x, y, buy, sell)
    plt.show()


def plot_backtest_plotly(data, x, y, buy=None, sell=None, col='close'):
    """使用plotly绘制回测后的数据，数据上会标记买入点和卖出点"""
    if isinstance(y, str):
        y = [y]
    fig = go.Figure()
    for y1 in y:
        fig.add_trace(go.Scatter(x=data[x], y=data[y1], mode='lines', name=y1))
    if buy:
        b = data[data[x].isin(buy)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[col],
                       mode='markers',
                       marker=dict(color="red", size=6)))
    if sell:
        b = data[data[x].isin(sell)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[col],
                       mode='markers',
                       marker=dict(color="green", size=6)))
    return fig


def plot_backtest_seaborn(data,
                          x,
                          y,
                          buy=None,
                          sell=None,
                          figsize=(20, 6),
                          col='close'):
    """使用seaborn绘制回测后的数据，数据上会标记买入点和卖出点"""
    if isinstance(y, str):
        y = [y]
    fig = plt.figure(figsize=figsize)
    for y1 in y:
        sns.lineplot(data=data, x=x, y=y1)
    if buy:
        b = data[data[x].isin(buy)]
        plt.plot(b[x], b[col], 'r.')
    if sell:
        b = data[data[x].isin(sell)]
        plt.plot(b[x], b[col], 'gx')
    return fig
