from finance_tools_py.backtest import TurtleStrategy
import pandas as pd
import datetime


def test_TurtleStrategy():
    ts = TurtleStrategy(colname='atr5')
    assert ts.stoploss_point == 2
    assert ts.stopprofit_point == 10
    assert ts.next_point == 1
    row = pd.Series({'atr5': 0.05})
    ls, lf, n = ts.calc_price(1, row=row)
    assert ls == (1 - ts.stoploss_point * 0.05)
    assert lf == (1 + ts.stopprofit_point * 0.05)
    assert n == (1 + ts.next_point * 0.05)

    print(">>> from finance_tools_py.backtest import TurtleStrategy")
    print(">>> ts = TurtleStrategy(colname='atr5')")
    print(">>> row = pd.Series({'atr5': 0.05})")
    print(">>> ts.calc_price(1, row=row")
    print("(0.9, 1.5, 1.05)")

    ts = TurtleStrategy(colname='',
                        stoploss_point=0.5,
                        stopprofit_point=20,
                        next_point=2)
    assert ts.stoploss_point == 0.5
    assert ts.stopprofit_point == 20
    assert ts.next_point == 2

    ls, lf, n = ts.calc_price(1, row=row)
    assert ls == -1
    assert lf == -1
    assert n == -1

    # 只有一笔持仓时的判断-开始
    ts = TurtleStrategy(
        colname='atr5',
        single_max=100,
        verbose=2,
        buy_dict={'0': [datetime.date(2000, 1, 1),
                        datetime.date(2000, 1, 2)]})
    ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                          '0',
                          1,
                          1000,
                          row=row,
                          verbose=2)
    print(ts.holds['0'][0])
    # 超过最大持仓线时不再购买
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 2), '0', 1.01, 500, row=row, verbose=2)
    print(ts.holds['0'][0])
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 2), '0', 1.1, 500, row=row, verbose=2)

    # 没有达到止损线，不卖
    assert not ts.on_check_sell(
        datetime.date(2000, 1, 3), '0', 0.95, 0, 0, 0, row=row, verbose=2)
    # 低于止损线，卖出
    assert ts.on_check_sell(datetime.date(2000, 1, 3),
                            '0',
                            0.89,
                            0,
                            0,
                            0,
                            row=row,
                            verbose=2)
    # 低于止盈，不卖
    assert not ts.on_check_sell(
        datetime.date(2000, 1, 3), '0', 1.49, 0, 0, 0, row=row, verbose=2)
    # 超过止盈，卖出
    assert ts.on_check_sell(datetime.date(2000, 1, 3),
                            '0',
                            1.51,
                            0,
                            0,
                            0,
                            row=row,
                            verbose=2)

    # 止损数量
    assert 100 == ts.on_calc_sell_amount(datetime.date(2000, 1, 3),
                                         '0',
                                         0,
                                         0,
                                         0,
                                         0,
                                         row=row,
                                         verbose=2)
    # 只有一笔持仓时的判断-结束

    # 多笔持仓时的判断-开始
    ts = TurtleStrategy(colname='atr5',
                        single_max=100,
                        verbose=2,
                        buy_dict={
                            '0': [
                                datetime.date(2000, 1, 1),
                                datetime.date(2000, 1, 2),
                                datetime.date(2000, 1, 3)
                            ]
                        })

    ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                          '0',
                          1,
                          1000,
                          row=row,
                          verbose=2)
    ts.on_calc_buy_amount(datetime.date(2000, 1, 2),
                          '0',
                          2,
                          1000,
                          row=row,
                          verbose=2)
    print(ts.holds['0'][0])
    print(ts.holds['0'][1])
    # 超过最大持仓线时不再购买
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 2), '0', 1.01, 500, row=row, verbose=2)
    print(ts.holds['0'][0])
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 2), '0', 1.1, 500, row=row, verbose=2)

    # 止损数量
    assert 100 == ts.on_calc_sell_amount(datetime.date(2000, 1, 3),
                                         '0',
                                         1.8,
                                         0,
                                         0,
                                         0,
                                         row=row,
                                         verbose=2)
    print(ts.holds['0'][0])
    assert 100 == ts.holds['0'][0].amount
    # 多笔持仓时的判断-结束


"""
持仓 - 有 - 
    - 无


"""


