模拟工具使用的回调
===============================


回调基类
------------------------------

所有回调均派生自此类型

.. autoclass:: finance_tools_py.simulation.CallBack
    :members:
    :special-members: __init__,

布林带回调
------------------------------

调用 ``talib.BBANDS`` 方法生成布林线。并工具布林线计算简单的买入卖出点。

.. autoclass:: finance_tools_py.simulation.CallBack_Bolling
    :members:
    :special-members: __init__,

简单移动平均回调
------------------------------

根据 pandas 中的简单移动平均函数，计算平均值和标准差。

.. autoclass:: finance_tools_py.simulation.Pandas_Rolling
    :members:
    :special-members: __init__,

线性角度回调
------------------------------

调用 ``talib.LINEARREG_ANGLE`` 线性角度。

.. autoclass:: finance_tools_py.simulation.Linear_Angle
    :members:
    :special-members: __init__,

合并多个回调生成买入卖出标记的回调
----------------------------------------

自动合并 :py:class:`finance_tools_py.simulation.CallBack_Bolling` ,
:py:class:`finance_tools_py.simulation.Pandas_Rolling` ,
:py:class:`finance_tools_py.simulation.Linear_Angle` 回调
生成的数据，并产生买入卖出信号列。

.. autoclass:: finance_tools_py.simulation.CalcTradePoint
    :members:
    :special-members: __init__,
