from finance_tools_py._jupyter_helper import report_metrics
from finance_tools_py._jupyter_helper import test_all_years
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
from finance_tools_py._jupyter_helper import test_all_years_single_symbol
from finance_tools_py._jupyter_helper import test_all_years
from finance_tools_py.calc import fluidity
from finance_tools_py.calc import position_unit

def test_example_metrics():
    rep = report_metrics(pd.Series([-0.012143, 0.045350, 0.030957, 0.004902]),
                         pd.Series([-0.112143, 0.145350, 0.130957, 0.104902]))
    print(rep)

def test_test_all_years():
    ret_datas = pd.read_csv(os.path.join(r'C:\Users\GuQiang\Documents\GitHub\StockTest\datas', 'qfq_2005_2_2020_rets.csv'),
                            index_col=None,
                            dtype={'code': str},
                            parse_dates=['date'])
    ret_datas.sort_values('date', inplace=True)
    ret_datas.set_index(['code', 'date'], inplace=True)

    report, datas, buys, sells = test_all_years(fulldata=ret_datas,
              cbs=[
        ATR(20),
        BBANDS(20, 2, 2),
        LINEARREG_SLOPE('close', 20),
        LINEARREG_SLOPE('bbands_20_2_2_mean', 20),
    ],
              init_cash=10000,
              start_year=2005,
              top=3,
              end_year=2020,
              lookback=1,
              verbose=2,
              show_report=True,
              show_plot=True,
              tb_kwgs={
                  'colname': 'atr_20',
                  'single_max': 400,
                  'min_amount': 100
              })