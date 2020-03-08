import os
import datetime
import traceback
from finance_tools_py.backtest import BackTest
from finance_tools_py.backtest import AHundredChecker
import pandas as pd
import pytest


@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                    reason="Skipping this test on Travis CI.")
def test_example():
    import QUANTAXIS as QA
    import talib
    list = QA.QA_fetch_get_stock_list('pytdx')
    list = list[:4]

    ## 合并所有股票一同回测

    print('Reading datas...')
    datas = {}
    for index, symbol in enumerate(list['code'].values):
        print('{}/{} {}:{}'.format(index + 1, len(list), symbol, datetime.datetime.now()))
        datas[symbol] = QA.QA_fetch_stock_day_adv(symbol, start='2006-01-01', end='2019-12-31')
    print('Datas readed.')

    result = {}
    codes = []
    values = []  # 总资产
    cashs = []  # 当前现金
    holds = []  # 持仓数量
    days = []  # 持仓时间

    buy_dict = {}
    sell_dict = {}

    print('Processing datas...')
    for index, (symbol, df) in enumerate(datas.items()):
        try:
            print('{}/{} {}:{}'.format(index + 1, len(datas), symbol, datetime.datetime.now()))
            df = QA.QA_fetch_stock_day_adv(symbol, start='2006-01-01', end='2019-12-31')
            if df and not df.data.empty and not df.to_qfq().data.empty:
                bbands = df.to_qfq().data.reset_index().copy()
                bbands['up'], bbands['mean'], bbands['low'] = talib.BBANDS(bbands['close'].values, timeperiod=30,
                                                                           nbdevup=2.8, nbdevdn=2.8)
                bbands['diff_up'] = bbands['up'] / bbands['close']
                bbands['diff_mean'] = bbands['mean'] / bbands['close']
                bbands['diff_low'] = bbands['low'] / bbands['close']

                bbands['opt'] = 0

                m1 = bbands['diff_up'].min() + bbands['diff_up'].std() * 0.2
                m2 = bbands['diff_low'].max() - bbands['diff_low'].std() * 0.2

                bbands.loc[bbands['diff_up'] < m1, 'opt'] = 1  # 卖出点
                bbands.loc[bbands['diff_low'] > m2, 'opt'] = 2  # 买入点
                bbands.loc[bbands['opt'] != 0][['date', 'close', 'opt']]
                point = bbands.loc[bbands['opt'] != 0][1:]

                buy_dict[symbol] = pd.DatetimeIndex(point.loc[point['opt'] == 2]['date'].values)
                sell_dict[symbol] = pd.DatetimeIndex(point.loc[point['opt'] == 1]['date'].values)

        except Exception as e:
            print(str(e))
            traceback.print_exc()
            continue
    print('Datas processed.')

    all_data = pd.concat([x.data for x in datas.values() if x is not None]).sort_index(level=0)

    bt = BackTest(all_data.reset_index(), 50000, callbacks=[AHundredChecker(buy_dict, sell_dict)])
    bt.calc_trade_history(verbose=2)
    print(bt.report())


@pytest.mark.skip(reason="性能测试用")
def test_sas():
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    test_example()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
