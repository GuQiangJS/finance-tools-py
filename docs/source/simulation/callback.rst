.. py:currentmodule:: finance_tools_py.simulation.callbacks

模拟工具使用的回调
******************************

.. toctree::
   :maxdepth: 5


talib函数相关
----------------------

.. toctree::
   :maxdepth: 5

   callback_talib

其他回调
----------------------

**计算未来数据的回调**

.. autoclass:: Rolling_Future
    :members:
    :inherited-members: col_close
    :exclude-members: on_preparing_data


**回调基类**

.. autoclass:: CallBack
    :members:
    :show-inheritance: False