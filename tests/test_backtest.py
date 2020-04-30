from datetime import date as dt
import numpy as np
import pandas as pd
import pytest
import datetime
from finance_tools_py.backtest import BackTest
from finance_tools_py.backtest import MinAmountChecker
from finance_tools_py.backtest import AllInChecker
from finance_tools_py.backtest import Utils
from finance_tools_py.backtest import TurtleStrategy
import os


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
    print(
        ">>> from datetime import date as dt\n"
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

def test_backtest_calc_sameday(init_global_data):
    bt = BackTest(pytest.global_data,
                  callbacks=[
                      MinAmountChecker(colname=None,
                          buy_dict={
                              pytest.global_code:
                              [dt(1999, 1, 1), dt(2001, 1, 1)]
                          },
                          sell_dict={
                              pytest.global_code:
                              [dt(2001, 1, 1), dt(2002, 1, 1)]
                          },
                      )
                  ])
    bt.calc_trade_history(verbose=2)
    assert bt.available_hold_df.empty
    assert 2==len(bt.history_df)

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
    assert bt._BackTest__get_buy_avg_price('000001') == (0.0, 0.0)
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
    print(bt.hold_time())
    print(bt.hold_price_cur_df)
    assert not bt.available_hold_df.empty
    assert bt.available_hold_df[pytest.global_code] == 100
    assert bt._BackTest__get_buy_avg_price('000001') == (13.4, 100.0)


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
    assert bt._BackTest__get_buy_avg_price('000001') == (0.0, 0.0)
    assert bt._BackTest__get_buy_avg_price('000002') == (41.5, 100.0)
    assert not bt.history_df.empty
    assert '000001' not in bt.available_hold_df.index
    assert bt.available_hold_df['000002'] != 0
    assert not bt.available_hold_df.empty
    # hold_table=bt.hold_table()
    # assert 100==hold_table['000002']
    # assert 0==hold_table['000001']
    assert not bt.hold_price_cur_df.empty
    assert 41.5 == bt.hold_price_cur_df.loc['000002']['buy_price']
    assert 100 == bt.hold_price_cur_df.loc['000002']['amount']
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
    assert bt._BackTest__get_buy_avg_price('000001') == (13.4, 100.0)
    assert bt._BackTest__get_buy_avg_price('000002') == (41.5, 100.0)
    # hold_table=bt.hold_table()
    # assert 100==hold_table['000002']
    # assert 100==hold_table['000001']
    assert not bt.hold_price_cur_df.empty
    assert 41.5 == bt.hold_price_cur_df.loc['000002']['buy_price']
    assert 13.4 == bt.hold_price_cur_df.loc['000001']['buy_price']
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
    assert bt._BackTest__get_buy_avg_price('000001') == np.average(
        [7.9, 13.4], weights=[100, 100], returned=True)
    assert bt._BackTest__get_buy_avg_price('000002') == np.average(
        [71.9, 61.7, 151.3], weights=[100, 100, 100], returned=True)
    assert 200 == bt.hold_price_cur_df.loc['000001']['amount']
    assert np.round(
        (7.9 + 13.4) / 2,
        2) == np.round(bt.hold_price_cur_df.loc['000001']['buy_price'], 2)
    assert 300 == bt.hold_price_cur_df.loc['000002']['amount']
    assert np.round(
        (71.9 + 61.7 + 151.3) / 3,
        2) == np.round(bt.hold_price_cur_df.loc['000002']['buy_price'], 2)
    assert bt.total_assets_cur == bt.available_cash + (15.3 * 200) + (151.3 *
                                                                      300)


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
    assert 100 == bt.hold_price_cur_df.loc['000001']['amount']
    assert np.round(6.7, 2) == np.round(
        bt.hold_price_cur_df.loc['000001']['buy_price'], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + 10 * 100, 2)
    assert bt._BackTest__get_buy_avg_price('000001') == (6.7, 100.0)


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
    assert 1200 == bt.hold_price_cur_df.loc['000001']['amount']
    assert np.round(6.7, 2) == np.round(
        bt.hold_price_cur_df.loc['000001']['buy_price'], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + 10 * 1200, 2)
    assert bt._BackTest__get_buy_avg_price('000001') == (6.7, 1200.0)


def test_calc():

    data = pd.DataFrame({
        'code': ['000001' for x in range(7)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1),
            dt(2003, 1, 1),
            dt(2004, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 10, 3.0, 3.5, 5.0],
    })

    class chker(MinAmountChecker):
        def __init__(self,
                     buy_dict,
                     sell_dict,
                     min_price=3000,
                     min_increase=1.15,
                     **kwargs):
            super().__init__(buy_dict, sell_dict, **kwargs)
            self._min_price = min_price
            self._min_increase = min_increase

        def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
                          price: float, cash: float, hold_amount: float,
                          hold_price: float, **kwargs) -> bool:
            if price < hold_price:
                # 当前价格小于持仓价时，不可卖
                return False
            if code in self.sell_dict.keys() and date in self.sell_dict[code]:
                # 其他情况均可卖
                return True
            # if hold_amount > 0 and self._min_increase > 0 and price >= hold_price * self._min_increase:
            #     # 当前价格超过成本价15%时，可卖
            #     return True
            return False

        def on_calc_buy_amount(self, date, code: str, price: float,
                               cash: float, **kwargs) -> float:
            amount = 100
            if self._min_price > 0:
                if cash < self._min_price:
                    return super().on_calc_buy_amount(date, code, price, cash)
                while True:
                    amount = amount + 100
                    if price * amount > self._min_price:
                        break
                amount = amount - 100
            return amount

        def on_calc_sell_amount(self, date: datetime.datetime.timestamp,
                                code: str, price: float, cash: float,
                                hold_amount: float, hold_price: float,
                                **kwargs) -> float:
            """返回所有持仓数量，一次卖出所有"""
            return hold_amount

    bt = BackTest(data,
                  init_cash=50000,
                  callbacks=[
                      chker(
                          buy_dict={
                              '000001': [
                                  dt(1998, 1, 1),
                                  dt(2000, 1, 1),
                                  dt(2002, 1, 1),
                                  dt(2004, 1, 1)
                              ]
                          },
                          sell_dict={
                              '000001':
                              [dt(1999, 1, 1),
                               dt(2001, 1, 1),
                               dt(2003, 1, 1)]
                          })
                  ])
    bt.calc_trade_history()
    print(bt.report())
    assert 600 == bt.hold_price_cur_df.loc['000001']['amount']
    assert np.round(5., 2) == np.round(
        bt.hold_price_cur_df.loc['000001']['buy_price'], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + (5.0) * 600, 2)
    assert bt._BackTest__get_buy_avg_price('000001') == (5.0, 600.0)


