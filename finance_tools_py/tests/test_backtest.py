from datetime import date

import pandas as pd
import pytest

from finance_tools_py.backtest import BackTest


@pytest.fixture
def init_global_data():
    pytest.global_data = pd.DataFrame({
        'date': [date(1998, 1, 1), date(1999, 1, 1), date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1)],
        'close': [4.5, 7.9, 6.7, 13.4, 15.3]
    })


def test_backtest_calc(init_global_data):
    bt = BackTest(pytest.global_data)
    buysignal = [date(1999, 1, 1), date(2001, 1, 1)]
    sellsignal = [date(2000, 1, 1), date(2002, 1, 1)]
    bt.calc_trade_history(buysignal, sellsignal)
    assert not bt.history_df.empty
    assert bt.available_sell == 0
    print(bt.report())
    bt = BackTest(pytest.global_data)
    sellsignal = [date(2000, 1, 1)]
    bt.calc_trade_history(buysignal, sellsignal)
    assert not bt.history_df.empty
    assert bt.available_sell == 100
    print(bt.report())
