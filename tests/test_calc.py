from finance_tools_py.calc import position_unit

def test_position_unit():
    assert 1956==(position_unit(6.39,0.08,1000))