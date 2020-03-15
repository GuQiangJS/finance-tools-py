from datetime import date as dt

import numpy as np
import pandas as pd
import pytest
import talib
import os
from finance_tools_py.simulation import Simulation
from finance_tools_py.simulation.callbacks import talib as cb_talib


@pytest.fixture
def init_global_data():
    pytest.global_code = '000001'
    pytest.global_data = pd.DataFrame({
        'code': [pytest.global_code for x in range(1998, 2020)],
        'date': [dt(y, 1, 1) for y in range(1998, 2020)],
        'close':
        np.random.random((len(list(range(1998, 2020))), )),
        'high':
        np.random.random((len(list(range(1998, 2020))), )),
        'low':
        np.random.random((len(list(range(1998, 2020))), )),
    })


def _mock_data(size):
    return pd.DataFrame({
        'close': np.random.random((len(list(range(size))), )),
        'high': np.random.random((len(list(range(size))), )),
        'low': np.random.random((len(list(range(size))), )),
    })


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_BBANDS(init_global_data):
    print('>>> print(data)')
    data = _mock_data(5)
    print(data)
    t = 3
    u = 2.4
    d = 2.7
    print('>>> t={}'.format(t))
    print('>>> u={}'.format(u))
    print('>>> d={}'.format(d))
    print('>>> print(BBANDS(t, u, d).on_preparing_data(data))')
    cb_talib.BBANDS(t, u, d).on_preparing_data(data)
    print(">>> cols=[col for col in data.columns if 'bbands' in col]")
    cols = [col for col in data.columns if 'bbands' in col]
    print('>>> print(data[cols].info())')
    print(data[cols].info())
    print('>>> print(data[cols])')
    print(data[cols])


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_WILLR(init_global_data):
    print('>>> print(data)')
    data = _mock_data(5)
    print(data)
    t = 3
    print('>>> t={}'.format(t))
    print('>>> print(WILLR(t).on_preparing_data(data))')
    cb_talib.WILLR(t).on_preparing_data(data)
    print(">>> cols=[col for col in data.columns if 'willr' in col]")
    cols = [col for col in data.columns if 'willr' in col]
    print('>>> print(data[cols].info())')
    print(data[cols].info())
    print('>>> print(data[cols])')
    print(data[cols])


def test_BBANDS(init_global_data):
    t = 5
    u = 2
    d = 2
    b = cb_talib.BBANDS(t, u, d)
    b.on_preparing_data(pytest.global_data)
    print(pytest.global_data.info())
    col_up = 'bbands_{}_{}_{}_up'.format(t, u, d)  # 布林带上线
    col_mean = 'bbands_{}_{}_{}_mean'.format(t, u, d)  # 布林带中线
    col_low = 'bbands_{}_{}_{}_low'.format(t, u, d)  # 布林带下线
    assert col_up in pytest.global_data.columns
    assert col_mean in pytest.global_data.columns
    assert col_low in pytest.global_data.columns
    up, mean, low = talib.BBANDS(pytest.global_data['close'], t, u, d)
    assert pd.Series.equals(up, pytest.global_data[col_up])
    assert pd.Series.equals(mean, pytest.global_data[col_mean])
    assert pd.Series.equals(low, pytest.global_data[col_low])


def test_Sim_BBANDS(init_global_data):
    """测试通过回测调用BBANDS，逻辑与`test_BBANDS`一致"""
    t = 5
    u = 2
    d = 2
    b = cb_talib.BBANDS(t, u, d)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    col_up = 'bbands_{}_{}_{}_up'.format(t, u, d)  # 布林带上线
    col_mean = 'bbands_{}_{}_{}_mean'.format(t, u, d)  # 布林带中线
    col_low = 'bbands_{}_{}_{}_low'.format(t, u, d)  # 布林带下线
    assert col_up in s.data.columns
    assert col_mean in s.data.columns
    assert col_low in s.data.columns
    up, mean, low = talib.BBANDS(s.data['close'], t, u, d)
    assert pd.Series.equals(up, s.data[col_up])
    assert pd.Series.equals(mean, s.data[col_mean])
    assert pd.Series.equals(low, s.data[col_low])


def test_WILLR(init_global_data):
    t = 5
    b = cb_talib.WILLR(t)
    b.on_preparing_data(pytest.global_data)
    print(pytest.global_data.info())
    w = 'willr_{}'.format(t)  # 威廉指标
    assert w in pytest.global_data.columns
    real = talib.WILLR(pytest.global_data['high'], pytest.global_data['low'],
                       pytest.global_data['close'], t)
    assert pd.Series.equals(real, pytest.global_data[w])


def test_Sim_BBANDS(init_global_data):
    """测试通过回测调用WILLR，逻辑与`test_WILLR`一致"""
    t = 5
    b = cb_talib.WILLR(t)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'willr_{}'.format(t)  # 威廉指标
    assert w in s.data.columns
    real = talib.WILLR(s.data['high'], s.data['low'],
                       s.data['close'], t)
    assert pd.Series.equals(real, s.data[w])
