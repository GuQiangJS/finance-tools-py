import datetime

import pytest

from finance_tools_py.order import Order
from finance_tools_py.order import OrderQueue
from finance_tools_py.parameters import MARKET_TYPE
from finance_tools_py.parameters import ORDER_DIRECTION


@pytest.fixture
def default_data():
    pytest.def_code = "000"
    pytest.def_price = 18.1
    pytest.def_amount = 100
    pytest.def_date = datetime.datetime(2020, 3, 1)
    pytest.def_order = Order(pytest.def_code, pytest.def_price, pytest.def_date,
                             pytest.def_amount)


def test_order_calc_tax(default_data):
    """测试印花税计算"""
    assert pytest.def_order.calc_tax() == pytest.def_price * pytest.def_amount * pytest.def_order.tax_coeff
    assert pytest.def_order.calc_tax(
        trade_price=28) == 28 * pytest.def_amount * pytest.def_order.tax_coeff
    assert pytest.def_order.calc_tax(trade_price=14.5,
                                     trade_amount=500) == 14.5 * 500 * pytest.def_order.tax_coeff


def test_order_calc_commission(default_data):
    """测试交易手续费计算"""
    assert pytest.def_order.calc_commission() == max(
        pytest.def_price * pytest.def_amount * pytest.def_order.commission_coeff,
        pytest.def_order.min_commisssion_coeff)
    assert pytest.def_order.calc_commission(trade_amount=1000) == max(
        pytest.def_price * 1000 * pytest.def_order.commission_coeff,
        pytest.def_order.min_commisssion_coeff)


def test_order_totalmoney(default_data):
    assert pytest.def_order.total_money == pytest.def_price * pytest.def_amount + pytest.def_order.calc_tax() + pytest.def_order.calc_commission()


def test_order_todict(default_data):
    d = {'date': pytest.def_order.date,
         'price': pytest.def_order.price,
         'amount': pytest.def_order.amount,
         'direction': pytest.def_order.direction,
         'code': pytest.def_order.code,
         'market_type': pytest.def_order.market_type}
    assert pytest.def_order.to_dict() == d


def test_order_fromdict(default_data):
    d = {'date': datetime.datetime(2020, 2, 29),
         'price': 1234,
         'amount': 5678,
         'direction': ORDER_DIRECTION.SELL,
         'code': "111",
         'market_type': MARKET_TYPE.STOCK_CN}
    assert pytest.def_order.direction == ORDER_DIRECTION.BUY
    assert pytest.def_order.amount == pytest.def_amount
    assert pytest.def_order.price == pytest.def_price
    assert pytest.def_order.code == pytest.def_code
    assert pytest.def_order.date == pytest.def_date
    pytest.def_order.from_dict(d)
    assert pytest.def_order.direction == d['direction']
    assert pytest.def_order.amount == d['amount']
    assert pytest.def_order.price == d['price']
    assert pytest.def_order.code == d['code']
    assert pytest.def_order.date == d['date']


def test_orderqueue_calc():
    o1=Order("",10,datetime.datetime.today(),1000)
    o2=Order("",5,datetime.datetime.today(),1000)
    os=OrderQueue()
    os.insert_order(o1)
    os.insert_order(o2)
    assert os.total_tax==o1.calc_tax()+o2.calc_tax()
    assert os.total_commission==o1.calc_commission()+o2.calc_commission()

def test_orderqueue_todf():
    o1=Order("123",10,datetime.datetime.today(),1000)
    o2=Order("456",5,datetime.datetime.today(),800)
    os=OrderQueue()
    os.insert_order(o1)
    os.insert_order(o2)
    print(os.to_df())