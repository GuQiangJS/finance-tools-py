from finance_tools_py.simulation import Simulation
import matplotlib.pyplot as plt
import datetime


def test_simulate():
    sim = Simulation()
    sim.simulate('300378', start='2016-01-01', end=datetime.date(2020, 3, 9))
    print(sim.lastest_signal)
    print(sim.signaldf)
    sim.plot_sns()
    plt.show()
