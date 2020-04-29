回测时的回调
================

.. toctree::
   :maxdepth: 5

回调基类
------------------------------

所有回调均派生自此类型

.. autoclass:: finance_tools_py.backtest.CallBack
    :members:


可以控制止盈/止损/加仓的策略回调
------------------------------------------
.. autoclass:: finance_tools_py.backtest.TurtleStrategy
    :members:
    :special-members: __init__,
    :inherited-members:
    :show-inheritance:


最小买卖的回调
------------------------------------------
.. autoclass:: finance_tools_py.backtest.MinAmountChecker
    :members:
    :special-members: __init__,
    :inherited-members:
    :show-inheritance:

全部资金出的回调
------------------------------------------
.. autoclass:: finance_tools_py.backtest.AllInChecker
    :members:
    :special-members: __init__,
    :inherited-members:
    :show-inheritance:
