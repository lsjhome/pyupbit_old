import unittest
import logging

from pyupbit import PyUpbit

class PyUpBitTest(unittest.TestCase):
    
    def test_get_market_all(self):
        pyupbit = PyUpbit()
        ret = pyupbit.get_market_all()
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
    
    def test_get_minutes_candles(self):
        pyupbit = PyUpbit()
        ret = pyupbit.get_minutes_candles(60, 'KRW-BTC')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)

    def test_get_days_candles(self):
        pyupbit = PyUpbit()
        ret = pyupbit.get_days_candles('KRW-ADA')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
