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
    assert bt.total_assets_cur == bt.available_cash + (15.3*200)+(151.3*300)


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
                          hold_price: float,**kwargs) -> bool:
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
                               cash: float,**kwargs) -> float:
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
                                hold_amount: float,
                                hold_price: float,**kwargs) -> float:
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
