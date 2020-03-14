from datetime import date as dt

import numpy as np
import pandas as pd
import pytest
import talib

from finance_tools_py.simulation.callbacks import talib as cb_talib


@pytest.fixture
def init_global_data():
    pytest.global_code = '000001'
    pytest.global_data = pd.DataFrame({
        'code': [pytest.global_code for x in range(1998, 2020)],
        'date': [dt(y, 1, 1) for y in range(1998, 2020)],
        'close':
            np.random.random((len(list(range(1998, 2020))),)),
        'high':
            np.random.random((len(list(range(1998, 2020))),)),
        'low':
            np.random.random((len(list(range(1998, 2020))),)),
    })


def test_talib_DEMA(init_global_data):
    timeperiod = 3
    b = cb_talib.DEMA(timeperiod)
    b.close_name == 'close'
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    n = 'dema_close_{}'.format(timeperiod)
    assert n in pytest.global_data.columns
    real = talib.DEMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_TEMA(init_global_data):
    timeperiod = 3
    b = cb_talib.TEMA(timeperiod)
    b.close_name == 'close'
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    n = 'tema_close_{}'.format(timeperiod)
    assert n in pytest.global_data.columns
    real = talib.TEMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_ADX(init_global_data):
    timeperiod = 3
    b = cb_talib.ADX(timeperiod=timeperiod)
    assert b.close_name == 'close'
    assert b.high_name == 'high'
    assert b.low_name == 'low'
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    n = 'adx_high_low_close_{}'.format(timeperiod)
    assert n in pytest.global_data.columns
    real = talib.TEMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_WMA(init_global_data):
    timeperiod = 3
    b = cb_talib.WMA(timeperiod)
    b.close_name == 'close'
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    n = 'wma_close_{}'.format(timeperiod)
    assert n in pytest.global_data.columns
    real = talib.WMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_TRIMA(init_global_data):
    timeperiod = 3
    b = cb_talib.TRIMA(timeperiod)
    b.close_name == 'close'
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    n = 'trima_close_{}'.format(timeperiod)
    assert n in pytest.global_data.columns
    real = talib.TRIMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_T3(init_global_data):
    timeperiod = 3
    vfactor = 1
    b = cb_talib.T3(timeperiod, vfactor)
    b.close_name == 'close'
    assert b.timeperiod == timeperiod
    assert b.vfactor == vfactor
    b.on_preparing_data(pytest.global_data)
    n = 't3_close_{}_{}'.format(timeperiod, vfactor)
    assert n in pytest.global_data.columns
    real = talib.T3(pytest.global_data['close'], timeperiod, vfactor)
    pd.Series.equals(real, pytest.global_data[n])


def test_talib_EMA(init_global_data):
    timeperiod = 3
    b = cb_talib.EMA(timeperiod)
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    assert 'ema_close_{}'.format(timeperiod) in pytest.global_data.columns
    real = talib.EMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real,
                     pytest.global_data['ema_close_{}'.format(timeperiod)])


def test_talib_MAMA(init_global_data):
    fastlimit = 0.5
    slowlimit = 0.5
    b = cb_talib.MAMA(fastlimit, slowlimit)
    assert b.fastlimit == fastlimit
    assert b.slowlimit == slowlimit
    b.on_preparing_data(pytest.global_data)
    assert 'mama_close_{}_{}'.format(fastlimit,
                                     slowlimit) in pytest.global_data.columns
    assert 'fama_close_{}_{}'.format(fastlimit,
                                     slowlimit) in pytest.global_data.columns
    mama, fama = talib.MAMA(pytest.global_data['close'], fastlimit, slowlimit)
    pd.Series.equals(
        mama,
        pytest.global_data['mama_close_{}_{}'.format(fastlimit, slowlimit)])
    pd.Series.equals(
        fama,
        pytest.global_data['fama_close_{}_{}'.format(fastlimit, slowlimit)])


# def test_talib_MAVP(init_global_data):
#     periods = 7
#     minperiod = 2
#     maxperiod = 5
#     matype = 0
#     b = simulation.talib_MAVP(periods, minperiod, maxperiod, matype)
#     assert b.periods == periods
#     assert b.minperiod == minperiod
#     assert b.maxperiod == maxperiod
#     assert b.matype == matype
#     b.on_preparing_data(pytest.global_data)
#     assert 'mavp_close_{}_{}_{}_{}'.format(periods, minperiod, maxperiod, matype) in pytest.global_data.columns
#     real = talib.MAVP(pytest.global_data['close'], periods, minperiod, maxperiod, matype)
#     pd.Series.equals(real, pytest.global_data['mavp_close_{}_{}_{}_{}'.format(periods, minperiod, maxperiod, matype)])


