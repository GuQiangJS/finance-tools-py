import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import clear_output
from finance_tools_py.backtest import BackTest
from finance_tools_py.simulation.callbacks import CallBack
from finance_tools_py.simulation.callbacks.talib import ATR
from finance_tools_py.simulation import Simulation
from finance_tools_py.backtest import Utils
import datetime
from finance_tools_py.backtest import TurtleStrategy
import traceback
from tqdm.auto import tqdm
import empyrical
import warnings
import copy
from finance_tools_py.calc import fluidity
from finance_tools_py.calc import position_unit

plt.rcParams['font.family'] = 'SimHei'


# IN_COLAB = 'google.colab' in sys.modules
#
# # if not IN_COLAB:
# #     logging.warning('Colab用。如果不是在Colab下可能会有各种各样的问题！！！')
#
#
def report_metrics(strategy_rets, benchmark_rets, factor_returns=0):
    """使用 `empyrical`_ 库计算各种常见财务风险和绩效指标。

    Args:
        strategy_rets (:py:class:`pandas.Series`): 策略收益。
        benchmark_rets (:py:class:`pandas.Series`): 基准收益。
        factor_returns : 计算 excess_sharpe 时使用，策略计算时使用`strategy_rets`作为`factor_returns`，
            当不存在`strategy_rets`时使用`factor_returns`。
            `factor_returns`参考 :py:func:`empyrical.excess_sharpe` 中的`factor_returns`参数的解释。

    Examples:
        >>> from finance_tools_py._jupyter_helper import report_metrics
        >>> import pandas as pd
        >>> rep = report_metrics(pd.Series([-0.01,0.04,0.03,-0.02]),
                                 pd.Series([0.04,0.05,0.06,0.07]))
        >>> print(rep)
                                  基准         策略
        最大回撤                0.000000  -0.020000
        年化收益           713630.025679  10.326756
        年度波动性               0.204939   0.467333
        夏普比率               67.629875   5.392302
        R平方                 0.994780   0.614649
        盈利比率                1.650602   2.081081
        excess_sharpe       4.260282  -1.317465
        年复合增长率         713630.025679  10.326756


    Returns:
        :py:class:`pandas.DataFrame`:

    .. _empyrical:
        http://quantopian.github.io/empyrical/

    """
    if not benchmark_rets.empty:
        max_drawdown_benchmark = empyrical.max_drawdown(benchmark_rets)
        annual_return_benchmark = empyrical.annual_return(benchmark_rets)
        annual_volatility_benchmark = empyrical.annual_volatility(
            benchmark_rets)
        sharpe_ratio_benchmark = empyrical.sharpe_ratio(benchmark_rets)
        stability_of_timeseries_benchmark = empyrical.stability_of_timeseries(
            benchmark_rets)
        tail_ratio_benchmark = empyrical.tail_ratio(benchmark_rets)
        excess_sharpe_benchmark = empyrical.excess_sharpe(
            benchmark_rets, factor_returns)
        cagr_benchmark = empyrical.cagr(benchmark_rets)
    else:
        max_drawdown_benchmark = None
        annual_return_benchmark = None
        annual_volatility_benchmark = None
        sharpe_ratio_benchmark = None
        stability_of_timeseries_benchmark = None
        tail_ratio_benchmark = None
        excess_sharpe_benchmark = None
        cagr_benchmark = None
    max_drawdown_strategy = empyrical.max_drawdown(strategy_rets)
    annual_return_strategy = empyrical.annual_return(strategy_rets)
    annual_volatility_strategy = empyrical.annual_volatility(strategy_rets)
    sharpe_ratio_strategy = empyrical.sharpe_ratio(strategy_rets)
    stability_of_timeseries_strategy = empyrical.stability_of_timeseries(
        strategy_rets)
    tail_ratio_strategy = empyrical.tail_ratio(strategy_rets)
    excess_sharpe_strategy = empyrical.excess_sharpe(
        strategy_rets,
        benchmark_rets if not benchmark_rets.empty else factor_returns)
    cagr_strategy = empyrical.cagr(strategy_rets)

    return pd.DataFrame(
        {
            '基准': [
                max_drawdown_benchmark, annual_return_benchmark,
                annual_volatility_benchmark, sharpe_ratio_benchmark,
                stability_of_timeseries_benchmark, tail_ratio_benchmark,
                excess_sharpe_benchmark, cagr_benchmark
            ],
            '策略': [
                max_drawdown_strategy, annual_return_strategy,
                annual_volatility_strategy, sharpe_ratio_strategy,
                stability_of_timeseries_strategy, tail_ratio_strategy,
                excess_sharpe_strategy, cagr_strategy
            ]
        },
        index=[
            '最大回撤', '年化收益', '年度波动性', '夏普比率', 'R平方', '盈利比率', 'excess_sharpe',
            '年复合增长率'
        ])

    # return s
    # if not benchmark_rets.empty:
    #     print('标准最大回撤:{:.2%}'.format(empyrical.max_drawdown(benchmark_rets)))
    # print('策略最大回撤:{:.2%}'.format(empyrical.max_drawdown(strategy_rets)))
    # if not benchmark_rets.empty:
    #     print('标准年化收益：{:.2%}'.format(empyrical.annual_return(benchmark_rets)))
    # print('策略年化收益：{:.2%}'.format(empyrical.annual_return(strategy_rets)))
    # if not benchmark_rets.empty:
    #     print('标准年度波动性：{:.2%}'.format(empyrical.annual_volatility(benchmark_rets)))
    # print('策略年度波动性：{:.2%}'.format(empyrical.annual_volatility(strategy_rets)))
    # if not benchmark_rets.empty:
    #     print('标准夏普比率：{:.2f}'.format(empyrical.sharpe_ratio(benchmark_rets)))
    # print('策略夏普比率：{:.2f}'.format(empyrical.sharpe_ratio(strategy_rets)))
    # print('标准alpha：{:.2f}，beta：{:.2f}'.format(empyrical.alpha_beta(benchmark_rets,0)))
    # print('策略alpha：{:.2f}，beta：{:.2f}'.format(empyrical.alpha_beta(strategy_rets,0)))
    # if not benchmark_rets.empty:
    #     print('标准R平方：{:.2f}'.format(empyrical.stability_of_timeseries(benchmark_rets)))
    # print('策略R平方：{:.2f}'.format(empyrical.stability_of_timeseries(strategy_rets)))
    # if not benchmark_rets.empty:
    #     print('标准盈利比率：{:.2f}'.format(empyrical.tail_ratio(benchmark_rets)))
    # print('策略盈利比率：{:.2f}'.format(empyrical.tail_ratio(strategy_rets)))
    # print('>> 盈利比率：确定右（95％）和左尾巴（5％）之间的比率。 例如，比率0.25意味着损失是利润的四倍。')
    # if not benchmark_rets.empty:
    #     print('标准信息风险：{:.2f}'.format(empyrical.excess_sharpe(benchmark_rets, 0)))
    # print('策略信息风险：{:.2f}'.format(empyrical.excess_sharpe(strategy_rets, 0)))
    # if not benchmark_rets.empty:
    #     print('信息风险：{:.2f}'.format(empyrical.excess_sharpe(strategy_rets, benchmark_rets)))
    # print(
    #     '>> 信息风险，也被称为评价比。它代表投资者每增加单位风险所获得的额外收益。\n它通常用于评估共同基金，对冲基金等经理人的技能。它衡量经理人投资组合的有效收益除以经理人相对于基准所承担的风险量。信息比率越高，给定承担的风险数量，投资组合的有效收益就越高，管理者也越好\n信息比率与夏普比率类似，主要区别在于，夏普比率使用无风险收益作为基准（例如美国国库券），而信息比率使用风险指数作为基准（例如S＆P500） 。'
    # )
    # if not benchmark_rets.empty:
    #     print('标准年复合增长率：{:.2%}'.format(empyrical.cagr(benchmark_rets)))
    # print('策略年复合增长率：{:.2%}'.format(empyrical.cagr(strategy_rets)))

    # return empyrical.aggregate_returns(
    #     benchmark_rets, convert_to='yearly').to_frame().rename(columns={
    #         'rets_log': '标准年回报'
    #     }).join(
    #         empyrical.aggregate_returns(
    #             strategy_rets,
    #             convert_to='yearly').to_frame().rename(columns={0: '策略年回报'}))


