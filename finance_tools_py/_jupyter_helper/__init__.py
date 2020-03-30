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

plt.rcParams['font.family'] = 'SimHei'
# IN_COLAB = 'google.colab' in sys.modules

# if not IN_COLAB:
#     logging.warning('Colab用。如果不是在Colab下可能会有各种各样的问题！！！')


def __plot_BACKTEST_bar(v, title):
    for index, i in enumerate(v.items()):
        plt.bar(x=index, height=i[1], label=i[0])
    plt.legend()
    plt.title(title)


def __BACKTEST(data,
               zs_data,
               callback=[],
               buy_start='2018-01-01',
               buy_end='2018-12-31',
               **kwargs):
    dfs = []
    for symbol in tqdm(data['code'].unique(), desc='处理数据中...'):
        s = Simulation(data[data['code'] == symbol].sort_values('date'),
                       symbol,
                       callbacks=callback)
        s.simulate()
        s.data['code'] = symbol
        dfs.append(s.data)
    sim_data = pd.concat(dfs)
    sim_data.sort_values(['date', 'code'], inplace=True)
    clear_output(True)

    #取买入卖出点的计算数据
    bs_data = sim_data[(sim_data['date'] >= buy_start)
                       & (sim_data['date'] <= buy_end)]

    #计算买入/卖出点...
    buys = bs_data[bs_data['opt'] == 1].groupby('code')['date'].apply(
        lambda x: x.dt.to_pydatetime()).to_dict()
    sells = bs_data[bs_data['opt'] == -1].groupby('code')['date'].apply(
        lambda x: x.dt.to_pydatetime()).to_dict()

    bt, bs_data, bt_buy, bt_sell = BACKTEST_PACK(sim_data=sim_data,
                                                 buys=buys,
                                                 sells=sells)

    clear_output(True)
    print("可买入时间：{}~{}".format(buy_start, buy_end))
    print(bt.report(
        show_history=False,
        show_hold=False,
    ))

    baseline = data.groupby('code').apply(
        lambda df: df.iloc[-1]['close'] / df.iloc[0]['close']).mean()
    name = kwargs.pop('name', '')
    __plot_BACKTEST_bar(
        {
            "沪深300": zs_data.iloc[-1]['close'] / zs_data.iloc[0]['close'],
            "BaseLine": baseline,
            name: bt.total_assets_cur / bt.init_cash
        }, name)

    return bt, bs_data


def BACKTEST_PACK_YEAR(data, zs_data, year, sim_callbacks, **kwargs):
    """按照年度回测数据

    Args:
        data: 待回测的数据。
        hs_data： 指数相关数据。与 `data` 匹配。
        sim_callbacks: 回测时使用的回调集合。
        year: 年度
        title:
    """
    start = '{0}-01-01'.format(year)
    end = '{0}-12-31'.format(year)
    __BACKTEST(data[(data['date'] >= start)
                    & (data['date'] <= end)],
               zs_data[(zs_data['date'] >= start)
                       & (zs_data['date'] <= end)],
               callback=sim_callbacks,
               buy_start=start,
               buy_end=end,
               **kwargs)


def BACKTEST_PACK_ALL(data,
                      zs_data,
                      sim_callbacks,
                      start_year=2005,
                      end_year=2019,
                      **kwargs):
    """跨年度回测数据

    Args:
        data: 待回测的数据。
        zs_data: 指数相关数据。与 `data` 匹配。
        sim_callbacks: 回测时使用的回调集合。
        start_year: 开始年度
        end_year: 结束年度
        title:
        **kwargs:

    Returns:

    """
    start = '{0}-01-01'.format(start_year)
    end = '{0}-12-31'.format(end_year)
    __BACKTEST(data[(data['date'] >= start)
                    & (data['date'] <= end)],
               zs_data[(zs_data['date'] >= start)
                       & (zs_data['date'] <= end)],
               callback=sim_callbacks,
               buy_start=start,
               buy_end=end,
               **kwargs)


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


