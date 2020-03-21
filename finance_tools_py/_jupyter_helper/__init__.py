import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import sys

IN_COLAB = 'google.colab' in sys.modules

def read_data_QFQ(symbol='600036') -> pd.DataFrame:
    """读取前复权数据"""
    if not IN_COLAB:
        raise NotImplementedError()
    data = pd.read_csv(
        'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
        format(symbol),
        parse_dates=True,
        usecols=[
            'date', 'open_qfq', 'high_qfq', 'low_qfq', 'close_qfq',
            'volume_qfq'
        ])
    data['date'] = pd.to_datetime(data['date'])
    data.rename(columns={
        'open_qfq': 'open',
        'high_qfq': 'high',
        'low_qfq': 'low',
        'close_qfq': 'close',
        'volume_qfq': 'volume'
    },
                inplace=True)
    # data['preclose']=data['close'].shift()
    # data['nextclose']=data['close'].shift(-1)
    # data['nextchange']=data['nextclose']-data['close']
    # data['nextchange_sign']=np.sign(data['nextchange'])
    return data


def read_data_HFQ(symbol='600036') -> pd.DataFrame:
    """读取后复权数据"""
    if not IN_COLAB:
        raise NotImplementedError()
    data = pd.read_csv(
        'https://raw.githubusercontent.com/GuQiangJS/temp/master/{}_daily.csv'.
        format(symbol),
        parse_dates=True,
        usecols=[
            'date', 'open_hfq', 'high_hfq', 'low_hfq', 'close_hfq',
            'volume_hfq'
        ])
    data['date'] = pd.to_datetime(data['date'])
    data.rename(columns={
        'open_hfq': 'open',
        'high_hfq': 'high',
        'low_hfq': 'low',
        'close_hfq': 'close',
        'volume_hfq': 'volume'
    },
                inplace=True)
    # data['preclose']=data['close'].shift()
    # data['nextclose']=data['close'].shift(-1)
    # data['nextchange']=data['nextclose']-data['close']
    # data['nextchange_sign']=np.sign(data['nextchange'])
    return data


def plot_backtest(data, x, y, buy=None, sell=None):
    if isinstance(y, str):
        y = [y]
    plot_backtest_plotly(data, x, y, buy, sell).show()
    plot_backtest_seaborn(data, x, y, buy, sell)
    plt.show()


def plot_backtest_plotly(data, x, y, buy=None, sell=None, col='close'):
    """使用plotly绘制回测后的数据，数据上会标记买入点和卖出点"""
    if isinstance(y, str):
        y = [y]
    fig = go.Figure()
    for y1 in y:
        fig.add_trace(go.Scatter(x=data[x], y=data[y1], mode='lines', name=y1))
    if buy:
        b = data[data[x].isin(buy)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[col],
                       mode='markers',
                       marker=dict(color="red", size=6)))
    if sell:
        b = data[data[x].isin(sell)]
        fig.add_trace(
            go.Scatter(x=b[x],
                       y=b[col],
                       mode='markers',
                       marker=dict(color="green", size=6)))
    return fig


def plot_backtest_seaborn(data, x, y, buy=None, sell=None, figsize=(20, 6), col='close'):
    """使用seaborn绘制回测后的数据，数据上会标记买入点和卖出点"""
    if isinstance(y, str):
        y = [y]
    fig = plt.figure(figsize=figsize)
    for y1 in y:
        sns.lineplot(data=data, x=x, y=y1)
    if buy:
        b = data[data[x].isin(buy)]
        plt.plot(b[x], b[col], 'r.')
    if sell:
        b = data[data[x].isin(sell)]
        plt.plot(b[x], b[col], 'gx')
    return fig