# def __plot_BACKTEST_bar(v, title):
#     for index, i in enumerate(v.items()):
#         plt.bar(x=index, height=i[1], label=i[0])
#     plt.legend()
#     plt.title(title)
#
#
# def SIMULATE_DATA(data, callback=[], **kwargs):
#     """循环处理所有数据，循环按照 `callback` 的回测集合对所有股票分别进行回测处理后再合并返回
#
#     Args:
#         clear_output (bool): 清除输出。默认True。
#     """
#     dfs = []
#     for symbol in tqdm(data['code'].unique(), desc='处理数据中...'):
#         s = Simulation(data[data['code'] == symbol].sort_values('date'),
#                        symbol,
#                        callbacks=callback)
#         s.simulate()
#         s.data['code'] = symbol
#         dfs.append(s.data)
#     sim_data = pd.concat(dfs)
#     sim_data.sort_values(['date', 'code'], inplace=True)
#     if kwargs.get('clear_output', True):
#         clear_output(True)
#     return sim_data
#
#
# def __BACKTEST(data,
#                zs_data,
#                callback=[],
#                buy_start='2018-01-01',
#                buy_end='2018-12-31',
#                **kwargs):
#     """
#
#     Args:
#         data:
#         zs_data:
#         callback:
#         buy_start:
#         buy_end:
#         clear_output (bool): 清除输出。默认True。
#
#     Returns:
#
#     """
#     sim_data = SIMULATE_DATA(data, callback, **kwargs)
#
#     #取买入卖出点的计算数据
#     bs_data = sim_data[(sim_data['date'] >= buy_start)
#                        & (sim_data['date'] <= buy_end)]
#
#     #计算买入/卖出点...
#     buys = bs_data[bs_data['opt'] == 1].groupby('code')['date'].apply(
#         lambda x: x.dt.to_pydatetime()).to_dict()
#     sells = bs_data[bs_data['opt'] == -1].groupby('code')['date'].apply(
#         lambda x: x.dt.to_pydatetime()).to_dict()
#
#     bt, bs_data, bt_buy, bt_sell = __BACKTEST_PACK_CORE(sim_data=sim_data,
#                                                         buys=buys,
#                                                         sells=sells,
#                                                         **kwargs)
#     if kwargs.get('clear_output', True):
#         clear_output(True)
#     print("可买入时间：{}~{}".format(buy_start, buy_end))
#     print(bt.report(
#         show_history=False,
#         show_hold=False,
#     ))
#
#     baseline = data.groupby('code').apply(
#         lambda df: df.iloc[-1]['close'] / df.iloc[0]['close']).mean()
#     name = kwargs.pop('name', '')
#     __plot_BACKTEST_bar(
#         {
#             "沪深300": zs_data.iloc[-1]['close'] / zs_data.iloc[0]['close'],
#             "BaseLine": baseline,
#             name: bt.total_assets_cur / bt.init_cash
#         }, name)
#
#     return bt, bs_data
#
#
# def BACKTEST_PACK_YEAR(data, zs_data, year, sim_callbacks, **kwargs):
#     """按照年度回测数据
#
#     Args:
#         data: 待回测的数据。
#         hs_data： 指数相关数据。与 `data` 匹配。
#         sim_callbacks: 回测时使用的回调集合。
#         year: 年度
#         name:
#
#     See Also:
#         * :func:`BACKTEST_PACK_ALL` 跨年度回测数据。
#
#     Example:
#         >>> from finance_tools_py.simulation.callbacks.talib import MFI
#         >>> qfq_datas=pd.DataFrame() #所有股票日线数据
#         >>> hs_300_data=pd.DataFrame() #沪深300指数日线数据
#         >>> class CB(CallBack):
#         >>>     def __init__(self, t, v1, v2):
#         >>>         self.t = t
#         >>>         self.v1 = v1
#         >>>         self.v2 = v2
#         >>>     def on_preparing_data(self, data, **kwargs):
#         >>>         data['opt'] = 0
#         >>>         data.loc[data['mfi_{}'.format(self.t)] < self.v1, 'opt'] = 1
#         >>>         data.loc[data['mfi_{}'.format(self.t)] > self.v2, 'opt'] = -1
#         >>>
#         >>> BACKTEST_PACK_YEAR(qfq_datas,
#         >>>                    hs_300_data,
#         >>>                    2015,
#         >>>                    [MFI(14), CB(14, 20, 80)],
#         >>>                    name='2015年度比较')
#         可买入时间：2015-01-01~2015-12-31
#         数据时间:2015-01-05 00:00:00~2015-12-31 00:00:00（可交易天数244）
#         初始资金:10000.00
#         交易次数:170 (买入/卖出各算1次)
#         可用资金:1402.50
#         当前总资产:12135.85(现金+持股现价值)
#         资金变化率:14.03%
#         资产变化率:121.36%
#         总手续费:850.54
#         总印花税:138.15
#     """
#     start = '{0}-01-01'.format(year)
#     end = '{0}-12-31'.format(year)
#     __BACKTEST(data[(data['date'] >= start)
#                     & (data['date'] <= end)],
#                zs_data[(zs_data['date'] >= start)
#                        & (zs_data['date'] <= end)],
#                callback=sim_callbacks,
#                buy_start=start,
#                buy_end=end,
#                **kwargs)
#
#
# def BACKTEST_PACK_ALL(data,
#                       zs_data,
#                       sim_callbacks,
#                       start_year=2005,
#                       end_year=2019,
#                       **kwargs):
#     """跨年度回测数据
#
#     See Also:
#         * :func:`BACKTEST_PACK_YEAR` 按照年度回测数据。
#
#     Args:
#         data: 待回测的数据。
#         zs_data: 指数相关数据。与 `data` 匹配。
#         sim_callbacks: 回测时使用的回调集合。
#         start_year: 开始年度
#         end_year: 结束年度
#         name:
#         clear_output (bool): 清除输出。默认True。
#
#     Example:
#         >>> from finance_tools_py.simulation.callbacks.talib import MFI
#         >>> qfq_datas=pd.DataFrame() #所有股票日线数据
#         >>> hs_300_data=pd.DataFrame() #沪深300指数日线数据
#         >>> class CB(CallBack):
#         >>>     def __init__(self, t, v1, v2):
#         >>>         self.t = t
#         >>>         self.v1 = v1
#         >>>         self.v2 = v2
#         >>>     def on_preparing_data(self, data, **kwargs):
#         >>>         data['opt'] = 0
#         >>>         data.loc[data['mfi_{}'.format(self.t)] < self.v1, 'opt'] = 1
#         >>>         data.loc[data['mfi_{}'.format(self.t)] > self.v2, 'opt'] = -1
#         >>>
#         >>> BACKTEST_PACK_ALL(qfq_datas,
#         >>>                   hs_300_data,
#         >>>                   [MFI(14), CB(14, 20, 80)],
#         >>>                   name='2015年度比较')
#     """
#     start = '{0}-01-01'.format(start_year)
#     end = '{0}-12-31'.format(end_year)
#     __BACKTEST(data[(data['date'] >= start)
#                     & (data['date'] <= end)],
#                zs_data[(zs_data['date'] >= start)
#                        & (zs_data['date'] <= end)],
#                callback=sim_callbacks,
#                buy_start=start,
#                buy_end=end,
#                **kwargs)
#
#
# class Checker(AllInChecker):
#     """测试用回测CallBack。每次最多买1/5，当价格超过持仓成本的15%时卖出"""
#     def on_calc_buy_amount(self, date: datetime.datetime.timestamp, code: str,
#                            price: float, cash: float) -> float:
#         # 每次最多买1/5
#         return super().on_calc_buy_amount(date, code, price, cash * 0.2)
#
#     def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
#                       price: float, cash: float, hold_amount: float,
#                       hold_price: float) -> bool:
#         """当 `date` 及 `code` 包含在参数 :py:attr:`sell_dict` 中时返回 `True` 。否则返回 `False` 。"""
#         if code in self.sell_dict.keys() and date in self.sell_dict[code]:
#             return True
#         """当价格超过持仓成本的15%时卖出"""
#         if hold_amount > 0 and hold_price * 1.15 < price:
#             return True
#         return False
#
#
# def plot_basic(symbol, data=None, sim_callbacks=[], ys=[], **kwargs):
#     """绘制收盘价与指标数据的分列图，每个数据一行。一并调用plotly和seaborn绘图。"""
#     figsize = kwargs.pop('figsize', (15, len(ys) * 3))
#     plot_basic_seaborn(symbol,
#                        data,
#                        sim_callbacks=sim_callbacks,
#                        ys=ys,
#                        figsize=figsize)
#
#
def plot_basic_plotly(symbol, data=None, ys=[], **kwargs):
    """绘制收盘价与指标数据的图。可以绘制买入/卖出点。

    Args:
        symbol: 股票代码。
        data: 待绘制的数据。
        ys: 绘制的数据。默认应该至少需要包含1个。
        figsize: 默认宽度为15，高度为 `len(ys)*3)`
        x: x轴。默认为 `date`。
        y: y轴。默认为 `close`。
        buy: 购买时间集合。
        sell: 卖出时间集合。

    Returns:

    """
    # if data is None:
    #     data = read_data_QFQ(symbol)
    #     s = Simulation(data, symbol, callbacks=sim_callbacks)
    #     s.simulate()
    #     data = s.data
    buy = kwargs.pop('buy', [])
    sell = kwargs.pop('sell', [])
    x = kwargs.pop('x', 'date')
    y = kwargs.pop('y', 'close')
    fig = go.Figure()
    for yt in ys:
        fig.add_trace(go.Scatter(x=data[x], y=data[yt], mode='lines', name=yt))
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
    plt.suptitle(symbol)
    fig.show()


