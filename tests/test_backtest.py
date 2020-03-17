from datetime import date as dt
import numpy as np
import pandas as pd
import pytest
import datetime
from finance_tools_py.backtest import BackTest
from finance_tools_py.backtest import MinAmountChecker
from finance_tools_py.backtest import AllInChecker


@pytest.fixture
def init_global_data():
    pytest.global_code = '000001'
    pytest.global_data = pd.DataFrame({
        'code': [pytest.global_code for x in range(5)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 13.4, 15.3],
    })


def test_example_backtest_date(init_global_data):
    print(">>> from datetime import date as dt\n"
    ">>> data = pd.DataFrame({\n"
    ">>>     'code': ['000001' for x in range(5)],\n"
    ">>>     'date': [\n"
    ">>>         dt(1998, 1, 1),\n"
    ">>>         dt(1999, 1, 1),\n"
    ">>>         dt(2000, 1, 1),\n"
    ">>>         dt(2001, 1, 1),\n"
    ">>>         dt(2002, 1, 1)\n"
    ">>>     ],\n"
    ">>>     'close': [4.5, 7.9, 6.7, 13.4, 15.3]\n"
    ">>> })\n"
    ">>> data['date'] = pd.to_datetime(data['date'])\n"
    ">>> bt = BackTest(\n"
    ">>>     data,\n"
    ">>>     callbacks=[\n"
    ">>>         MinAmountChecker(\n"
    ">>>             buy_dict={\n"
    ">>>                 pytest.global_code:\n"
    ">>>                 data[data['date'] < '2000-1-1']['date'].dt.to_pydatetime()\n"
    ">>>             },\n"
    ">>>             sell_dict={\n"
    ">>>                 pytest.global_code:\n"
    ">>>                 data[data['date'] > '2000-1-1']['date'].dt.to_pydatetime()\n"
    ">>>             },\n"
    ">>>         )\n"
    ">>>     ])\n"
    ">>> bt.calc_trade_history()\n"
    ">>> bt.report())\n")

    data = pd.DataFrame({
        'code': ['000001' for x in range(5)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 13.4, 15.3]
    })
    data['date'] = pd.to_datetime(data['date'])
    bt = BackTest(
        data,
        callbacks=[
            MinAmountChecker(
                buy_dict={
                    pytest.global_code:
                    data[data['date'] < '2000-1-1']['date'].dt.to_pydatetime()
                },
                sell_dict={
                    pytest.global_code:
                    data[data['date'] > '2000-1-1']['date'].dt.to_pydatetime()
                },
            )
        ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    print(bt.report())


def test_backtest_calc(init_global_data):
    bt = BackTest(pytest.global_data,
                  callbacks=[
                      MinAmountChecker(
                          buy_dict={
                              pytest.global_code:
                              [dt(1999, 1, 1), dt(2001, 1, 1)]
                          },
                          sell_dict={
                              pytest.global_code:
                              [dt(2000, 1, 1), dt(2002, 1, 1)]
                          },
                      )
                  ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    print(bt.report())
    assert bt.available_hold_df.empty
    bt = BackTest(pytest.global_data,
                  callbacks=[
                      MinAmountChecker(
                          buy_dict={
                              pytest.global_code:
                              [dt(1999, 1, 1), dt(2001, 1, 1)]
                          },
                          sell_dict={pytest.global_code: [dt(2000, 1, 1)]},
                      )
                  ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    print(bt.report())
    assert not bt.available_hold_df.empty
    assert bt.available_hold_df[pytest.global_code] == 100


def test_backtest_calc_mutil(init_global_data):
    data = pd.DataFrame({
        'code': ['000001' for x in range(5)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 13.4, 15.3],
    })
    data = data.append(
        pd.DataFrame({
            'code': ['000002' for x in range(5)],
            'date': [
                dt(1998, 12, 31),
                dt(1999, 12, 31),
                dt(2000, 12, 31),
                dt(2001, 12, 31),
                dt(2002, 12, 31)
            ],
            'close': [41.5, 71.9, 61.7, 131.4, 151.3],
        }))

    bt = BackTest(
        data,
        callbacks=[
            MinAmountChecker(
                buy_dict={
                    '000001': [dt(1999, 1, 1), dt(2001, 1, 1)],
                    '000002': [dt(1998, 12, 31)]
                },
                sell_dict={'000001': [dt(2000, 1, 1),
                                      dt(2002, 1, 1)]},
            )
        ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    assert '000001' not in bt.available_hold_df.index
    assert bt.available_hold_df['000002'] != 0
    assert not bt.available_hold_df.empty
    # hold_table=bt.hold_table()
    # assert 100==hold_table['000002']
    # assert 0==hold_table['000001']
    assert not bt.hold_price_cur.empty
    assert 41.5 == bt.hold_price_cur['000002'][0]
    assert 100 == bt.hold_price_cur['000002'][1]
    print(bt.report())
    bt = BackTest(data,
                  callbacks=[
                      MinAmountChecker(
                          buy_dict={
                              '000001': [dt(1999, 1, 1),
                                         dt(2001, 1, 1)],
                              '000002': [dt(1998, 12, 31)]
                          },
                          sell_dict={'000001': [dt(2000, 1, 1)]},
                      )
                  ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    assert not bt.available_hold_df.empty
    assert bt.available_hold_df['000001'] != 0
    assert bt.available_hold_df['000002'] != 0
    # hold_table=bt.hold_table()
    # assert 100==hold_table['000002']
    # assert 100==hold_table['000001']
    assert not bt.hold_price_cur.empty
    assert 41.5 == bt.hold_price_cur['000002'][0]
    assert 13.4 == bt.hold_price_cur['000001'][0]
    print(bt.report())
    print(bt.hold_time().to_string())


def test_backtest_holdprice(init_global_data):
    data = pd.DataFrame({
        'code': ['000001' for x in range(5)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 13.4, 15.3],
    })
    data = data.append(
        pd.DataFrame({
            'code': ['000002' for x in range(5)],
            'date': [
                dt(1998, 12, 31),
                dt(1999, 12, 31),
                dt(2000, 12, 31),
                dt(2001, 12, 31),
                dt(2002, 12, 31)
            ],
            'close': [41.5, 71.9, 61.7, 131.4, 151.3],
        }))
    bt = BackTest(
        data,
        init_cash=100000,
        callbacks=[
            MinAmountChecker(buy_dict={
                '000001': [dt(1999, 1, 1), dt(2001, 1, 1)],
                '000002':
                [dt(1999, 12, 31),
                 dt(2000, 12, 31),
                 dt(2002, 12, 31)]
            },
                            sell_dict={})
        ])
    bt.calc_trade_history()
    print(bt.report())
    assert 200 == bt.hold_price_cur['000001'][1]
    assert np.round((7.9 + 13.4) / 2,
                    2) == np.round(bt.hold_price_cur['000001'][0], 2)
    assert 300 == bt.hold_price_cur['000002'][1]
    assert np.round((71.9 + 61.7 + 151.3) / 3,
                    2) == np.round(bt.hold_price_cur['000002'][0], 2)
    assert bt.total_assets_cur == bt.available_cash + (7.9 + 13.4 + 71.9 +
                                                       61.7 + 151.3) * 100


def test_example():
    data = pd.DataFrame({
        'code': ['000001' for x in range(4)],
        'date':
        [dt(1998, 1, 1),
         dt(1999, 1, 1),
         dt(2000, 1, 1),
         dt(2001, 1, 1)],
        'close': [4.5, 7.9, 6.7, 10],
    })
    bt = BackTest(data,
                  init_cash=1000,
                  callbacks=[
                      MinAmountChecker(buy_dict={
                          '000001': [dt(1998, 1, 1),
                                     dt(2000, 1, 1)]
                      },
                                      sell_dict={'000001': [dt(1999, 1, 1)]})
                  ])
    bt.calc_trade_history()
    print(bt.report())
    assert 100 == bt.hold_price_cur['000001'][1]
    assert np.round(6.7, 2) == np.round(bt.hold_price_cur['000001'][0], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + (6.7) * 100, 2)


def test_allin():

    data = pd.DataFrame({
        'code': ['000001' for x in range(4)],
        'date':
        [dt(1998, 1, 1),
         dt(1999, 1, 1),
         dt(2000, 1, 1),
         dt(2001, 1, 1)],
        'close': [4.5, 7.9, 6.7, 10],
    })
    bt = BackTest(
        data,
        init_cash=5000,
        callbacks=[
            AllInChecker(buy_dict={'000001': [dt(1998, 1, 1),
                                              dt(2000, 1, 1)]},
                         sell_dict={'000001': [dt(1999, 1, 1)]})
        ])
    bt.calc_trade_history()
    print(bt.report())
    assert 1200 == bt.hold_price_cur['000001'][1]
    assert np.round(6.7, 2) == np.round(bt.hold_price_cur['000001'][0], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + (6.7) * 1200, 2)