def test_init_hold():
    data = pd.DataFrame({
        'code': ['000001' for x in range(4)],
        'date':
        [dt(1998, 1, 1),
         dt(1999, 1, 1),
         dt(2000, 1, 1),
         dt(2001, 1, 1)],
        'close': [4.5, 7.9, 6.7, 10],
    })
    init_hold = pd.DataFrame({
        'code': ['000001'],
        'amount': [400],
        'price': [3],
        'buy_date': [dt(1998, 1, 1)],
        'stoploss_price':[-1],
        'stopprofit_price':[-1],
        'next_price':[-1],
    })
    bt = BackTest(data, init_hold=init_hold)
    assert not bt.available_hold_df.empty
    assert bt.available_hold_df['000001'] == 400
    assert bt.hold_price_cur_df.loc['000001', 'buy_price'] == 3.0
    assert bt.hold_price_cur_df.loc['000001', 'amount'] == 400
    assert bt.hold_price_cur_df.loc['000001', 'price_cur'] == 10.0
    bt.calc_trade_history()
    print(bt.report())

    bt = BackTest(
        data,
        init_hold=init_hold,
        callbacks=[
            MinAmountChecker(
                sell_dict={'000001': [dt(1999, 1, 1),
                                      dt(2000, 1, 1)]})
        ])
    bt.calc_trade_history()
    assert not bt.history_df.empty
    assert bt.available_hold_df['000001'] == 200
    assert bt.available_cash > bt.init_cash
    assert bt.total_assets_cur == bt.available_cash + 200 * 10  #最新价格10元，总共持有200股
    print(bt.report())