def plot_basic_seaborn(symbol, data=None, ys=[], **kwargs):
    """绘制收盘价与指标数据的分列图，每个数据一行。

    Args:
        symbol: 股票代码。
        data: 待绘制的数据。
        ys: 绘制的数据。默认应该至少需要包含1个。
        x: x轴。默认为 `date`。
        figsize: 默认宽度为15，高度为 `len(ys)*3)`

    Returns:

    """
    figsize = kwargs.pop('figsize', (15, len(ys) * 3))
    x = kwargs.pop('x', 'date')
    # if data is None:
    #     data = read_data_QFQ(symbol)
    #     s = Simulation(data, symbol, callbacks=sim_callbacks)
    #     s.simulate()
    #     data = s.data
    if len(ys) > 1:
        fig, axes = plt.subplots(len(ys), 1, figsize=figsize)
        for index, y in enumerate(ys):
            sns.lineplot(data=data, x=x, y=y, ax=axes[index])
    else:
        fig = plt.figure(figsize=figsize)
        sns.lineplot(data=data, x=x, y=ys[0])
    fig.suptitle('{} 数据预览'.format(symbol))
    plt.show()


#
#
# def __BACKTEST_PACK_CORE(**kwargs):
#     """多支支股票的回测计算。
#
#     Args:
#         sim_data: 所有处理后的数据。包含这个值以后，不再使用 `ori_data`。如果这个值为 None ，则会根据 `sim_callbacks` 中的回调定义对 `ori_data` 进行处理。
#         ori_data: 所有原始数据。包含多支不同的股票。
#         buy_sell_data: 买入卖出计算数据。默认使用 `data` 的值。如果传入字符串则从 `sim_data` 中根据条件取值。
#         buys: 可以是字符串，示例：'rsi_close_14>80'。如果是字符串则会自动从 `buy_sell_data` 中筛选。也可以是字典类型，示例:{'000002':[datetime,datetime]}。如果是字典类型则无需传入 `buy_sell_data`。
#         sells: 参考 `buys`。
#         sim_callbacks: 附加数据时的回调。只有当 `sim_data` 为空时才有用。
#         show_detail: 打印买入，卖出占比。默认为False
#         show_report: 打印回测报告。默认为False
#         show_history: 打印成交明细。默认为False
#         plot: 绘图。默认为False
#         clear_output (bool): 清除输出。默认True。
#
#     Returns:
#         backtest实例，数据，买入时间集合，卖出时间集合
#
#     """
#     dfs = []
#
#     ori_data = kwargs.pop('ori_data', None)
#     sim_data = kwargs.pop('sim_data', None)
#     sim_callbacks = kwargs.pop('sim_callbacks', [])
#     buys = kwargs.pop('buys', {})
#     sells = kwargs.pop('sells', {})
#
#     if sim_data is None and ori_data is None:
#         raise ValueError()
#     if sim_data is None:
#         _data = SIMULATE_DATA(ori_data, sim_callbacks)
#     else:
#         _data = sim_data
#     buy_sell_data = kwargs.pop('buy_sell_data', _data)
#     #     _print_buy=False
#     #     _print_sell=False
#     if isinstance(buy_sell_data, str):
#         buy_sell_data = _data.loc[_data.query(buy_sell_data)]
#     if isinstance(buys, str):
#         bq = str(buys)
#         #         _print_buy=True
#         buys = {}
#         for symbol in tqdm(buy_sell_data['code'].unique(), desc='计算买入点...'):
#             buys[symbol] = buy_sell_data[buy_sell_data['code'] ==
#                                          symbol].query(
#                                              bq)['date'].dt.to_pydatetime()
#     if isinstance(sells, str):
#         #         _print_sell=True
#         sq = str(sells)
#         for symbol in tqdm(buy_sell_data['code'].unique(), desc='计算卖出点...'):
#             sells[symbol] = buy_sell_data[buy_sell_data['code'] ==
#                                           symbol].query(
#                                               sq)['date'].dt.to_pydatetime()
#     bt = BackTest(_data, callbacks=[Checker(buys, sells)])
#     bt.calc_trade_history()
#     if kwargs.get("clear_output", True):
#         clear_output(True)
#     #     print('\x1b[1;31m{} 回测测试\x1b[0m\n买入条件:{}\n卖出条件:{}'.format(
#     #         symbol, buy_query, sell_query))
#     #     print('-----------------------------------------------')
#     if kwargs.pop('show_detail', False):
#         print('预计购买次数:{},占比:{:.2%}\n预计卖出次数:{},占比:{:.2%}'.format(
#             len(buys),
#             len(buys) / len(_data), len(sells),
#             len(sells) / len(_data)))
#     if kwargs.pop('show_report', False):
#         print(
#             bt.report(show_history=kwargs.pop('show_history', False),
#                       **kwargs))
#     if kwargs.pop('plot', False):
#         plot_backtest(_data,
#                       x='date',
#                       y='close',
#                       buy=list(buys),
#                       sell=list(sells))
#     return bt, _data, buys, sells
#
#
# def BACKTEST_SINGLE(symbol,
#                     data=None,
#                     buy_query='',
#                     sell_query='',
#                     sim_callbacks=[],
#                     **kwargs):
#     """单支股票的回测计算。默认包含先调用 `sim_callbacks` 进行数据处理，
#     再从 `buy_data` 中根据 `buy_query` 和 `sell_query` 产生买入卖出是几点，
#     最后再进行回测计算。
#
#     .. seealso::
#         * :func:`__BACKTEST_PACK_CORE` 多支股票的回测计算。
#
#     Args:
#         symbol:
#         data:
#         buy_query: 示例：'rsi_close_14>80'
#         sell_query:
#         sim_callbacks:
#         show_detail: 打印买入，卖出占比。默认为 False
#         show_report: 打印回测报告。默认为 False
#         show_history: 打印成交明细。默认为 False
#         plot: 绘图。默认为 False
#         clear_output (bool): 清除输出。默认True。
#
#     Returns:
#         backtest实例，数据，买入时间集合，卖出时间集合
#
#     """
#     if data is None or data.empty:
#         data = read_data_QFQ(symbol)
#         data['code'] = symbol
#     s = Simulation(data, symbol, callbacks=sim_callbacks)
#     s.simulate()
#     s.data['code'] = symbol
#     buys = []
#     sells = []
#     if buy_query:
#         buys = s.data.query(buy_query)['date'].dt.to_pydatetime()
#     if sell_query:
#         sells = s.data.query(sell_query)['date'].dt.to_pydatetime()
#     bt = BackTest(s.data, callbacks=[Checker({symbol: buys}, {symbol: sells})])
#     bt.calc_trade_history()
#     if kwargs.get("clear_output", True):
#         clear_output(True)
#     print('\x1b[1;31m{} 回测测试\x1b[0m\n买入条件:{}\n卖出条件:{}'.format(
#         symbol, buy_query, sell_query))
#     print('-----------------------------------------------')
#     if kwargs.pop('show_detail', False):
#         print('预计购买次数:{},占比:{:.2%}\n预计卖出次数:{},占比:{:.2%}'.format(
#             len(buys),
#             len(buys) / len(s.data), len(sells),
#             len(sells) / len(s.data)))
#     if kwargs.pop('show_report', False):
#         print(
#             bt.report(show_history=kwargs.pop('show_history', False),
#                       **kwargs))
#     if kwargs.pop('plot', False):
#         plot_backtest(s.data,
#                       x='date',
#                       y='close',
#                       buy=list(buys),
#                       sell=list(sells))
#     return bt, s.data, buys, sells
#
#
# def RANDMON_TEST_BASIC(data, times=100, buy_times=50, **kwargs):
#     """随机执行 `times` 次回测。默认调用 :class:`Checker` 来执行回测。
#
#     Args:
#         data: 所有股票完整数据
#         times: 随机执行总次数
#         buy_times: 从所有数据中随机选择购买的次数。
#         clear_output: 执行完成后清除报告。默认为True。
#         init_cash: 初始资金。默认50000.
#         buy_data: 计算买入时间点的数据集。默认为 `data`。其中最少需要包含 `date` 和 `code` 列。
#
#     Returns:
#         报告,所有测试的总价值集合,所有测试的剩余现金集合,所有成交明细集合
#     """
#     hs = []  # 总价值
#     cs = []  # 可用资金
#     hiss = []  # 交易明细
#
#     init_cash = kwargs.pop('init_cash', 50000)
#     buy_data = kwargs.pop('buy_data', data)
#     for i in tqdm(range(times)):
#         buys = buy_data.iloc[np.random.choice(
#             len(buy_data),
#             buy_times)].sort_values('date').groupby('code')['date'].apply(
#                 lambda g: g.dt.to_pydatetime()).to_dict()
#
#         bt = BackTest(data, init_cash=init_cash, callbacks=[Checker(buys, {})])
#         bt.calc_trade_history(**kwargs)
#         hs.append(bt.total_assets_cur)
#         cs.append(bt.available_cash)
#         hiss.append(bt.history_df)
#     if kwargs.get("clear_output", True):
#         clear_output(True)
#     report = '测试起始资金 {}，总数据量 {} 随机抽取 {} 次买入点作为测试。'.format(
#         init_cash, len(data), buy_times)
#     report = report + \
#              '\n测试区间：{}-{}'.format(data.iloc[0]['date'], data.iloc[-1]['date'])
#     report = report + '\n测试{}次后，平均总价值:{}'.format(times, np.average(hs))
#     report = report + '\n测试{}次后，平均总现金:{}'.format(times, np.average(cs))
#     return report, hs, cs, hiss
#
#
# def read_data_QFQ(symbol='600036') -> pd.DataFrame:
#     """读取前复权数据"""
#     # if not IN_COLAB:
#     #     raise NotImplementedError()
#     data = pd.read_csv(
#         'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
#         format(symbol),
#         parse_dates=True,
#         usecols=[
#             'date', 'open_qfq', 'high_qfq', 'low_qfq', 'close_qfq',
#             'volume_qfq'
#         ])
#     data['date'] = pd.to_datetime(data['date'])
#     data.rename(columns={
#         'open_qfq': 'open',
#         'high_qfq': 'high',
#         'low_qfq': 'low',
#         'close_qfq': 'close',
#         'volume_qfq': 'volume'
#     },
#                 inplace=True)
#     # data['preclose']=data['close'].shift()
#     # data['nextclose']=data['close'].shift(-1)
#     # data['nextchange']=data['nextclose']-data['close']
#     # data['nextchange_sign']=np.sign(data['nextchange'])
#     return data
#
#
# def read_data_HFQ(symbol='600036') -> pd.DataFrame:
#     """读取后复权数据"""
#     # if not IN_COLAB:
#     #     raise NotImplementedError()
#     data = pd.read_csv(
#         'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
#         format(symbol),
#         parse_dates=True,
#         usecols=[
#             'date', 'open_hfq', 'high_hfq', 'low_hfq', 'close_hfq',
#             'volume_hfq'
#         ])
#     data['date'] = pd.to_datetime(data['date'])
#     data.rename(columns={
#         'open_hfq': 'open',
#         'high_hfq': 'high',
#         'low_hfq': 'low',
#         'close_hfq': 'close',
#         'volume_hfq': 'volume'
#     },
#                 inplace=True)
#     # data['preclose']=data['close'].shift()
#     # data['nextclose']=data['close'].shift(-1)
#     # data['nextchange']=data['nextclose']-data['close']
#     # data['nextchange_sign']=np.sign(data['nextchange'])
#     return data
#
#
# def plot_backtest(data, x, y, buy=None, sell=None):
#     if isinstance(y, str):
#         y = [y]
#     try:
#         plot_backtest_plotly(data, x, y, buy, sell).show()
#     except:
#         traceback.print_exc()
#     try:
#         plot_backtest_seaborn(data, x, y, buy, sell)
#         plt.legend()
#         plt.show()
#     except:
#         traceback.print_exc()
#
#
# def plot_backtest_plotly(data, x, y, buy=None, sell=None, col='close'):
#     """使用plotly绘制回测后的数据，数据上会标记买入点和卖出点"""
#     if isinstance(y, str):
#         y = [y]
#     fig = go.Figure()
#     for y1 in y:
#         fig.add_trace(go.Scatter(x=data[x], y=data[y1], mode='lines', name=y1))
#     if buy:
#         b = data[data[x].isin(buy)]
#         fig.add_trace(
#             go.Scatter(x=b[x],
#                        y=b[col],
#                        mode='markers',
#                        name='buy',
#                        marker=dict(color="red", size=6)))
#     if sell:
#         b = data[data[x].isin(sell)]
#         fig.add_trace(
#             go.Scatter(x=b[x],
#                        y=b[col],
#                        mode='markers',
#                        name='sell',
#                        marker=dict(color="green", size=6)))
#     return fig
#
#
# def plot_backtest_seaborn(data,
#                           x,
#                           y,
#                           buy=None,
#                           sell=None,
#                           figsize=(20, 6),
#                           col='close'):
#     """使用seaborn绘制回测后的数据，数据上会标记买入点和卖出点"""
#     if isinstance(y, str):
#         y = [y]
#     fig = plt.figure(figsize=figsize)
#     for y1 in y:
#         sns.lineplot(data=data, x=x, y=y1, c='#4281C0', label=y1)
#     if buy:
#         b = data[data[x].isin(buy)]
#         plt.plot(b[x], b[col], 'r.', label='buy')
#     if sell:
#         b = data[data[x].isin(sell)]
#         plt.plot(b[x], b[col], 'gx', label='sell')
#     return fig