def test_TurtleStrategy_1():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  #买入价
                100,  #持仓数量
                9,  #止损价
                11,  #止盈价
                10.5  #下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy('', holds=holds)
    # 当前时间不包含在卖出点字典中-开始
    assert 1 == len(ts.holds[symbol])
    assert 0 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol, 10.2,
                                       1000, 0, 10)
    assert not ts.on_check_sell(datetime.date(2000, 1, 1), symbol, 10.2, 1000,
                                0, 10)
    assert 1 == len(ts.holds[symbol])
    # 当前时间不包含在卖出点字典中-开始


def test_TurtleStrategy_2():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  #买入价
                100,  #持仓数量
                9,  #止损价
                11,  #止盈价
                10.5  #下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy('', holds=holds)

    assert 1 == len(ts.holds[symbol])
    # 虽然有持仓，但是没有任何的卖出点标记，也没有到止盈/止损/加仓点位
    assert not ts.on_check_sell(datetime.date(2000, 1, 1), symbol, 10.2, 1000,
                                100, 10)
    assert 100 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol,
                                         10.2, 1000, 100, 10)
    assert 0 == len(ts.holds[symbol])


def test_TurtleStrategy_3():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  #买入价
                100,  #持仓数量
                9,  #止损价
                11,  #止盈价
                10.5  #下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy('', holds=holds)

    assert 1 == len(ts.holds[symbol])
    # 虽然有持仓，但是没有任何的卖出点标记，也没有到止盈/止损/加仓点位
    assert not ts.on_check_sell(datetime.date(2000, 1, 1), symbol, 10.2, 1000,
                                0, 10)
    # 没有到达止损点位
    assert 0 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol, 9.01,
                                       1000, 0, 10)
    # 到达止损点位
    assert 100 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol, 9,
                                         1000, 0, 10)
    assert 0 == len(ts.holds[symbol])


def test_TurtleStrategy_4():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  # 买入价
                100,  # 持仓数量
                9,  # 止损价
                11,  # 止盈价
                10.5  # 下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy('', holds=holds)

    assert 1 == len(ts.holds[symbol])
    # 虽然有持仓，但是没有任何的卖出点标记，也没有到止盈/止损/加仓点位
    assert not ts.on_check_sell(datetime.date(2000, 1, 1), symbol, 10.2, 1000,
                                0, 10)
    # 没有到达止盈点位
    assert 0 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol,
                                       10.99, 1000, 0, 10)
    # 到达止盈点位
    assert 100 == ts.on_calc_sell_amount(datetime.date(2000, 1, 1), symbol, 11,
                                         1000, 0, 10)
    assert 0 == len(ts.holds[symbol])


def test_TurtleStrategy_4():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  # 买入价
                100,  # 持仓数量
                9,  # 止损价
                11,  # 止盈价
                10.5  # 下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy('',
                        holds=holds,
                        buy_dict={symbol: [datetime.date(2000, 1, 1)]})

    assert 1 == len(ts.holds[symbol])
    # 没有到达加仓点位
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 1), symbol, 10.49, 1000, verbose=2)
    # 到达加仓点位
    assert ts.on_check_buy(datetime.date(2000, 1, 1),
                           symbol,
                           10.50,
                           1000,
                           verbose=2)
    # 没有加仓点位
    assert 0 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                                      symbol,
                                      10.49,
                                      1000,
                                      verbose=2)
    # 到达购买点，但是资金不足
    assert 0 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                                      symbol,
                                      10.50,
                                      1000,
                                      verbose=2)
    # 到达购买点，资金充足
    assert 100 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                                        symbol,
                                        10.50,
                                        1200,
                                        verbose=2)
    assert 2 == len(ts.holds[symbol])
    assert ts.holds[symbol][-1].amount == 100
    assert ts.holds[symbol][-1].stoploss_price == -1
    assert ts.holds[symbol][-1].stopprofit_price == -1
    assert ts.holds[symbol][-1].next_price == -1
    # 到达加仓点位
    assert ts.on_check_buy(datetime.date(2000, 1, 1), symbol, 10.50, 1000)
    assert 100 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                                        symbol,
                                        10.50,
                                        1200,
                                        verbose=2)
    # 到达加仓点位
    assert ts.on_check_buy(datetime.date(2000, 1, 1), symbol, 10.50, 1000)
    assert 100 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1),
                                        symbol,
                                        10.50,
                                        1200,
                                        verbose=2)
    # 到达加仓点位。但是到达持仓限制
    assert not ts.on_check_buy(
        datetime.date(2000, 1, 1), symbol, 10.50, 1000, verbose=2)


