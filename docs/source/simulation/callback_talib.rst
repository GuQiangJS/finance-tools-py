.. module:: finance_tools_py.simulation.callbacks.talib

.. toctree::
   :maxdepth: 5

趋势型指标计算回调
---------------------------------

实现 talib 中 `Overlap Studies`_ 相关函数的回调。

.. _Overlap Studies: https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html

* :py:class:`BBANDS` 布林带 BBANDS
* :py:class:`DEMA` 双指数移动平均 DEMA
* :py:class:`EMA` 指数移动平均 EMA
* :py:class:`HT_TRENDLINE` 希尔伯特变换-瞬时趋势 Hilbert Transform
* :py:class:`KAMA` 考夫曼自适应移动平均 KAMA
* :py:class:`MA` 移动平均 MA
* :py:class:`MAMA` MESA自适应移动平均 MAMA
* :py:class:`MIDPOINT` 中间点指标 MIDPOINT
* :py:class:`SMA` 简单移动均线指标 SMA
* :py:class:`T3` 双指数移动均线改进指标 T3
* :py:class:`TEMA` 三重指数移动均线指标 TEMA
* :py:class:`TRIMA` 三指数移动平均 TRIMA
* :py:class:`WMA` 加权移动均线指标 WMA

布林带  BBANDS
""""""""""""""""""""""""""""""
BBANDS - Bollinger Bands

简介：其利用统计原理，求出股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。

分析和应用：`百度百科 <https://baike.baidu.com/item/bollinger%20bands/1612394?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/56d0d9be66b4f7a0?rid=53>`__

.. autoclass:: BBANDS
    :members:
    :inherited-members: close_name

希尔伯特变换-瞬时趋势 Hilbert Transform
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline

简介：是一种趋向类指标，其构造原理是仍然对价格收盘价进行算术平均，并根据计算结果来进行分析，用于判断价格未来走势的变动趋势。

分析和应用： `百度文库 <https://wenku.baidu.com/view/0e35f6eead51f01dc281f18e.html>`__

.. autoclass:: HT_TRENDLINE
    :members:
    :inherited-members: close_name

双指数移动平均 DEMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Double Exponential Moving Average

简介：两条移动平均线来产生趋势信号，较长期者用来识别趋势，较短期者用来选择时机。正是两条平均线及价格三者的相互作用，才共同产生了趋势信号。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E5%8F%8C%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF/1831921?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/a04d723659318237>`__

.. autoclass:: DEMA
    :members:
    :inherited-members: close_name

双指数移动均线改进指标 T3
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

简介：双指数移动均线改进指标T3是对DEMA指标的简单改进。
TRIX长线操作时采用本指标的讯号，长时间按照本指标讯号交易，获利百分比大于损失百分比，利润相当可观。
比如日线MA5指5天内的收盘价除以5 。

分析和应用：`百度百科 <https://baike.baidu.com/item/%E4%B8%89%E9%87%8D%E6%8C%87%E6%95%B0%E5%B9%B3%E6%BB%91%E5%B9%B3%E5%9D%87%E7%BA%BF/15749345?fr=aladdin>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/6c22c15ccbf24e64?rid=80>`__

.. autoclass:: T3
    :members:
    :inherited-members: close_name

三重指数移动均线指标 TEMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

简介：与T3类似，三重指数移动均线指标TEMA也是对价格进行迭代计算。不同的是，这里采用的是指数移动平均EMA。

.. autoclass:: TEMA
    :members:
    :inherited-members: close_name

加权移动均线指标 WMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
WMA - Weighted Moving Average

简介：加权移动平均线WMA，其比重是以平均线的长度设定，愈近期的收市价，对市况影响愈重要。
计算方式是基于加权移动平均线日数，将每一个之前日数比重提升。
每一价格会乘以一个比重，最新的价格会有最大的比重，其之前的每一日的比重将会递减。

移动加权平均法是指以每次进货的成本加上原有库存存货的成本，除以每次进货数量与原有库存存货的数量之和，
据以计算加权平均单位成本，以此为基础计算当月发出存货的成本和期末存货的成本的一种方法。

.. autoclass:: WMA
    :members:
    :inherited-members: close_name

三指数移动平均 TRIMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. autoclass:: TRIMA
    :members:
    :inherited-members: close_name

指数移动平均 EMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
EMA - Exponential Moving Average

简介：是一种趋向类指标，其构造原理是仍然对价格收盘价进行算术平均，并根据计算结果来进行分析，用于判断价格未来走势的变动趋势。

分析和应用：`百度百科 <https://baike.baidu.com/item/EMA/12646151>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/b7a39d74783ad689?rid=589>`__



.. autoclass:: EMA
    :members:
    :inherited-members: close_name

考夫曼自适应移动平均 KAMA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
KAMA - Kaufman Adaptive Moving Average

简介：短期均线贴近价格走势，灵敏度高，但会有很多噪声，产生虚假信号；长期均线在判断趋势上一般比较准确 ，
但是长期均线有着严重滞后的问题。我们想得到这样的均线，当价格沿一个方向快速移动时，短期的移动 平均线是最合适的；
当价格在横盘的过程中，长期移动平均线是合适的。

