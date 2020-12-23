import unittest
import CurrencyRates
import ECBHandler


class MyTestCase(unittest.TestCase):
    def test_convert_to_self(self):
        _TEST_DATE = '2020-05-05'
        _TEST_CURRENCY = 'USD'
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 [_TEST_CURRENCY],
                                                                 [_TEST_CURRENCY],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table[f'({_TEST_CURRENCY},{_TEST_CURRENCY})'][_TEST_DATE], '1.0')


if __name__ == '__main__':
    unittest.main()
