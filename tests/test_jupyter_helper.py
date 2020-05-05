from finance_tools_py._jupyter_helper import report_metrics
import pandas as pd
import os
import finance_tools_py
from finance_tools_py._jupyter_helper import report_metrics
from finance_tools_py.backtest import Utils
from finance_tools_py.backtest import Utils
from finance_tools_py.simulation import Simulation
from finance_tools_py.simulation.callbacks.talib import SMA
from finance_tools_py.simulation.callbacks import CallBack
from finance_tools_py.simulation.callbacks.talib import BBANDS
from finance_tools_py.simulation.callbacks.talib import ATR
from finance_tools_py.simulation.callbacks.talib import LINEARREG_SLOPE
from finance_tools_py._jupyter_helper import all_years_single_symbol
from finance_tools_py._jupyter_helper import all_years
from finance_tools_py.calc import fluidity
from finance_tools_py.calc import position_unit
import pytest
import numpy as np


def test_example_metrics():
    rep = report_metrics(pd.Series([-0.012143, 0.045350, 0.030957, 0.004902]),
                         pd.Series([-0.112143, 0.145350, 0.130957, 0.104902]))
    print(rep)


@pytest.mark.skip
def test_test_all_years():
    import numpy as np

    class CALC_OPT(CallBack):
        def on_preparing_data(self, data, **kwargs):
            data.dropna(inplace=True)
            data['opt'] = np.NaN
            data.loc[data['close'] > data['bbands_20_2_2_up'], 'opt'] = 1
            data.loc[data['close'] < data['bbands_20_2_2_low'], 'opt'] = 0
            if kwargs.pop('for_test', False):
                data['opt'].fillna(method='ffill', inplace=True)
                data['opt'].fillna(method='bfill', inplace=True)

    ret_datas = pd.read_csv(os.path.join(
        r'C:\Users\GuQiang\Documents\GitHub\StockTest\datas',
        'qfq_2005_2_2020_rets.csv'),
                            index_col=None,
                            dtype={'code': str},
                            parse_dates=['date'])
    ret_datas.sort_values('date', inplace=True)
    ret_datas.set_index(['code', 'date'], inplace=True)

    def t(**kwargs):
        all_years(**kwargs)

    for top in [
            3,
            5,
            # 10, 15, 20, 30, 35, 40, 50
    ]:
        for atr in [
                0.005,
                # 0.01, 0.02
        ]:
            for init_cash in [
                    10000,
                    # 50000,
                    # 100000
            ]:
                for max_hold in [
                        0,
                        20,
                        # 35,
                        # 51,
                        # 66,
                        # 120,
                        # 240,
                ]:  # 限定最大持仓天数
                    start_year = 2005  # 期间起(包含)
                    end_year = 2009  # 期间末(包含)
                    try:
                        t(
                            fulldata=ret_datas,
                            cbs=[
                                ATR(20),
                                BBANDS(20, 2, 2),
                                LINEARREG_SLOPE('close', 20),
                                LINEARREG_SLOPE('bbands_20_2_2_mean', 20),
                                CALC_OPT(),
                            ],
                            init_cash=init_cash,
                            start_year=start_year,
                            top=top,
                            end_year=end_year,
                            lookback=1,
                            verbose=1,
                            show_report=False,
                            show_history=False,
                            show_plot=False,
                            tb_kwgs={
                                'colname': 'atr_20',
                                'max_days': max_hold
                            },
                            clear=False,
                            fixed_unit=False,  # 每年年初动态调整持仓头寸计算基数
                            unit_percent=atr,
                        )
                    except:
                        raise


def test_cache():

    d = {}

    symbol = '123456'
    start = None
    end = None
    data = np.array([1, 2, 3, 4, 5])
    c1 = finance_tools_py._jupyter_helper._cache(symbol)
    d[c1] = data
    assert len(d) == 1
    c2 = finance_tools_py._jupyter_helper._cache(symbol, start, end)
    d[c2] = data
    assert len(d) == 1
    assert np.array_equal(np.array(d[c1]), np.array(d[c2]))
    c3 = finance_tools_py._jupyter_helper._cache(symbol, '123', '456')
    d[c3] = np.array([2, 3, 4, 5, 6])
    assert len(d) == 2
    assert not np.array_equal(np.array(d[c3]), np.array(d[c2]))


@pytest.mark.skip
def test_profile():
    import cProfile, pstats, io
    # from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    test_test_all_years()
    pr.disable()
    s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())