def all_years_single_symbol(symbol,
                            fulldata,
                            cbs,
                            init_cash=10000,
                            start_year=2005,
                            end_year=2007,
                            verbose=2,
                            show_report=True,
                            show_plot=True,
                            show_history=False,
                            tb_kwgs={},
                            **kwargs):
    """逐年度对单一股票进行回测。

    采用 :py:class:`finance_tools_py.backtest.TurtleStrategy` 进行回测

    Args:
        fulldata (:py:class:`pandas.DataFrame`): 完整的原始数据。
            index[0]为股票代码,index[1]为日期。
        init_cash:
        start_year (int): 开始计算年份。
        end_year (int): 结束计算年份。
        cbs ([:py:class:`finance_tools_py.simulation.callbacks.CallBack`]): 对数据进行模拟填充时的回调。参考 :py:class:`finance_tools_py.simulation.Simulation` 中的`callbacks`参数。
        tb_kwgs (dict): :py:class:`finance_tools_py.backtest.TurtleStrategy` 的参数集合。

    Returns:
        - dict: BackTest字典。key值为年份。

        - dict: 回测用的数据源字典。key值为年份。

        - dict: 买点字典。key值为年份。

        - dict: 卖点字典。key值为年份。
    """
    hold = pd.DataFrame()
    report = {}
    datas = {}
    buys = {}
    sells = {}
    h = {}
    tb_kwgs_copy = copy.deepcopy(tb_kwgs)

    for year in tqdm(range(start_year, end_year)):
        df_symbol_year = fulldata[
            (fulldata.index.get_level_values(0) == symbol)
            & (fulldata.index.get_level_values(1) <= '{}-12-31'.format(year))]
        s = Simulation(df_symbol_year.reset_index(), symbol, callbacks=cbs)
        s.simulate()
        df_symbol_years = s.data
        df_symbol_years.sort_values('date', inplace=True)
        # 遍历股票，对每支股票进行数据处理-结束

        buy_dict = df_symbol_years[df_symbol_years['opt'] == 1].reset_index(
        ).groupby('code')['date'].apply(
            lambda x: x.dt.to_pydatetime()).to_dict()

        sell_dict = df_symbol_years[df_symbol_years['opt'] == 0].reset_index(
        ).groupby('code')['date'].apply(
            lambda x: x.dt.to_pydatetime()).to_dict()

        buys[year] = buy_dict
        sells[year] = sell_dict

        df_symbol_years = df_symbol_years[
            df_symbol_years['date'] >= '{}-01-01'.format(year)]

        datas[year] = df_symbol_years

        if verbose == 2:
            print('起止日期:{:%Y-%m-%d}~{:%Y-%m-%d}'.format(
                min(df_symbol_years['date']), max(df_symbol_years['date'])))
            #     print('数据量:{}'.format(len(df_symbol_years)))

        ts = TurtleStrategy(buy_dict=buy_dict,
                            sell_dict=sell_dict,
                            holds=h,
                            **tb_kwgs_copy)
        bt = BackTest(df_symbol_years,
                      init_cash=init_cash,
                      init_hold=hold,
                      live_start_date=datetime.datetime(year, 1, 1),
                      callbacks=[ts])
        bt.calc_trade_history(verbose=2)
        report[year] = bt

        h = ts.holds
        if h:
            hs = []
            for k, v in h.items():
                for v1 in v:
                    hs.append(
                        pd.DataFrame({
                            'code': [k],
                            'amount': [v1.amount],
                            'price': [v1.price],
                            'buy_date': [v1.date],
                            'stoploss_price': [v1.stoploss_price],
                            'stopprofit_price': [v1.stopprofit_price],
                            'next_price': [v1.next_price],
                        }))
            hold = pd.concat(hs) if hs else pd.DataFrame()

        init_cash = bt.available_cash
        if show_report:
            print(bt.report(show_history=show_history))
        if show_report or show_plot:
            rp = bt.profit_loss_df()
        if show_report:
            print(rp)
        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(10, 3))
            Utils.plt_win_rate(rp, ax=axes[0])
            Utils.plt_pnl_ratio(rp, ax=axes[1])
            plt.gcf().autofmt_xdate()
            plt.show()
    return report, datas, buys, sells


