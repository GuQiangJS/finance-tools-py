from datetime import date as dt

import numpy as np
import pandas as pd
import pytest
import talib
import os
from finance_tools_py.simulation import Simulation
from finance_tools_py.simulation.callbacks import talib as cb_talib
from finance_tools_py.simulation import callbacks


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


@pytest.fixture
def mock_data():
    pytest.mock_code = '600036'
    if "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true":
        pytest.mock_data = pd.read_csv('tests/data/600036.csv', index_col=None)
    else:
        pytest.mock_data = pd.read_csv('data/600036.csv', index_col=None)

    pytest.mock_data['date'] = pd.to_datetime(pytest.mock_data['date'])


def _mock_data(size):
    return pd.DataFrame({
        'close': np.random.random((len(list(range(size))), )),
        'high': np.random.random((len(list(range(size))), )),
        'low': np.random.random((len(list(range(size))), )),
    })


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_BBANDS():
    print('>>> from finance_tools_py.simulation.callbacks.talib import BBANDS')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import BBANDS
    print(">>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})")
    data = pd.DataFrame({'close': [y for y in np.arange(0.0, 8.0)]})
    print(">>> print(data['close'].values)")
    print(data['close'].values)
    t = 3
    u = 2.4
    d = 2.7
    print('>>> t = {}'.format(t))
    print('>>> u = {}'.format(u))
    print('>>> d = {}'.format(d))
    print(">>> s = Simulation(data,'',callbacks=[BBANDS(t, u, d)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[BBANDS(t, u, d)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'bbands' in col]")
    cols = [col for col in s.data.columns if 'bbands' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_WILLR(init_global_data):
    print('>>> from finance_tools_py.simulation.callbacks.talib import WILLR')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import WILLR
    print(">>> data = pd.DataFrame({'close': [y for y in range(0, 8)],\n\
                        'high': [y for y in range(0.1, 8.2)],\n\
                        'low': [y for y in range(0.2, 8.2)]})")
    data = pd.DataFrame({
        'close': [y for y in np.arange(0.0, 8.0)],
        'high': [y for y in np.arange(0.1, 8.1)],
        'low': [y for y in np.arange(0.2, 8.2)]
    })
    print(">>> print(data)")
    print(data)
    t = 3
    print('>>> t={}'.format(t))
    print(">>> s = Simulation(data,'',callbacks=[WILLR(t)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[WILLR(t)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'willr' in col]")
    cols = [col for col in s.data.columns if 'willr' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_CCI(init_global_data):
    print('>>> from finance_tools_py.simulation.callbacks.talib import CCI')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import CCI
    print(">>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],\n\
                        'high': [y for y in range(10.1,15.0)],\n\
                        'low': [y for y in range(0.0, 4.9)]})")
    data = pd.DataFrame({
        'close': [y for y in np.arange(5.0, 10.0)],
        'high': [y for y in np.arange(10.1, 15.0)],
        'low': [y for y in np.arange(0.0, 4.9)]
    })
    print(">>> print(data)")
    print(data)
    t = 3
    print('>>> t = {}'.format(t))
    print(">>> s = Simulation(data,'',callbacks=[CCI(t)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[CCI(t)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'cci' in col]")
    cols = [col for col in s.data.columns if 'cci' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_MFI(init_global_data):
    print('>>> from finance_tools_py.simulation.callbacks.talib import MFI')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import MFI
    print(">>> data = pd.DataFrame({'close': [y for y in range(5.0, 10.0)],\n\
                        'high': [y for y in range(10.1, 15.0)],\n\
                        'low': [y for y in range(0.0, 4.9)],\n\
                        'volume': [y for y in range(50.0, 100.0, 10.0)]})")
    data = pd.DataFrame({
        'close': [y for y in np.arange(5.0, 10.0)],
        'high': [y for y in np.arange(10.1, 15.0)],
        'low': [y for y in np.arange(0.0, 4.9)],
        'volume': [y for y in np.arange(50.0, 100.0, 10.0)]
    })
    print(">>> print(data)")
    print(data)
    t = 3
    print('>>> t = {}'.format(t))
    print(">>> s = Simulation(data,'',callbacks=[MFI(t)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[MFI(t)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'mfi' in col]")
    cols = [col for col in s.data.columns if 'mfi' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_DEMA(init_global_data):
    print('>>> from finance_tools_py.simulation.callbacks.talib import DEMA')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import DEMA
    print(">>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})")
    data = pd.DataFrame({'close': [y for y in np.arange(0.0, 8.0)]})
    print(">>> print(data['close'].values)")
    print(data['close'].values)
    t = 3
    print('>>> t={}'.format(t))
    print(">>> s = Simulation(data,'',callbacks=[DEMA(t)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[DEMA(t)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'dema' in col]")
    cols = [col for col in s.data.columns if 'dema' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_RSI(init_global_data):
    print('>>> from finance_tools_py.simulation.callbacks.talib import RSI')
    print('>>> from finance_tools_py.simulation import Simulation')
    from finance_tools_py.simulation.callbacks.talib import RSI
    print(">>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})")
    data = pd.DataFrame({'close': [y for y in np.arange(0.0, 8.0)]})
    print(">>> print(data['close'].values)")
    print(data['close'].values)
    t = 3
    print('>>> t={}'.format(t))
    print(">>> s = Simulation(data,'',callbacks=[RSI(t)])")
    print('>>> s.simulate()')
    s = Simulation(data, '', callbacks=[RSI(t)])
    s.simulate()
    print(">>> cols = [col for col in data.columns if 'rsi' in col]")
    cols = [col for col in s.data.columns if 'rsi' in col]
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(s.data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(s.data[col].values, 2)))

@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping this test on Travis CI. This is an example.")
def test_example_Rolling_Future(init_global_data):
    print(">>> data = pd.DataFrame({'close': [y for y in range(0, 8)]})")
    print(">>> print(data['close'].values)")
    data = pd.DataFrame({'close': [y for y in range(0, 8)]})
    print(data['close'].values)
    t = 3
    print('>>> t={}'.format(t))
    print('>>> print(Rolling_Future(t).on_preparing_data(data))')
    callbacks.Rolling_Future(t).on_preparing_data(data)
    print(">>> cols=[col for col in data.columns if col!='close']")
    cols = [col for col in data.columns if col != 'close']
    print(">>> for col in cols:")
    print(">>>     print('{}:{}'.format(col,np.round(data[col].values,2)))")
    for col in cols:
        print('{}:{}'.format(col, np.round(data[col].values, 2)))


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


def test_Sim_WILLR(init_global_data):
    """测试通过回测调用WILLR，逻辑与`test_WILLR`一致"""
    t = 5
    b = cb_talib.WILLR(t)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'willr_{}'.format(t)  # 威廉指标
    assert w in s.data.columns
    real = talib.WILLR(s.data['high'], s.data['low'], s.data['close'], t)
    assert pd.Series.equals(real, s.data[w])


def test_Sim_CCI(init_global_data):
    """测试通过回测调用CCI，逻辑与`test_CCI`一致"""
    t = 5
    b = cb_talib.CCI(t)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'cci_high_low_close_5'  # 顺势指标
    assert w in s.data.columns
    real = talib.CCI(s.data['high'], s.data['low'], s.data['close'], t)
    assert pd.Series.equals(real, s.data[w])


def test_Sim_MFI(mock_data):
    """测试通过回测调用MFI，逻辑与`test_MFI`一致"""
    t = 5
    b = cb_talib.MFI(t)
    s = Simulation(pytest.mock_data, pytest.mock_data, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'mfi_{}'.format(t)  # 顺势指标
    assert w in s.data.columns
    real = talib.MFI(s.data['high'], s.data['low'], s.data['close'],
                     s.data['volume'], t)
    assert pd.Series.equals(real, s.data[w])


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


def test_Sim_DEMA(init_global_data):
    """测试通过回测调用DEMA，逻辑与`test_DEMA`一致"""
    t = 5
    b = cb_talib.DEMA(t)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'dema_{}_{}'.format('close', t)
    assert w in s.data.columns
    real = talib.DEMA(s.data['close'], t)
    assert pd.Series.equals(real, s.data[w])


def test_Sim_RSI(init_global_data):
    """测试通过回测调用RSI，逻辑与`test_RSI`一致"""
    t = 5
    b = cb_talib.RSI(t)
    s = Simulation(pytest.global_data, pytest.global_code, callbacks=[b])
    s.simulate()
    print(s.data.info())
    w = 'rsi_{}_{}'.format('close', t)
    assert w in s.data.columns
    real = talib.RSI(s.data['close'], t)
    assert pd.Series.equals(real, s.data[w])


def test_DEMA(init_global_data):
    t = 5
    b = cb_talib.DEMA(t)
    b.on_preparing_data(pytest.global_data)
    print(pytest.global_data.info())
    w = 'dema_close_{}'.format(t)
    assert w in pytest.global_data.columns
    real = talib.DEMA(pytest.global_data['close'], t)
    assert pd.Series.equals(real, pytest.global_data[w])

def test_RSI(init_global_data):
    t = 5
    b = cb_talib.RSI(t)
    b.on_preparing_data(pytest.global_data)
    print(pytest.global_data.info())
    w = 'rsi_close_{}'.format(t)
    assert w in pytest.global_data.columns
    real = talib.RSI(pytest.global_data['close'], t)
    assert pd.Series.equals(real, pytest.global_data[w])


def test_CCI(init_global_data):
    t = 5
    b = cb_talib.CCI(t)
    b.on_preparing_data(pytest.global_data)
    print(pytest.global_data.info())
    w = 'cci_high_low_close_5'  # 顺势指标
    assert w in pytest.global_data.columns
    real = talib.CCI(pytest.global_data['high'], pytest.global_data['low'],
                     pytest.global_data['close'], t)
    assert pd.Series.equals(real, pytest.global_data[w])


def test_MFI(mock_data):
    t = 14
    b = cb_talib.MFI(t)
    b.on_preparing_data(pytest.mock_data)
    print(pytest.mock_data.info())
    w = 'mfi_{}'.format(t)
    assert w in pytest.mock_data.columns
    real = talib.MFI(pytest.mock_data['high'], pytest.mock_data['low'],
                     pytest.mock_data['close'], pytest.mock_data['volume'], t)
    assert pd.Series.equals(real, pytest.mock_data[w])


def test_Sim_Rolling_Future(init_global_data):
    """测试通过回测调用Rolling_Future，逻辑与`test_Rolling_Future`一致"""
    data = pd.DataFrame({'close': [y for y in range(0, 10)]})

    t = 3
    s = Simulation(data,
                   pytest.global_code,
                   callbacks=[callbacks.Rolling_Future(t)])
    s.simulate()
    _min = 'rolling_{}_{}_min'.format('close', t)
    _max = 'rolling_{}_{}_max'.format('close', t)
    _mean = 'rolling_{}_{}_mean'.format('close', t)
    _med = 'rolling_{}_{}_med'.format('close', t)
    assert _min in s.data.columns
    assert _max in s.data.columns
    assert _mean in s.data.columns
    assert _med in s.data.columns
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 3.0, 4.0, 5.0, 6.0, 7.0, np.NaN, np.NaN, np.NaN]),
        s.data[_min])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 5.0, 6.0, 7.0, 8.0, 9.0, np.NaN, np.NaN, np.NaN]),
        s.data[_max])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 4.0, 5.0, 6.0, 7.0, 8.0, np.NaN, np.NaN, np.NaN]),
        s.data[_mean])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 4.0, 5.0, 6.0, 7.0, 8.0, np.NaN, np.NaN, np.NaN]),
        s.data[_med])


def test_Rolling_Future(init_global_data):
    data = pd.DataFrame({'close': [y for y in range(0, 10)]})

    t = 3
    b = callbacks.Rolling_Future(t)
    b.on_preparing_data(data)
    print(data.info())
    _min = 'rolling_{}_{}_min'.format('close', t)
    _max = 'rolling_{}_{}_max'.format('close', t)
    _mean = 'rolling_{}_{}_mean'.format('close', t)
    _med = 'rolling_{}_{}_med'.format('close', t)
    assert _min in data.columns
    assert _max in data.columns
    assert _mean in data.columns
    assert _med in data.columns
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 3.0, 4.0, 5.0, 6.0, 7.0, np.NaN, np.NaN, np.NaN]),
        data[_min])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 5.0, 6.0, 7.0, 8.0, 9.0, np.NaN, np.NaN, np.NaN]),
        data[_max])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 4.0, 5.0, 6.0, 7.0, 8.0, np.NaN, np.NaN, np.NaN]),
        data[_mean])
    assert pd.Series.equals(
        pd.Series(
            [np.NaN, np.NaN, 4.0, 5.0, 6.0, 7.0, 8.0, np.NaN, np.NaN, np.NaN]),
        data[_med])
