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
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 ['USD'],
                                                                 ['EUR'],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table['(USD,EUR)'][_TEST_DATE], '1.0843')

    def test_convert_to_not_euro(self):
        _TEST_DATE = '2020-05-05'
        rates_table = CurrencyRates.get_currency_conversion_rate(ECBHandler,
                                                                 ['USD'],
                                                                 ['JPY'],
                                                                 _TEST_DATE,
                                                                 _TEST_DATE)
        self.assertEqual(rates_table['(USD,JPY)'][_TEST_DATE], '0.009370840895341804')


if __name__ == '__main__':
    unittest.main()
