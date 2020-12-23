import unittest
import CurrencyRates
import ECBHandler


class CurrencyRatesTestCase(unittest.TestCase):
    def test_convert_to_self(self):
        _TEST_DATE = '2020-05-05'
        _TEST_CURRENCY = 'USD'
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 [_TEST_CURRENCY],
                                                                 [_TEST_CURRENCY],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table[f'({_TEST_CURRENCY},{_TEST_CURRENCY})'][_TEST_DATE], '1.0')

    def test_convert_to_euro(self):
        _TEST_DATE = '2020-05-05'
        _TEST_FROM_CURRENCY = 'USD'
        _TEST_TO_CURRENCY = 'EUR'
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 [_TEST_FROM_CURRENCY],
                                                                 [_TEST_TO_CURRENCY],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table[f'({_TEST_FROM_CURRENCY},{_TEST_TO_CURRENCY})'][_TEST_DATE], '1.0843')

    def test_convert_to_not_euro(self):
        _TEST_DATE = '2020-05-05'
        _TEST_FROM_CURRENCY = 'USD'
        _TEST_TO_CURRENCY = 'JPY'
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 [_TEST_FROM_CURRENCY],
                                                                 [_TEST_TO_CURRENCY],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table[f'({_TEST_FROM_CURRENCY},{_TEST_TO_CURRENCY})'][_TEST_DATE],
                         '0.009370840895341804')


if __name__ == '__main__':
    unittest.main()
