import os
if "TRAVIS" not in os.environ or os.environ["TRAVIS"] != "true":
    from finance_tools_py.simulation import Simulation
    from finance_tools_py import simulation
    import matplotlib.pyplot as plt
    import datetime
    import QUANTAXIS as QA


    def test_simulate():
        symbol = '600422'
        start = '1990-01-01'
        end = datetime.date(2020, 3, 10)
        data = QA.QA_fetch_stock_day_adv(symbol, start=start, end=end).to_qfq().data
        sim = Simulation(data, symbol)
        sim.simulate(callbacks=[simulation.Bolling(60, 2.8, 2.8, 0.5, 0.5),
                                simulation.Pandas_Rolling(60, 120),
                                simulation.Linear_Angle(),
                                simulation.CalcTradePoint()])
        print(sim.lastest_signal)
        print(sim.signaldata)
        print(sim.data[['close', 'diff_low', 'diff_up', 'rolling_mean']])
        print(sim.buy_query)
        print(sim.sell_query)
        # sim.plot_sns(y=['close','boll_60_up','boll_60_low'])
        # plt.show()
        # sim.plot_sns(data=sim.data[-300:],y=['close','boll_60_up','boll_60_low'])
        # plt.show()


    def test_simulate2():
        """不同时间区间计算结果不一致。尤其是买入点的数据判断有问题。可以参考绘图结果。
        Todo: 重大问题
        """

        symbol = '600422'
        for year in range(2006, 2020):
            start = datetime.date(year, 1, 1).strftime('%Y-%m-%d')
            end = datetime.date(2020, 3, 10)
            data = QA.QA_fetch_stock_day_adv(symbol, start=start, end=end).to_qfq().data
            sim = Simulation(data, symbol)
            sim.simulate(callbacks=[simulation.Bolling(60, 2.8, 2.8, 0.5, 0.5),
                                    simulation.Pandas_Rolling(60, 120),
                                    simulation.Linear_Angle(),
                                    simulation.CalcTradePoint()])
            print('{}:{}'.format(start, sim.buy_query))
            # sim.plot_sns(y=['close', 'boll_60_up', 'boll_60_low'])
            # plt.show()