class _cache():
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.start = start
        self.end = end

    def __hash__(self):
        return self.symbol.__hash__() ^ self.start.__hash__(
        ) ^ self.end.__hash__()

    def __eq__(self, other):
        return self.symbol == other.symbol and self.start == other.start and self.end == other.end


def all_years(fulldata,
              cbs,
              init_cash=10000,
              start_year=2005,
              end_year=2020,
              lookback=1,
              verbose=2,
              show_report=True,
              show_plot=True,
              tb_kwgs={},
              top=10,
              show_history=False,
              **kwargs):
    """逐年度对流动性最大的n支股票进行回测。

    采用 :py:class:`finance_tools_py.backtest.TurtleStrategy` 进行回测

    Args:
        fulldata (:py:class:`pandas.DataFrame`): 完整的原始数据。
            index[0]为股票代码,index[1]为日期。
        init_cash:
        top (int): 选取流动性最大的n值股票。默认为10。
            流动性计算参考 :py:func:`finance_tools_py.calc.fluidity`
        start_year (int): 开始计算年份。
        end_year (int): 结束计算年份。
        lookback (int): 回看几年的数据，用来计算流动性。当lookback==1时，实际会回看
        cbs ([:py:class:`finance_tools_py.simulation.callbacks.CallBack`]): 对数据进行模拟填充时的回调。参考 :py:class:`finance_tools_py.simulation.Simulation` 中的`callbacks`参数。
        tb_kwgs (dict): :py:class:`finance_tools_py.backtest.TurtleStrategy` 的参数集合。
        unit_percent (float): 计算头寸单元时使用的基准，默认为1%。
        fixed_unit (bool): 是否使用固定金额（init_cash）作为计算头寸单元的标的。默认为True。
            如果为False的话，会在每年开始时，使用上一年度的总资产（:py:attr:`finance_tools_py.backtest.BackTest.total_assets_cur`）结合`unit_percent`进行运算。
            如果是第一年则使用`init_cash`结合`unit_percent`进行运算。

    Returns:
        - dict: BackTest字典。key值为年份。

        - dict: 回测用的数据源字典。key值为年份。

        - dict: 买点字典。key值为年份。

        - dict: 卖点字典。key值为年份。
    """
    hold = pd.DataFrame()
    report = {}
    datas = {}
    buys = {}
    sells = {}
    h = {}
    tb_kwgs_copy = copy.deepcopy(tb_kwgs)
    baseValue = init_cash * kwargs.get('unit_percent', 0.01)  #计算头寸单元时使用的基准
    lookbacks = []
    years = []
    lookback = lookback - 1
    for i in range(start_year, end_year):
        if i + lookback + 1 <= end_year:
            lookbacks.append([i, i + lookback])
            years.append(i + lookback + 1)

    if verbose == 2:
        for lookback, year in zip(lookbacks, years):
            print(lookback, year)

    _top_dict = {}
    _every_year_dict = {}

    if 'symbol' not in fulldata.columns:
        fulldata['symbol']=fulldata.index.get_level_values(0)
    if 'datetime' not in fulldata.columns:
        fulldata['datetime']=fulldata.index.get_level_values(1)

    for look, year in tqdm(zip(lookbacks, years)):
        # 取 year 年的n支流动性最大的股票-开始
        year_df = fulldata[
            (fulldata['datetime'] <= datetime.date(look[-1],12,31))
            &
            (fulldata['datetime'] >= datetime.date(look[0],1,1))]
        #
        # year_df = fluidity(year_df)
        #
        # #计算所有的头寸单元
        # year_df.dropna(inplace=True)
        # year_df['unit'] = year_df.apply(lambda row: int(position_unit(row['close'], row['atr_20'], baseValue)/100), axis=1)
        # year_df=year_df[year_df['unit']>0]
        # #计算所有的头寸单元
        #
        # top_year = year_df[:top] if top > 0 else year_df

        tb_kwgs_copy['min_amount'] = {}
        tb_kwgs_copy['max_amount'] = {}
        top_year = []
        for v in fluidity(year_df).index.values:
            c = _cache(v)
            _s_data = None
            if c not in _top_dict or _top_dict[c] is None:
                df_symbol = year_df[year_df['symbol'] == v]
                s = Simulation(df_symbol.reset_index(), v,
                               callbacks=[ATR(20)])  #TODO
                s.simulate()
                s.data.dropna(inplace=True)
                _s_data = s.data.copy()
                _top_dict[c] = _s_data.copy()
            else:
                _s_data = _top_dict[c]
            if _s_data.empty:
                continue
            _s_data['unit'] = _s_data.apply(lambda row: position_unit(
                row['close'], row[tb_kwgs_copy['colname']], baseValue),
                                            axis=1)
            m = int(_s_data.iloc[-1]['unit'] / 100) * 100
            if m > 0:
                tb_kwgs_copy['min_amount'][v] = m
                tb_kwgs_copy['max_amount'][v] = m * 4
                top_year.append(v)
            else:
                if verbose > 0:
                    print('{}-根据时间 {:%Y-%m-%d}~{:%Y-%m-%d} 计算头寸单位大小为0'.format(
                        v,
                        year_df['datetime'][0],
                        year_df['datetime'][-1]))
            if len(top_year) >= top:
                break

        ls = list(
            set(
                list(top_year) +
                list(hold['code'].unique() if not hold.empty else [])))
        if not ls:
            if verbose > 0:
                print('{}无任何可跟踪的股票'.format(year))
            continue

        # 取 year 年的10支流动性最大的股票-结束
        #     print('{}年的10支流动性最大的股票'.format(year))
        # 遍历股票，对每支股票进行数据处理-开始
        df_symbol_years = []
        for symbol in ls:
            c = _cache(symbol, look[0], year)
            _s_data = None
            if c not in _every_year_dict or _every_year_dict[c] is None:
                df_symbol_year = fulldata[
                    (fulldata['symbol'] == symbol)
                    & (fulldata['datetime'] <= datetime.date(year,12,31))
                    & (fulldata['datetime'] >= datetime.date(look[0],1,1))]
                s = Simulation(df_symbol_year.reset_index(),
                               symbol,
                               callbacks=cbs)
                s.simulate()
                _s_data = s.data.copy()
            else:
                _s_data = _every_year_dict[c]
            df_symbol_years.append(_s_data)
        df_symbol_years = pd.concat(df_symbol_years)
        df_symbol_years.sort_values('date', inplace=True)
        # 遍历股票，对每支股票进行数据处理-结束

        buy_dict = df_symbol_years[df_symbol_years['opt'] == 1].reset_index(
        ).groupby('code')['date'].apply(
            lambda x: x.dt.to_pydatetime()).to_dict()

        sell_dict = df_symbol_years[df_symbol_years['opt'] == 0].reset_index(
        ).groupby('code')['date'].apply(
            lambda x: x.dt.to_pydatetime()).to_dict()

        if not hold.empty:
            for onlysell in set(hold['code'].to_list()).difference(
                    set(top_year)):
                if onlysell in buy_dict:
                    del buy_dict[onlysell]

        buys[year] = buy_dict
        sells[year] = sell_dict

        df_symbol_years = df_symbol_years[
            df_symbol_years['date'] >= '{}-01-01'.format(year)]

        datas[year] = df_symbol_years

        if verbose == 2:
            print('起止日期:{:%Y-%m-%d}~{:%Y-%m-%d}'.format(
                min(df_symbol_years['date']), max(df_symbol_years['date'])))
        #     print('数据量:{}'.format(len(df_symbol_years)))

        ts = TurtleStrategy(buy_dict=buy_dict,
                            sell_dict=sell_dict,
                            holds=h,
                            **tb_kwgs_copy)
        bt = BackTest(df_symbol_years,
                      init_cash=init_cash,
                      init_hold=hold,
                      live_start_date=datetime.datetime(year, 1, 1),
                      callbacks=[ts])
        bt.calc_trade_history(verbose=verbose)
        report[year] = bt

        if not kwargs.get('fixed_unit', True):
            baseValue = bt.total_assets_cur * kwargs.get('unit_percent',
                                                         0.01)  # 计算头寸单元时使用的基准

        h = ts.holds
        if h:
            hs = []
            for k, v in h.items():
                for v1 in v:
                    hs.append(
                        pd.DataFrame({
                            'code': [k],
                            'amount': [v1.amount],
                            'price': [v1.price],
                            'buy_date': [v1.date],
                            'stoploss_price': [v1.stoploss_price],
                            'stopprofit_price': [v1.stopprofit_price],
                            'next_price': [v1.next_price],
                        }))
            hold = pd.concat(hs) if hs else pd.DataFrame()

        init_cash = bt.available_cash
        if show_report:
            print(bt.report(show_history=show_history))
        if show_report or show_plot:
            rp = bt.profit_loss_df()
        if show_report:
            print(rp)
        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(10, 3))
            Utils.plt_win_rate(rp, ax=axes[0])
            Utils.plt_pnl_ratio(rp, ax=axes[1])
            plt.gcf().autofmt_xdate()
            plt.show()
    df_profit = pd.concat([x.profit_loss_df() for x in report.values()])
    return df_profit, report, datas, buys, sells
