.. py:currentmodule:: finance_tools_py.simulation.callbacks.talib

.. toctree::
   :maxdepth: 5

趋势型指标计算回调
---------------------------------

实现 talib 中 `Overlap Studies`_ 相关函数的回调。

.. _Overlap Studies: https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

* :py:class:`BBANDS` BBANDS - Bollinger Bands
* :py:class:`SMA` SMA - Simple Moving Average 简单移动平均线
* :py:class:`DEMA` DEMA - Double Exponential Moving Average 双移动平均线
* :py:class:`EMA` EMA - Exponential Moving Average 指数移动平均线
* :py:class:`WMA` WMA - Weighted Moving Average 移动加权平均法

**BBANDS - Bollinger Bands**

简介：其利用统计原理，求出股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。

分析和应用：`百度百科 <https://baike.baidu.com/item/bollinger%20bands/1612394?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/56d0d9be66b4f7a0?rid=53>`__

.. autoclass:: BBANDS
    :exclude-members: on_preparing_data
    :inherited-members: col_close

**DEMA - Double Exponential Moving Average 双移动平均线**

简介：两条移动平均线来产生趋势信号，较长期者用来识别趋势，较短期者用来选择时机。正是两条平均线及价格三者的相互作用，才共同产生了趋势信号。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E5%8F%8C%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF/1831921?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/a04d723659318237>`__

.. autoclass:: DEMA
    :exclude-members: on_preparing_data
    :inherited-members: col_close



**SMA - Simple Moving Average 简单移动平均线**

简介：移动平均线，Moving Average，简称MA，原本的意思是移动平均，由于我们将其制作成线形，所以一般称之为移动平均线，简称均线。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF/217887?fromtitle=MA&fromid=1511750#viewPageContent>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/a04d723659318237?rid=96>`__

.. autoclass:: SMA
    :exclude-members: on_preparing_data
    :inherited-members: col_close



**EMA - Exponential Moving Average 指数移动平均线**

简介：是一种趋向类指标，其构造原理是仍然对价格收盘价进行算术平均，并根据计算结果来进行分析，用于判断价格未来走势的变动趋势。

分析和应用：`百度百科 <https://baike.baidu.com/item/EMA/12646151>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/b7a39d74783ad689?rid=589>`__

.. autoclass:: EMA
    :exclude-members: on_preparing_data
    :inherited-members: col_close


**WMA - Weighted Moving Average 移动加权平均法**

简介：移动加权平均法是指以每次进货的成本加上原有库存存货的成本，除以每次进货数量与原有库存存货的数量之和，据以计算加权平均单位成本，以此为基础计算当月发出存货的成本和期末存货的成本的一种方法。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E7%A7%BB%E5%8A%A8%E5%8A%A0%E6%9D%83%E5%B9%B3%E5%9D%87%E6%B3%95/10056490?fr=aladdin&fromid=16799870&fromtitle=%E5%8A%A0%E6%9D%83%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/262b1dfd1c68ee30>`__

.. autoclass:: WMA
    :exclude-members: on_preparing_data
    :inherited-members: col_close



动量指标计算回调
---------------------------------

实现 talib 中 `Momentum Indicators`_ 相关函数的回调。

.. _Momentum Indicators: https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html

* :py:class:`CCI` 顺势指标
* :py:class:`MFI` 资金流量指标
* :py:class:`WILLR` 威廉指标
* :py:class:`RSI` 相对强弱指数



**CCI - Commodity Channel Index 顺势指标**

简介：CCI指标专门测量股价是否已超出常态分布范围

* 当CCI指标曲线在+100线～-100线的常态区间里运行时,CCI指标参考意义不大，可以用KDJ等其它技术指标进行研判。
* 当CCI指标曲线从上向下突破+100线而重新进入常态区间时，表明市场价格的上涨阶段可能结束，将进入一个比较长时间的震荡整理阶段，应及时平多做空。
* 当CCI指标曲线从上向下突破-100线而进入另一个非常态区间（超卖区）时，表明市场价格的弱势状态已经形成，将进入一个比较长的寻底过程，可以持有空单等待更高利润。如果CCI指标曲线在超卖区运行了相当长的一段时间后开始掉头向上，表明价格的短期底部初步探明，可以少量建仓。CCI指标曲线在超卖区运行的时间越长，确认短期的底部的准确度越高。
* CCI指标曲线从下向上突破-100线而重新进入常态区间时，表明市场价格的探底阶段可能结束，有可能进入一个盘整阶段，可以逢低少量做多。
* CCI指标曲线从下向上突破+100线而进入非常态区间(超买区)时，表明市场价格已经脱离常态而进入强势状态，如果伴随较大的市场交投，应及时介入成功率将很大。
* CCI指标曲线从下向上突破+100线而进入非常态区间(超买区)后，只要CCI指标曲线一直朝上运行，表明价格依然保持强势可以继续持有待涨。但是，如果在远离+100线的地方开始掉头向下时，则表明市场价格的强势状态将可能难以维持，涨势可能转弱，应考虑卖出。如果前期的短期涨幅过高同时价格回落时交投活跃，则应该果断逢高卖出或做空。

CCI主要是在超买和超卖区域发生作用，对急涨急跌的行情检测性相对准确。非常适用于股票、外汇、贵金属等市场的短期操作。

.. autoclass:: CCI
    :exclude-members: on_preparing_data
    :inherited-members: col_close,col_high,col_low


**MFI - Money Flow Index 资金流量指标**

资金流量指标（MFI）又称为量相对强弱指标（Volume Relative Strength Index，VRSI），英文全名Money Flow Index，缩写为MFI，根据成交量来计测市场供需关系和买卖力道。该指标是通过反映股价变动的四个元素：上涨的天数、下跌的天数、成交量增加幅度、成交量减少幅度来研判量能的趋势，预测市场供求关系和买卖力道，属于量能反趋向指标。

经过长期测试，MFI指标的背离讯号更能忠实的反应股价的反转现象。一次完整的波段行情，至少都会维持一定相当的时间，反转点出现的次数并不会太多。

将MFI指标的参数设定为14天时，其背离讯号产生的时机，大致上都能和股价的顶点吻合。因此在使用MFI指标时，参数设定方面应尽量维持14日的原则。

.. autoclass:: MFI
    :exclude-members: on_preparing_data
    :inherited-members: col_close,col_high,col_low

**WILLR - Williams’ %R 威廉指标**

简介：WMS表示的是市场处于超买还是超卖状态。股票投资分析方法主要有如下三种：基本分析、技术分析、演化分析。在实际应用中，它们既相互联系，又有重要区别。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A0%87?fr=aladdin>`__
`维基百科 <https://zh.wikipedia.org/wiki/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A8%99>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/967febb0316c57c1>`__