def test_TurtleStrategy_5():
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  # 买入价
                100,  # 持仓数量
                9,  # 止损价
                11,  # 止盈价
                10.5  # 下一个仓位价格
            )
        ]
    }

    ts = TurtleStrategy('',
                        holds=holds,
                        buy_dict={symbol: [datetime.date(2000, 1, 1)]},
                        sell_dict={symbol: [datetime.date(2000, 1, 2)]})

    assert 100 == ts.on_calc_buy_amount(datetime.date(2000, 1, 1), symbol, 20,
                                        10000)
    assert 2 == len(ts.holds[symbol])
    assert 100 == ts.holds[symbol][0].amount
    assert 10 == ts.holds[symbol][0].price
    assert 100 == ts.holds[symbol][-1].amount
    assert 20 == ts.holds[symbol][-1].price

    assert ts.on_check_sell(datetime.date(2000, 1, 2), symbol, 15, 9999, 300,
                            -1)
    assert ts.on_check_sell(datetime.date(2000, 1, 2), symbol, 15, 9999, -1,
                            -1)

    assert 200 == ts.on_calc_sell_amount(datetime.date(2000, 1, 2), symbol, 15,
                                         9999, -1, -1)
    assert 0 == len(ts.holds[symbol])


def test_TurtleStrategy_6():
    """买卖在同一天时，更新止盈/下一个买点价格"""
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  # 买入价
                100,  # 持仓数量
                9,  # 止损价
                11,  # 止盈价
                10.5  # 下一个仓位价格
            ),
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 2, 1),
                20,  # 买入价
                200,  # 持仓数量
                18,  # 止损价
                25,  # 止盈价
                30  # 下一个仓位价格
            )
        ]
    }

    ts = TurtleStrategy(colname='atr5',
                        holds=holds,
                        buy_dict={symbol: [datetime.date(2000, 1, 1)]})

    assert ts.holds[symbol][-1].stopprofit_price == 25
    assert ts.holds[symbol][-1].next_price == 30

    row = pd.Series({'atr5': 0.05})
    ts.on_buy_sell_on_same_day(datetime.date(2000, 1, 1), symbol, 50, row=row)

    new_stoploss, new_stopprofit, new_next = ts.calc_price(50, row=row)

    assert not ts.holds[symbol][-1].stopprofit_price == 25
    assert not ts.holds[symbol][-1].next_price == 30

    assert ts.holds[symbol][-1].stopprofit_price == new_stopprofit
    assert ts.holds[symbol][-1].next_price == new_next

def test_TurtleStrategy_7():
    """买卖在同一天时，不更新止盈/下一个买点价格"""
    symbol = '123456'
    holds = {
        symbol: [
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 1, 1),
                10,  # 买入价
                100,  # 持仓数量
                9,  # 止损价
                11,  # 止盈价
                10.5  # 下一个仓位价格
            ),
            TurtleStrategy.Hold(
                symbol,
                datetime.date(1999, 2, 1),
                20,  # 买入价
                200,  # 持仓数量
                18,  # 止损价
                25,  # 止盈价
                30  # 下一个仓位价格
            )
        ]
    }
    ts = TurtleStrategy(colname='atr5',
                        update_price_onsameday=False,
                        holds=holds,
                        buy_dict={symbol: [datetime.date(2000, 1, 1)]})

    assert ts.holds[symbol][-1].stopprofit_price == 25
    assert ts.holds[symbol][-1].next_price == 30

    row = pd.Series({'atr5': 0.05})
    ts.on_buy_sell_on_same_day(datetime.date(2000, 1, 1), symbol, 50, row=row)

    new_stoploss, new_stopprofit, new_next = ts.calc_price(50, row=row)

    assert ts.holds[symbol][-1].stopprofit_price == 25
    assert ts.holds[symbol][-1].next_price == 30

    assert not ts.holds[symbol][-1].stopprofit_price == new_stopprofit
    assert not ts.holds[symbol][-1].next_price == new_next
