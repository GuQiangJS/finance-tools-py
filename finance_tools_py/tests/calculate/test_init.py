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


if __name__ == '__main__':
    unittest.main()
