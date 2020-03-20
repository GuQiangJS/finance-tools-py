.. py:currentmodule:: finance_tools_py.simulation.callbacks.talib

.. toctree::
   :maxdepth: 5

趋势型指标计算回调
---------------------------------

实现 talib 中 `Overlap Studies`_ 相关函数的回调。

.. _Overlap Studies: https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

* :py:class:`BBANDS` BBANDS - Bollinger Bands
* :py:class:`DEMA` DEMA - Double Exponential Moving Average 双移动平均线

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


动量指标计算回调
---------------------------------

实现 talib 中 `Momentum Indicators`_ 相关函数的回调。

.. _Momentum Indicators: https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html

* :py:class:`CCI` 威廉指标
* :py:class:`MFI` 资金流量指标
* :py:class:`WILLR` 威廉指标



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