def test_calc_Skip():

    data = pd.DataFrame({
        'code': ['000001' for x in range(7)],
        'date': [
            dt(1998, 1, 1),
            dt(1999, 1, 1),
            dt(2000, 1, 1),
            dt(2001, 1, 1),
            dt(2002, 1, 1),
            dt(2003, 1, 1),
            dt(2004, 1, 1)
        ],
        'close': [4.5, 7.9, 6.7, 10, 3.0, 3.5, 5.0],
    })

    class chker(MinAmountChecker):
        def __init__(self,
                     buy_dict,
                     sell_dict,
                     min_price=3000,
                     min_increase=1.15,
                     **kwargs):
            super().__init__(buy_dict, sell_dict, **kwargs)
            self._min_price = min_price
            self._min_increase = min_increase

        def on_check_sell(self, date: datetime.datetime.timestamp, code: str,
                          price: float, cash: float, hold_amount: float,
                          hold_price: float, **kwargs) -> bool:
            if price < hold_price:
                # 当前价格小于持仓价时，不可卖
                return False
            if code in self.sell_dict.keys() and date in self.sell_dict[code]:
                # 其他情况均可卖
                return True
            # if hold_amount > 0 and self._min_increase > 0 and price >= hold_price * self._min_increase:
            #     # 当前价格超过成本价15%时，可卖
            #     return True
            return False

        def on_calc_buy_amount(self, date, code: str, price: float,
                               cash: float, **kwargs) -> float:
            amount = 100
            if self._min_price > 0:
                if cash < self._min_price:
                    return super().on_calc_buy_amount(date, code, price, cash)
                while True:
                    amount = amount + 100
                    if price * amount > self._min_price:
                        break
                amount = amount - 100
            return amount

        def on_calc_sell_amount(self, date: datetime.datetime.timestamp,
                                code: str, price: float, cash: float,
                                hold_amount: float, hold_price: float,
                                **kwargs) -> float:
            """返回所有持仓数量，一次卖出所有"""
            return hold_amount

    bt = BackTest(
        data,
        init_cash=50000,
        live_start_date=dt(2000, 1, 1),
        callbacks=[
            chker(buy_dict={
                '000001': [
                    dt(1998, 1, 1),
                    dt(2000, 1, 1),
                    dt(2002, 1, 1),
                    dt(2004, 1, 1)
                ]
            },
                  sell_dict={'000001': [dt(2001, 1, 1),
                                        dt(2003, 1, 1)]})
        ])
    bt.calc_trade_history()
    print(bt.report())
    assert 600 == bt.hold_price_cur_df.loc['000001']['amount']
    assert np.round(5., 2) == np.round(
        bt.hold_price_cur_df.loc['000001']['buy_price'], 2)
    assert np.round(bt.total_assets_cur,
                    2) == np.round(bt.available_cash + (5.0) * 600, 2)
    assert bt._BackTest__get_buy_avg_price('000001') == (5.0, 600.0)
    assert bt.history_df.sort_values('datetime').iloc[0]['datetime'] == dt(
        2000, 1, 1)


