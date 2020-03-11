import os
if "TRAVIS" not in os.environ and os.environ["TRAVIS"] != "true":
    from finance_tools_py.simulation import Simulation
    import matplotlib.pyplot as plt
    import datetime
    import QUANTAXIS as QA

    def test_simulate():
        symbol='300378'
        start = '2016-01-01'
        end = datetime.date(2020, 3, 9)
        data = QA.QA_fetch_stock_day_adv(symbol, start=start, end=end).to_qfq().data
        sim = Simulation(data,symbol)
        sim.simulate()
        print(sim.lastest_signal)
        print(sim.signaldf)
        sim.plot_sns()
        plt.show()
