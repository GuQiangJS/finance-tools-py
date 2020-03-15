.. module:: finance_tools_py.simulation.callbacks.talib

.. toctree::
   :maxdepth: 5

趋势型指标计算回调
---------------------------------

实现 talib 中 `Overlap Studies`_ 相关函数的回调。

.. _Overlap Studies: https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

* :py:class:`BBANDS` BBANDS - Bollinger Bands

BBANDS - Bollinger Bands
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

简介：其利用统计原理，求出股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。

分析和应用：`百度百科 <https://baike.baidu.com/item/bollinger%20bands/1612394?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/56d0d9be66b4f7a0?rid=53>`__

.. autoclass:: BBANDS
    :exclude-members: on_preparing_data
    :inherited-members: CallBack


动量指标计算回调
---------------------------------

实现 talib 中 `Momentum Indicators`_ 相关函数的回调。

.. _Momentum Indicators: https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html

* :py:class:`WILLR` WILLR - Williams’ %R 威廉指标

WILLR - Williams’ %R 威廉指标
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

简介：WMS表示的是市场处于超买还是超卖状态。股票投资分析方法主要有如下三种：基本分析、技术分析、演化分析。在实际应用中，它们既相互联系，又有重要区别。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A0%87?fr=aladdin>`__
`维基百科 <https://zh.wikipedia.org/wiki/%E5%A8%81%E5%BB%89%E6%8C%87%E6%A8%99>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/967febb0316c57c1>`__

.. autoclass:: WILLR
    :exclude-members: on_preparing_data
    :inherited-members: col_close