def test_calc_pnl_fifo():
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 10)

    history_df = pd.DataFrame({
        'code': ['000001', '000001', '000001', '000001'],
        'amount': [100, 200, -200, -100],
        'price': [6.3, 5.4, 7.1, 4.3],
        'datetime': ['2020-04-11', '2020-05-12', '2020-05-14', '2020-07-11']
    })
    print(history_df)
    profit_df = BackTest._pnl_fifo(history_df, history_df.code.unique())
    print(profit_df)
    assert not profit_df.empty
    assert len(profit_df) == 3
    assert profit_df.loc['000001'].iloc[0]['buy_price'] == 6.3
    assert profit_df.loc['000001'].iloc[0]['amount'] == 100
    assert profit_df.loc['000001'].iloc[0]['sell_price'] == 7.1
    assert profit_df.loc['000001'].iloc[0]['pnl_ratio'] == 7.1 / 6.3 - 1
    assert profit_df.loc['000001'].iloc[0]['pnl_money'] == (7.1 - 6.3) * 100
    assert profit_df.loc['000001'].iloc[0]['hold_gap'] == profit_df.loc[
        '000001'].iloc[0].sell_date - profit_df.loc['000001'].iloc[0].buy_date

    history_df = pd.DataFrame({
        'code':
        ['000001', '000001', '000002', '000001', '000002', '000003', '000001'],
        'amount': [100, 200, 400, -200, -200, 100, -100],
        'price': [6.3, 5.4, 3.3, 7.1, 3.51, 1.09, 4.3],
        'datetime': [
            '2020-04-11', '2020-05-12', '2020-05-12', '2020-05-14',
            '2020-05-14', '2020-07-11', '2020-07-11'
        ]
    })
    print(history_df)
    profit_df = BackTest._pnl_fifo(history_df, history_df.code.unique())
    print(profit_df)
    assert not profit_df.empty
    assert len(profit_df) == 4
    assert profit_df.loc['000001'].iloc[0]['buy_price'] == 6.3
    assert profit_df.loc['000001'].iloc[0]['amount'] == 100
    assert profit_df.loc['000001'].iloc[0]['sell_price'] == 7.1
    assert profit_df.loc['000001'].iloc[0]['pnl_ratio'] == 7.1 / 6.3 - 1
    assert profit_df.loc['000001'].iloc[0]['pnl_money'] == (7.1 - 6.3) * 100
    assert profit_df.loc['000001'].iloc[0]['hold_gap'] == profit_df.loc[
        '000001'].iloc[0].sell_date - profit_df.loc['000001'].iloc[0].buy_date

    assert profit_df.loc['000002']['buy_price'] == 3.3
    assert profit_df.loc['000002']['amount'] == 200
    assert profit_df.loc['000002']['sell_price'] == 3.51
    assert profit_df.loc['000002']['pnl_ratio'] == 3.51 / 3.3 - 1
    assert profit_df.loc['000002']['pnl_money'] == (3.51 - 3.3) * 200
    assert profit_df.loc['000002']['hold_gap'] == profit_df.loc[
        '000002'].sell_date - profit_df.loc['000002'].buy_date


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_bar_pnl_ratio():
    import matplotlib.pyplot as plt
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 10)
    history_df = pd.DataFrame({
        'code':
        ['000001', '000001', '000002', '000001', '000002', '000003', '000001'],
        'amount': [100, 200, 400, -200, -200, 100, -100],
        'price': [6.3, 5.4, 3.3, 7.1, 3.51, 1.09, 4.3],
        'datetime': [
            '2020-04-11', '2020-05-12', '2020-05-12', '2020-05-14',
            '2020-05-14', '2020-07-11', '2020-07-11'
        ]
    })

    profit_df = BackTest._pnl_fifo(history_df, history_df.code.unique())

    print('>>> profit_df')
    print(profit_df)
    print('>>> Utils.win_rate(profit_df)')
    print(Utils.win_rate(profit_df))

    Utils._bar_pnl_ratio(profit_df)
    # plt.show()
    Utils._bar_pnl_money(profit_df)
    # plt.show()

    fig, axes = plt.subplots(1, 3)
    Utils.plt_pnl_ratio(profit_df, ax=axes[0])
    axes[0].set_title("柱状图")
    Utils.plt_pnl_ratio(profit_df, kind='scatter', ax=axes[1])
    axes[1].set_title("散列图")
    plt.gcf().autofmt_xdate()
    Utils.plt_win_rate(profit_df, ax=axes[2])
    # plt.show()


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_plt_pnl():
    import matplotlib.pyplot as plt
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 10)
    history_df = pd.DataFrame({
        'code': ['000001', '000001', '000001', '000001'],
        'amount': [100, -100, 100, -100],
        'price': [6.3, 6.4, 6.2, 6.1],
        'datetime': ['2020-04-11', '2020-04-13', '2020-04-15', '2020-04-17']
    })

    data = pd.DataFrame({
        'date': [
            datetime.datetime(2020, 4, 10),
            datetime.datetime(2020, 4, 11),
            datetime.datetime(2020, 4, 12),
            datetime.datetime(2020, 4, 13),
            datetime.datetime(2020, 4, 14),
            datetime.datetime(2020, 4, 15),
            datetime.datetime(2020, 4, 16),
            datetime.datetime(2020, 4, 17)
        ],
        'close': [6.25, 6.3, 6.35, 6.4, 6.3, 6.2, 6.15, 6.1]
    })

    profit_df = BackTest._pnl_fifo(history_df, history_df.code.unique())

    print('>>> data')
    print(data)
    print('>>> profit_df')
    print(profit_df)
    print(">>> Utils.plt_pnl(data=data,\
                       v=profit_df,\
                       x='date',\
                       y='close',\
                       subplot_kws={'title': 'test'},\
                       line_kws={'c': 'b'})")
    ax = Utils.plt_pnl(data=data,
                       v=profit_df,
                       x='date',
                       y='close',
                       subplot_kws={'title': 'test'},
                       line_kws={'c': 'b'})
    # plt.show()