def test_talib_MA(init_global_data):
    timeperiod = 3
    matype = 1
    b = cb_talib.MA(timeperiod, matype)
    assert b.timeperiod == timeperiod
    assert b.matype == matype
    b.on_preparing_data(pytest.global_data)
    assert 'ma_close_{}_{}'.format(timeperiod,
                                   matype) in pytest.global_data.columns
    real = talib.MA(pytest.global_data['close'], timeperiod, matype)
    pd.Series.equals(
        real, pytest.global_data['ma_close_{}_{}'.format(timeperiod, matype)])


def test_talib_KAMA(init_global_data):
    timeperiod = 3
    b = cb_talib.KAMA(timeperiod)
    assert b.timeperiod == timeperiod
    b.on_preparing_data(pytest.global_data)
    assert 'kama_close_{}'.format(timeperiod) in pytest.global_data.columns
    real = talib.KAMA(pytest.global_data['close'], timeperiod)
    pd.Series.equals(real,
                     pytest.global_data['kama_close_{}'.format(timeperiod)])


def test_talib_HT_TRENDLINE(init_global_data):
    b = cb_talib.HT_TRENDLINE()
    b.on_preparing_data(pytest.global_data)
    assert 'ht_trendline_close' in pytest.global_data.columns
    real = talib.HT_TRENDLINE(pytest.global_data['close'])
    pd.Series.equals(real, pytest.global_data['ht_trendline_close'])


def test_talib_Bolling(init_global_data):
    timeperiod = 3
    nbdevup = 2.1
    nbdevdn = 2.4
    b = cb_talib.BBANDS(timeperiod, nbdevup, nbdevdn)
    assert b.timeperiod == timeperiod
    assert b.nbdevdn == nbdevdn
    assert b.nbdevup == nbdevup
    b.on_preparing_data(pytest.global_data)
    # 默认取值列为 close
    assert 'boll_close_{}_{}_{}_up'.format(
        timeperiod, nbdevup, nbdevdn) in pytest.global_data.columns
    assert 'boll_close_{}_{}_{}_mean'.format(
        timeperiod, nbdevup, nbdevdn) in pytest.global_data.columns
    assert 'boll_close_{}_{}_{}_low'.format(
        timeperiod, nbdevup, nbdevdn) in pytest.global_data.columns
    up, mean, low = talib.BBANDS(pytest.global_data['close'], timeperiod,
                                 nbdevup, nbdevdn)
    pd.Series.equals(
        up, pytest.global_data['boll_close_{}_{}_{}_up'.format(
            timeperiod, nbdevup, nbdevdn)])
    pd.Series.equals(
        mean, pytest.global_data['boll_close_{}_{}_{}_mean'.format(
            timeperiod, nbdevup, nbdevdn)])
    pd.Series.equals(
        low, pytest.global_data['boll_close_{}_{}_{}_low'.format(
            timeperiod, nbdevup, nbdevdn)])


def test_talib_Linear_Angle(init_global_data):
    timeperiod = 3
    a = cb_talib.Linear_Angle(timeperiod)
    a.on_preparing_data(pytest.global_data)
    assert a.timeperiod == timeperiod
    assert 'linear_angle_close_{}'.format(
        timeperiod) in pytest.global_data.columns
    pd.Series.equals(
        talib.LINEARREG_ANGLE(pytest.global_data['close'], timeperiod),
        pytest.global_data['linear_angle_close_{}'.format(timeperiod)])

# def test_Pandas_Rolling(init_global_data):
#     min_periods = 3
#     window = 5
#     b = simulation.Pandas_Rolling(min_periods, window)
#     b.on_preparing_data(pytest.global_data)
#     for n in ['sum', 'mean', 'median', 'var', 'std', 'min', 'max', 'corr', 'cov', 'skew', 'kurt']:
#         col = 'rolling_{}_{}_{}'.format(window, min_periods, n)
#         assert col in pytest.global_data.columns
