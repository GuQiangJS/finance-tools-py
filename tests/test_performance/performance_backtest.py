from finance_tools_py.backtest import BackTest
from finance_tools_py.backtest import MinAmountChecker
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta


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
                      hold_price: float) -> bool:
        if price < hold_price:
            # 当前价格小于持仓价时，不可卖
            return False
        if code in self.sell_dict.keys() and date in self.sell_dict[code]:
            # 其他情况均可卖
            return True
        if hold_amount > 0 and self._min_increase > 0 and price >= hold_price * self._min_increase:
            # 当前价格超过成本价15%时，可卖
            return True
        return False

    def on_calc_buy_amount(self, date, code: str, price: float,
                           cash: float) -> float:
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

    def on_calc_sell_amount(self, date: datetime.datetime.timestamp, code: str,
                            price: float, cash: float, hold_amount: float,
                            hold_price: float) -> float:
        """返回所有持仓数量，一次卖出所有"""
        return hold_amount


def do_profile(max=1, verbose=0):
    """模拟 max 只股票的交易过程"""
    def mock_data(code,
                  buy_count=10,
                  sell_count=10,
                  start=datetime.date(2000, 1, 1),
                  end=datetime.date(2020, 1, 1)):
        """从2000-01-01~2020-01-01创建随机数据。并随机选择buy_count天数作为购买日期。
        sell_count天数作为卖出日期。返回随机模拟数据，购买日期集合，卖出日期集合"""
        days = (end - start).days

        df = pd.DataFrame({
            'close':
            np.abs(np.random.normal(0, 1, days)),
            'date': [start + datetime.timedelta(days=x) for x in range(days)]
        })
        df['code'] = code
        df['date'] = pd.to_datetime(df['date'])
        buy = sorted(np.random.choice(df['date'].dt.to_pydatetime(),
                                      buy_count))
        sell = sorted(
            np.random.choice(df['date'].dt.to_pydatetime(), sell_count))

        return df, buy, sell

    code_lst = ['{:06d}'.format(i) for i in range(1, max + 1)]
    dfs = []
    buys = {}
    sells = {}
    for code in code_lst:
        df, b, s = mock_data(code)
        dfs.append(df)
        buys[code] = b
        sells[code] = s

    df = pd.concat(dfs).sort_values('date')
    bt = BackTest(df,
                  init_cash=50000,
                  callbacks=[chker(buy_dict=buys, sell_dict=sells)])
    bt.calc_trade_history(verbose=verbose)


import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()
do_profile(200)  # 模拟200支股票的交易过程
pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