def BACKTEST_PACK(**kwargs):
    """多支支股票的回测计算。

    Args:
        sim_data: 所有处理后的数据。包含这个值以后，不再使用 `ori_data`。如果这个值为 None ，则会根据 `sim_callbacks` 中的回调定义对 `ori_data` 进行处理。
        ori_data: 所有原始数据。包含多支不同的股票。
        buy_sell_data: 买入卖出计算数据。默认使用 `data` 的值。如果传入字符串则从 `sim_data` 中根据条件取值。
        buys: 可以是字符串，示例：'rsi_close_14>80'。如果是字符串则会自动从 `buy_sell_data` 中筛选。也可以是字典类型，示例:{'000002':[datetime,datetime]}。如果是字典类型则无需传入 `buy_sell_data`。
        sells: 参考 `buys`。
        sim_callbacks: 附加数据时的回调。只有当 `sim_data` 为空时才有用。
        show_detail: 打印买入，卖出占比。默认为False
        show_report: 打印回测报告。默认为False
        show_history: 打印成交明细。默认为False
        plot: 绘图。默认为False

    Returns:
        backtest实例，数据，买入时间集合，卖出时间集合

    """
    dfs = []

    ori_data = kwargs.pop('ori_data', None)
    sim_data = kwargs.pop('sim_data', None)
    sim_callbacks = kwargs.pop('sim_callbacks', [])
    buys = kwargs.pop('buys', {})
    sells = kwargs.pop('sells', {})

    if sim_data is None and ori_data is None:
        raise ValueError()
    if sim_data is None:
        for symbol in tqdm(ori_data['code'].unique(), desc='处理数据中...'):
            s = Simulation(ori_data[ori_data['code'] == symbol],
                           symbol,
                           callbacks=sim_callbacks)
            s.simulate()
            s.data['code'] = symbol
            dfs.append(s.data)
        _data = pd.concat(dfs)
        _data.sort_values('date', inplace=True)
    else:
        _data = sim_data
    buy_sell_data = kwargs.pop('buy_sell_data', _data)
    #     _print_buy=False
    #     _print_sell=False
    if isinstance(buy_sell_data, str):
        buy_sell_data = _data.loc[_data.query(buy_sell_data)]
    if isinstance(buys, str):
        bq = str(buys)
        #         _print_buy=True
        buys = {}
        for symbol in tqdm(buy_sell_data['code'].unique(), desc='计算买入点...'):
            buys[symbol] = buy_sell_data[buy_sell_data['code'] ==
                                         symbol].query(
                                             bq)['date'].dt.to_pydatetime()
    if isinstance(sells, str):
        #         _print_sell=True
        sq = str(sells)
        for symbol in tqdm(buy_sell_data['code'].unique(), desc='计算卖出点...'):
            sells[symbol] = buy_sell_data[buy_sell_data['code'] ==
                                          symbol].query(
                                              sq)['date'].dt.to_pydatetime()
    bt = BackTest(_data, callbacks=[Checker(buys, sells)])
    bt.calc_trade_history()
    if kwargs.pop("clear_output", True):
        clear_output(True)
    #     print('\x1b[1;31m{} 回测测试\x1b[0m\n买入条件:{}\n卖出条件:{}'.format(
    #         symbol, buy_query, sell_query))
    #     print('-----------------------------------------------')
    if kwargs.pop('show_detail', False):
        print('预计购买次数:{},占比:{:.2%}\n预计卖出次数:{},占比:{:.2%}'.format(
            len(buys),
            len(buys) / len(_data), len(sells),
            len(sells) / len(_data)))
    if kwargs.pop('show_report', False):
        print(
            bt.report(show_history=kwargs.pop('show_history', False),
                      **kwargs))
    if kwargs.pop('plot', False):
        plot_backtest(_data,
                      x='date',
                      y='close',
                      buy=list(buys),
                      sell=list(sells))
    return bt, _data, buys, sells


def BACKTEST_SINGLE(symbol,
                    data=None,
                    buy_query='',
                    sell_query='',
                    sim_callbacks=[],
                    **kwargs):
    """单支股票的回测计算。默认包含先调用 `sim_callbacks` 进行数据处理，
    再从 `buy_data` 中根据 `buy_query` 和 `sell_query` 产生买入卖出是几点，
    最后再进行回测计算。

    .. seealso::
        * :func:`BACKTEST_PACK` 多支股票的回测计算。

    Args:
        symbol:
        data:
        buy_query: 示例：'rsi_close_14>80'
        sell_query:
        sim_callbacks:
        show_detail: 打印买入，卖出占比。默认为 False
        show_report: 打印回测报告。默认为 False
        show_history: 打印成交明细。默认为 False
        plot: 绘图。默认为 False

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
    if kwargs.pop('show_detail', False):
        print('预计购买次数:{},占比:{:.2%}\n预计卖出次数:{},占比:{:.2%}'.format(
            len(buys),
            len(buys) / len(s.data), len(sells),
            len(sells) / len(s.data)))
    if kwargs.pop('show_report', False):
        print(
            bt.report(show_history=kwargs.pop('show_history', False),
                      **kwargs))
    if kwargs.pop('plot', False):
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
    buy_data = kwargs.pop('buy_data', data)
    for i in tqdm(range(times)):
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
    report = '测试起始资金 {}，总数据量 {} 随机抽取 {} 次买入点作为测试。'.format(
        init_cash, len(data), buy_times)
    report = report + \
             '\n测试区间：{}-{}'.format(data.iloc[0]['date'], data.iloc[-1]['date'])
    report = report + '\n测试{}次后，平均总价值:{}'.format(times, np.average(hs))
    report = report + '\n测试{}次后，平均总现金:{}'.format(times, np.average(cs))
    return report, hs, cs, hiss


def read_data_QFQ(symbol='600036') -> pd.DataFrame:
    """读取前复权数据"""
    # if not IN_COLAB:
    #     raise NotImplementedError()
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
    # if not IN_COLAB:
    #     raise NotImplementedError()
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
