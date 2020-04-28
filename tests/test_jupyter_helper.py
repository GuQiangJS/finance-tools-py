from finance_tools_py._jupyter_helper import report_metrics
import pandas as pd


def test_example_metrics():
    rep = report_metrics(pd.Series([-0.012143, 0.045350, 0.030957, 0.004902]),
                         pd.Series([-0.112143, 0.145350, 0.130957, 0.104902]))
    print(rep)
