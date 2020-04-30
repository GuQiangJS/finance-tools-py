from finance_tools_py.calc import position_unit
from finance_tools_py.calc import fluidity
import pandas as pd

def test_position_unit():
    assert 1956==(position_unit(6.39,0.08,1000))

def test_fluidity():
    df=pd.DataFrame({'code':['001','001','002','002','003','003'],
                     'amount':[100,100,200,400,1000,3000],
                     'rets':[0.01,0.23,0.02,0.55,0.10,0.45]})
    print(df)
    print(fluidity(df))