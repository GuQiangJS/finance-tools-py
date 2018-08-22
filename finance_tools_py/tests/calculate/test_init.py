# Copyright (C) 2018 GuQiangJs.
# Licensed under Apache License 2.0 <see LICENSE file>

import unittest

from finance_datareader_py.sohu.daily import SohuDailyReader

from finance_tools_py.calculate import *


class calculate_TestCase(unittest.TestCase):
    def test_daily_return(self):
        df = SohuDailyReader('000300', prefix='zs_').read()['Close']
        self.assertFalse(df.empty)
        df1 = daily_returns(df)
        self.assertFalse(df1.empty)
        print(df.sort_index().tail())
        print(df1.tail())

    def test_cum_returns(self):
        data = [1, 2, 3, 4, 5]
        corr = (5 / 1) - 1
        df = pd.DataFrame(data)
        cum = cum_returns(df)
        self.assertEqual(cum, corr)
        column_name = 'A'
        df = pd.DataFrame({column_name: data})
        cum1 = cum_returns(df, column_name)
        cum2 = cum_returns(df)
        self.assertEqual(cum1, cum2)
        self.assertEqual(cum1, corr)

    def test_daily_returns_avg(self):
        data = [1, 2, 3, 4, 5]
        df = pd.DataFrame(data)
        self.assertEqual(daily_returns_avg(df)[0], daily_returns(df).mean()[0])

    def test_daily_returns_std(self):
        data = [1, 2, 3, 4, 5]
        df = pd.DataFrame(data)
        self.assertEqual(daily_returns_std(df)[0], daily_returns(df).std()[0])

    def test_risk_free_interest_rate(self):
        # 年化收益 5%，持有 30 天，本金 10000。月均收益应该为 41.1
        risk = risk_free_interest_rate(0.05, 365)
        # print(risk)
        # print(risk * 30 * 10000)
        # print(np.around((risk * 30 * 10000), decimals=2))
        # print(np.around(41.1, decimals=2))
        self.assertEqual(np.around((risk * 30 * 10000), decimals=2),
                         np.around(41.1, decimals=2))

    def test_sharpe_ratio(self):
        """测试夏普比率计算"""
        # 假设你希望你的股票投资组合，返回12％，明年全年。
        # 如果无风险国债收益票据的，比如说5％，你的投资组合带有0.06标准偏差，
        # 然后从上面的公式，我们可以计算出的夏普比率为你的投资组合是：
        # （0.12 - 0.05） / 0.06 = 1.17
        # 这意味着对于每个回报点，您承担1.17“单位”的风险。
        sr = sharpe_ratio(0.12, 0.05, 0.06)
        self.assertIsInstance(sr, float)
        self.assertEqual(np.around(sr, decimals=2), 1.17)

        lst = []
        for i in range(100):
            lst.append(sharpe_ratio(pd.DataFrame(np.random.normal(0.12, 0.06,
                                                                  10)), 0.05))

        sr = sharpe_ratio(pd.DataFrame([0.0100, -0.0100, 0.0300, 0.0400,
                                        -0.0200, -0.0100]), 0)
        self.assertIsInstance(sr, float)
        self.assertEqual(np.around(sr, decimals=6), 0.275241)


if __name__ == '__main__':
    unittest.main()