分析和应用：`参考1 <http://blog.sina.com.cn/s/blog_62d0bbc701010p7d.html>`__
`参考2 <https://wenku.baidu.com/view/bc4bc9c59ec3d5bbfd0a7454.html?from=search>`__

.. autoclass:: KAMA
    :members:
    :inherited-members: close_name

移动平均 MA
""""""""""""""""""""""""""""""""""
MA - Moving average 移动平均线

简介：移动平均线，Moving Average，简称MA，原本的意思是移动平均，由于我们将其制作成线形，所以一般称之为移动平均线，简称均线。它是将某一段时间的收盘价之和除以该周期。 比如日线MA5指5天内的收盘价除以5 。


分析和应用：`百度百科 <https://baike.baidu.com/item/%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF/217887?fromtitle=MA&fromid=1511750#viewPageContent>`__
`同花顺学院 <http://www.iwencai.com/yike/detail/auid/a04d723659318237?rid=96>`__

.. autoclass:: MA
    :members:
    :inherited-members: close_name

MESA自适应移动平均 MAMA
""""""""""""""""""""""""""""""""""
MESA自适应移动平均

.. autoclass:: MAMA
    :members:
    :inherited-members: close_name

中间点指标 MIDPOINT
""""""""""""""""""""""""""""""""""

简介：MIDPOINT用来反映价格在某一个周期区间内的总体平均水平。它反映了该价格在某一时间范围内的水平。
与简单移动平均不同的是，MIDPOINT不关心价格的变动轨迹，而只反映价格变动的极值，是收盘价最大值和最小值的平均值。

.. autoclass:: MIDPOINT
    :members:
    :inherited-members: close_name

简单移动均线指标 SMA
""""""""""""""""""""""""""""""""""

简介：简单移动平均线SMA，又称“算术移动平均线”，是指对特定期间的收盘价进行简单平均化。
一般所提及之移动平均线即指简单移动平均线。

.. autoclass:: SMA
    :members:
    :inherited-members: close_name

动量型指标计算回调
---------------------------------

实现 talib 中 `Statistic Functions`_ 相关函数的回调。

.. _Momentum Indicator Functions: https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html

* :py:class:`ADX` 平均趋向指数 ADX



平均趋向指数 ADX
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
简介：平均趋向指数ADX是一种常用的趋势衡量指标。ADX指数是反映趋向变动的程度，而不是方向本身。
也即是说，ADX无法告诉你趋势的发展方向，但如果趋势存在，它可以衡量趋势的强度。
使用ADX指标，指标判断盘整、振荡和单边趋势。

**特点：**

* ADX无法告诉你趋势的发展方向。
* 如果趋势存在，ADX可以衡量趋势的强度。不论上升趋势或下降趋势，ADX看起来都一样。
* ADX的读数越大，趋势越明显。衡量趋势强度时，需要比较几天的ADX 读数，观察ADX究竟是上升或下降。ADX读数上升，代表趋势转强；如果ADX读数下降，意味着趋势转弱。
* 当ADX曲线向上攀升，趋势越来越强，应该会持续发展。如果ADX曲线下滑，代表趋势开始转弱，反转的可能性增加。
* 单就ADX本身来说，由于指标落后价格走势，所以算不上是很好的指标，不适合单就ADX进行操作。可是，如果与其他指标配合运用，ADX可以确认市场是否存在趋势，并衡量趋势的强度。

**指标应用：**

* +DI与–DI表示多空相反的二个动向，当据此绘出的两条曲线彼此纠结相缠时，代表上涨力道与下跌力道相当，多空势均力敌。当 +DI与–DI彼此穿越时，由下往上的一方其力道开始压过由上往下的另一方，此时出现买卖讯号。
* ADX可作为趋势行情的判断依据，当行情明显朝多空任一方向进行时，ADX数值都会显著上升，趋势走强。若行情呈现盘整格局时，ADX会低于 +DI与–DI二条线。若ADX数值低于20，则不论DI表现如何，均显示市场没有明显趋势。
* ADX持续偏高时，代表“超买”（Overbought）或“超卖”（Oversold）的现象，行情反转的机会将增加，此时则不适宜顺势操作。当ADX数值从上升趋势转为下跌时，则代表行情即将反转；若ADX数值由下跌趋势转为上升时，行情将止跌回升。
* 总言之，DMI指标包含4条线：+DI、-DI、ADX和ADXR。+DI代表买盘的强度、-DI代表卖盘的强度；ADX代表趋势的强度、ADXR则为ADX的移动平均。

.. autoclass:: ADX
    :members:
    :inherited-members: close_name,high_name,low_name



统计相关计算回调
---------------------------------

实现 talib 中 `Statistic Functions`_ 相关函数的回调。

.. _Statistic Functions: https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html

* :py:class:`Linear_Angle` 线性回归角度 LINEARREG_ANGLE - Linear Regression Angle


线性回归角度 LINEARREG_ANGLE
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
简介：来确定价格的角度变化.

分析和应用：`参考 <http://blog.sina.com.cn/s/blog_14c9f45b20102vv8p.md>`_

.. autoclass:: Linear_Angle
    :members:
    :inherited-members: close_name