.. autoclass:: WILLR
    :exclude-members: on_preparing_data
    :inherited-members: col_close


**RSI - Relative Strength Index 相对强弱指数**

简介：通过比较一段时期内的平均收盘涨数和平均收盘跌数来分析市场买沽盘的意向和实力，从而作出未来市场的走势。

RSI值将0到100之间分成了从"极弱"、"弱""强"到"极强"四个区域。
"强"和"弱"以50作为分界线,但"极弱"和"弱"之间以及"强"和"极强"之间的界限则要随着RSI参数的变化而变化。
不同的参数,其区域的划分就不同。一般而言,参数越大,分界线离中心线50就越近,离100和0就越远。
不过一般都应落在15、30到70、85的区间内。
RSI值如果超过50,表明市场进入强市,可以考虑买入,但是如果继续进入"极强"区,就要考虑物极必反,准备卖出了。
同理RSI值在50以下也是如此,如果进入了"极弱"区,则表示超卖,应该伺机买入。

分析和应用：`百度百科 <https://baike.baidu.com/item/RSI/6130115#3>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/6a280c6cebcf140a?rid=>`__

.. autoclass:: RSI
    :exclude-members: on_preparing_data
    :inherited-members: col_close

波动率型指标计算回调
---------------------------------

实现 talib 中 `Volatility Indicator`_ 相关函数的回调。

.. Volatility Indicators: https://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html

* :py:class:`ATR` 平均真实波幅指标
* :py:class:`NATR` 归一化平均真实波幅

**ATR - Average True Range - 平均真实波幅指标**

简介：均幅指标是显示市场变化率的指标，由威尔德（Welles Wilder）在《技术交易系统中的新概念》一书中首次提出，已成为众多指标经常引用的技术量。威尔德发现较高的ATR值常发生在市场底部，并伴随恐慌性抛盘。当其值较低时，则往往发生在合并以后的市场顶部。

著名的海龟法则中,海龟交易法则按照价格高于初始价格0.5ATR进行加仓操作,按照价格低于建仓价2ATR进行止损操作。

均幅指标一般不单独使用，应结合其他指标综合研判。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E5%9D%87%E5%B9%85%E6%8C%87%E6%A0%87/3618107>`__

.. autoclass:: ATR
    :exclude-members: on_preparing_data
    :inherited-members: col_close,col_high,col_low


**NATR - Normalized Average True Range**

简介：归一化平均真实波幅是对平均真实波幅的一种改进。NATR在ATR的基础上，将ATR的值进行归一化，便于跨期比较。

.. autoclass:: NATR
    :exclude-members: on_preparing_data
    :inherited-members: col_close,col_high,col_low