@pytest.mark.skip
def test_temp():

    import logging
    logging.debug = print
    logging.info = print

    ret_datas = pd.read_csv(os.path.join(r'C:\Users\GuQiang\Documents\GitHub\StockTest\datas', 'qfq_2005_2_2020_rets.csv'),
                            index_col=None,
                            dtype={'code': str},
                            parse_dates=['date'])
    ret_datas.sort_values('date', inplace=True)
    ret_datas.set_index(['code', 'date'], inplace=True)

    symbol = '600036'

    df_symbol = ret_datas[ret_datas.index.get_level_values(0) == symbol]

    from finance_tools_py.simulation import Simulation
    from finance_tools_py.simulation.callbacks.talib import SMA
    from finance_tools_py.simulation.callbacks import CallBack
    from finance_tools_py.simulation.callbacks.talib import BBANDS
    from finance_tools_py.simulation.callbacks.talib import ATR
    import talib

    class CALC_LINEARREG_SLOPE(CallBack):
        """计算线性角度"""

        def __init__(self, colname, timeperiod, **kwargs):
            super().__init__(**kwargs)
            self.colname = colname
            self.timeperiod = timeperiod

        def on_preparing_data(self, data, **kwargs):
            col_name = '{}_lineSlope_{}'.format(self.colname, self.timeperiod)
            data[col_name] = talib.LINEARREG_SLOPE(data[self.colname], self.timeperiod)

    class CALC_OPT(CallBack):
        def on_preparing_data(self, data, **kwargs):
            data.dropna(inplace=True)
            data['opt'] = np.NaN
            data.loc[data['close'] > data['bbands_20_2_2_up'], 'opt'] = 1
            data.loc[data['close'] < data['bbands_20_2_2_low'], 'opt'] = 0

    #         data['opt'].fillna(method='ffill',inplace=True)
    #         data['opt'].fillna(method='bfill',inplace=True)

    cbs = [
        ATR(20),
        BBANDS(20, 2, 2),
        CALC_LINEARREG_SLOPE('bbands_20_2_2_mean', 20),
        CALC_OPT(),
    ]

    import statistics

    def test_all_years_single_symbol(symbol,
                                     init_cash=10000,
                                     start_year=2005,
                                     end_year=2007,
                                     verbose=2,
                                     show_report=True,
                                     show_plot=True,
                                     cbs=cbs,
                                     show_history=False,
                                     min_amount=100,
                                     single_max=400,
                                     **kwargs):
        """

        Args:
            init_cash:
            start_year (int): 开始计算年份。
            end_year (int): 结束计算年份。


        Returns:
            report (dict): BackTest字典。key值为年份。
            datas (dict): 回测用的数据源字典。key值为年份。
            buys (dict): 买点字典。key值为年份。
            sells (dict): 卖点字典。key值为年份。
        """
        hold = pd.DataFrame()
        report = {}
        datas = {}
        buys = {}
        sells = {}
        h = {}

        from tqdm import tqdm

        for year in tqdm(range(start_year, end_year)):
            df_symbol_year = ret_datas[
                (ret_datas.index.get_level_values(0) == symbol)
                & (ret_datas.index.get_level_values(1) <= '{}-12-31'.format(year))]
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

            ts = TurtleStrategy(
                colname='atr_20',
                buy_dict=buy_dict,
                sell_dict=sell_dict,
                holds=h,
                max_amount=single_max,
                min_amount=min_amount,
            )
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
                        hs.append(pd.DataFrame({
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
        return report, datas, buys, sells

    init_cash = 10000
    report, datas, buys, sells = test_all_years_single_symbol('600036',
                                                              init_cash=init_cash,
                                                              start_year=2005,
                                                              end_year=2020,
                                                              verbose=0,
                                                              show_report=False,
                                                              show_history=False,
                                                              show_plot=False)
    # clear_output(True)
    print('计算起止日期:{:%Y-%m-%d}~{:%Y-%m-%d}'.format(
        list(datas.values())[0].sort_values('date').iloc[0]['date'],
        list(datas.values())[-1].sort_values('date').iloc[0]['date']))
    print('测试年份:{}-{}'.format(len(list(datas.keys())), list(datas.keys())))
    print('总体期初资产:{:.2f},总体期末资产:{:.2f};变化率:{:.2%}'.format(
        init_cash,
        list(report.values())[-1].total_assets_cur,
        list(report.values())[-1].total_assets_cur / init_cash))
    pds = pd.DataFrame({
        'assert': [x.total_assets_cur for x in list(report.values())],
        'year':
            list(report.keys())
    })
    pds = pds.append(
        pd.DataFrame({
            'assert': [init_cash],
            'year': [list(report.keys())[0] - 1]
        })).sort_values('year')
    pds['rets'] = pds['assert'].pct_change()
    pds['rets1'] = pds['assert'] / pds['assert'].iloc[0] - 1
    pds.fillna(0, inplace=True)
    print(pd.concat([v.profit_loss_df() for v in report.values()]))