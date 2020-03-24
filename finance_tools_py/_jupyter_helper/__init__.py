import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from IPython.display import clear_output
from finance_tools_py.backtest import BackTest
from finance_tools_py.simulation.callbacks import CallBack
from finance_tools_py.simulation import Simulation
import datetime
from finance_tools_py.backtest import AllInChecker
import logging
import traceback
from tqdm.auto import tqdm

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
        if code in self.sell_dict.keys() and date in self.sell_dict[code]:
            return True
        """当价格超过持仓成本的15%时卖出"""
        if hold_amount > 0 and hold_price * 1.15 < price:
            return True
        return False


def plot_basic(symbol, data=None, sim_callbacks=[], ys=[], **kwargs):
    """绘制收盘价与指标数据的分列图，每个数据一行。一并调用plotly和seaborn绘图。"""
    figsize = kwargs.pop('figsize', (15, len(ys) * 3))
    plot_basic_seaborn(symbol,
                       data,
                       sim_callbacks=sim_callbacks,
                       ys=ys,
                       figsize=figsize)


def plot_basic_plotly(symbol, data=None, sim_callbacks=[], ys=[], **kwargs):
    """绘制收盘价与指标数据的图。可以绘制买入/卖出点。

    Args:
        symbol: 股票代码。
        data: 待绘制的数据。如果为None，则会调用 :method:`read_data_QFQ` 读取。
        sim_callbacks: 调用 :method:`read_data_QFQ` 时使用的回调。用来附加数据。
        ys: 绘制的数据。默认应该至少需要包含1个。
        figsize: 默认宽度为15，高度为 `len(ys)*3)`
        xl: x轴。默认为 `date`。
        yl: y轴。默认为 `close`。
        buy: 购买时间集合。
        sell: 卖出时间集合。

    Returns:

    """
    if data is None:
        data = read_data_QFQ(symbol)
        s = Simulation(data, symbol, callbacks=sim_callbacks)
        s.simulate()
        data = s.data
    buy = kwargs.pop('buy', [])
    sell = kwargs.pop('sell', [])
    x = kwargs.pop('x', 'date')
    y = kwargs.pop('y', 'close')
    fig = go.Figure()
    for yt in ys:
        fig.add_trace(go.Scatter(x=data[x], y=data[yt], mode='lines', name=y))
    if buy:
        b = data[data[x].isin(buy)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[y],
                       mode='markers',
                       name='buy',
                       marker=dict(color="red", size=6)))
    if sell:
        b = data[data[x].isin(sell)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[y],
                       mode='markers',
                       name='sell',
                       marker=dict(color="green", size=6)))
    fig.show()


def plot_basic_seaborn(symbol, data=None, sim_callbacks=[], ys=[], **kwargs):
    """绘制收盘价与指标数据的分列图，每个数据一行。

    Args:
        symbol: 股票代码。
        data: 待绘制的数据。如果为None，则会调用 :method:`read_data_QFQ` 读取。
        sim_callbacks: 调用 :method:`read_data_QFQ` 时使用的回调。用来附加数据。
        ys: 绘制的数据。默认应该至少需要包含1个。
        figsize: 默认宽度为15，高度为 `len(ys)*3)`

    Returns:

    """
    figsize = kwargs.pop('figsize', (15, len(ys) * 3))
    if data is None:
        data = read_data_QFQ(symbol)
        s = Simulation(data, symbol, callbacks=sim_callbacks)
        s.simulate()
        data = s.data
    if len(ys) > 1:
        fig, axes = plt.subplots(len(ys), 1, figsize=figsize)
        for index, y in enumerate(ys):
            sns.lineplot(data=data, x='date', y=y, ax=axes[index])
    else:
        fig = plt.figure(figsize=figsize)
        sns.lineplot(data=data, x='date', y=ys[0])
    fig.suptitle('{} 数据预览'.format(symbol))
    plt.show()


