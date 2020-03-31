.. py:currentmodule:: finance_tools_py._jupyter_helper

jupyter notebook 中可能用到的常用方法封装
================================================================

.. toctree::
   :maxdepth: 5


回测相关
---------------------------------

* :py:meth:`BACKTEST_PACK_ALL` 跨年度回测
* :py:meth:`BACKTEST_PACK_YEAR` 按年度回测
* :py:meth:`BACKTEST_SINGLE` 单支股票回测
* :py:meth:`RANDMON_TEST_BASIC` 随机回测
* :py:meth:`SIMULATE_DATA` 循环处理所有数据

绘图相关
---------------------------------

* :py:meth:`plot_backtest_plotly` 使用plotly绘制回测后的数据
* :py:meth:`plot_backtest_seaborn` 使用seaborn绘制回测后的数据

跨年度回测
~~~~~~~~~~~~~~~
.. automethod:: finance_tools_py._jupyter_helper::BACKTEST_PACK_ALL

按年度回测
~~~~~~~~~~~~~~~
.. automethod:: finance_tools_py._jupyter_helper::BACKTEST_PACK_YEAR

单支股票回测
~~~~~~~~~~~~~~~
.. automethod:: finance_tools_py._jupyter_helper::BACKTEST_SINGLE

随机回测
~~~~~~~~~~~~~~~
.. automethod:: finance_tools_py._jupyter_helper::RANDMON_TEST_BASIC

使用plotly绘制回测后的数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
单支股票用

.. automethod:: finance_tools_py._jupyter_helper::plot_backtest_plotly

使用seaborn绘制回测后的数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
单支股票用

.. automethod:: finance_tools_py._jupyter_helper::plot_backtest_seaborn