def backtest(symbol,
             data=None,
             buy_query='',
             sell_query='',
             sim_callbacks=[],
             **kwargs):
    """

    Args:
        symbol:
        data:
        buy_query: 示例：'rsi_close_14>80'
        sell_query:
        callbacks:
        show_detail: 打印买入，卖出占比。默认为True
        show_report: 打印回测报告。默认为True
        show_history: 打印成交明细。默认为True
        plot: 绘图。默认为True

    Returns:
        backtest实例，数据，买入时间集合，卖出时间集合

    """
    if data is None or data.empty:
        data = read_data_QFQ(symbol)
        data['code'] = symbol
    s = Simulation(data, symbol, callbacks=sim_callbacks)
    s.simulate()
    s.data['code'] = symbol
    buys = []
    sells = []
    if buy_query:
        buys = s.data.query(buy_query)['date'].dt.to_pydatetime()
    if sell_query:
        sells = s.data.query(sell_query)['date'].dt.to_pydatetime()
    bt = BackTest(s.data, callbacks=[Checker({symbol: buys}, {symbol: sells})])
    bt.calc_trade_history()
    if kwargs.pop("clear_output", True):
        clear_output(True)
    print('\x1b[1;31m{} 回测测试\x1b[0m\n买入条件:{}\n卖出条件:{}'.format(
        symbol, buy_query, sell_query))
    print('-----------------------------------------------')
    if kwargs.pop('show_detail', True):
        print('预计购买次数:{},占比:{:.2%}\n预计卖出次数:{},占比:{:.2%}'.format(
            len(buys),
            len(buys) / len(s.data), len(sells),
            len(sells) / len(s.data)))
    if kwargs.pop('show_report', True):
        print(bt.report(**kwargs))
    if kwargs.pop('plot', True):
        plot_backtest(s.data,
                      x='date',
                      y='close',
                      buy=list(buys),
                      sell=list(sells))
    return bt, s.data, buys, sells


def RANDMON_TEST_BASIC(data, times=100, buy_times=50, **kwargs):
    """随机执行 `times` 次回测。默认调用 :class:`Checker` 来执行回测。

    Args:
        data: 所有股票完整数据
        times: 随机执行总次数
        buy_times: 从所有数据中随机选择购买的次数。
        clear_output: 执行完成后清除报告。默认为True。
        init_cash: 初始资金。默认50000.
        buy_data: 计算买入时间点的数据集。默认为 `data`。其中最少需要包含 `date` 和 `code` 列。

    Returns:
        报告,所有测试的总价值集合,所有测试的剩余现金集合,所有成交明细集合
    """
    hs = []  # 总价值
    cs = []  # 可用资金
    hiss = []  # 交易明细

    init_cash = kwargs.pop('init_cash', 50000)

    for i in tqdm(range(times)):
        buy_data = kwargs.pop('buy_data', data)
        buys = buy_data.iloc[np.random.choice(
            len(buy_data),
            buy_times)].sort_values('date').groupby('code')['date'].apply(
                lambda g: g.dt.to_pydatetime()).to_dict()

        bt = BackTest(data, init_cash=init_cash, callbacks=[Checker(buys, {})])
        bt.calc_trade_history(**kwargs)
        hs.append(bt.total_assets_cur)
        cs.append(bt.available_cash)
        hiss.append(bt.history_df)
    if kwargs.pop("clear_output", True):
        clear_output(True)
    report = '测试起始资金 {}，总数据量 {} 随机抽取 {} 次作为测试。'.format(init_cash, len(data),
                                                       buy_times)
    report = report + \
             '\n测试区间：{}-{}'.format(data.iloc[0]['date'], data.iloc[-1]['date'])
    report = report + '\n测试{}次后，平均总价值:{}'.format(times, np.average(hs))
    report = report + '\n测试{}次后，平均总现金:{}'.format(times, np.average(cs))
    return report, hs, cs, hiss


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
    try:
        plot_backtest_plotly(data, x, y, buy, sell).show()
    except:
        traceback.print_exc()
    try:
        plot_backtest_seaborn(data, x, y, buy, sell)
        plt.legend()
        plt.show()
    except:
        traceback.print_exc()


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
                       name='buy',
                       marker=dict(color="red", size=6)))
    if sell:
        b = data[data[x].isin(sell)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[col],
                       mode='markers',
                       name='sell',
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
        sns.lineplot(data=data, x=x, y=y1, c='#4281C0', label=y1)
    if buy:
        b = data[data[x].isin(buy)]
        plt.plot(b[x], b[col], 'r.', label='buy')
    if sell:
        b = data[data[x].isin(sell)]
        plt.plot(b[x], b[col], 'gx', label='sell')
    return fig
