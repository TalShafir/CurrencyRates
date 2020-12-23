import unittest

import ECBHandler


class APITestCase(unittest.TestCase):
    def test_api_single_currency_single_date(self):
        _TEST_CURRENCY = 'USD'
        _TEST_DATE = '2020-05-05'
        translation_table = ECBHandler.get_translation_table_to_eur(_TEST_CURRENCY, _TEST_DATE, _TEST_DATE)
        self.assertEqual(translation_table[_TEST_CURRENCY, 'EUR'][_TEST_DATE], '1.0843')

    def test_api_single_currency_multiple_dates(self):
        _TEST_CURRENCY = 'USD'
        _TEST_START_DATE = '2020-05-05'
        _TEST_END_DATE = '2020-05-06'
        translation_table = ECBHandler.get_translation_table_to_eur(_TEST_CURRENCY, _TEST_START_DATE, _TEST_END_DATE)
        self.assertEqual(translation_table[_TEST_CURRENCY, 'EUR'][_TEST_START_DATE], '1.0843')
        self.assertEqual(translation_table[_TEST_CURRENCY, 'EUR'][_TEST_END_DATE], '1.0807')

    def test_api_multiple_currencies_single_date(self):
        _TEST_DATE = '2020-05-05'
        _TEST_CURRENCIES = ['USD', 'JPY']
        translation_table = ECBHandler.get_translation_table_to_eur('+'.join(_TEST_CURRENCIES), _TEST_DATE, _TEST_DATE)
        self.assertEqual(translation_table[_TEST_CURRENCIES[0], 'EUR'][_TEST_DATE], '1.0843')
        self.assertEqual(translation_table[_TEST_CURRENCIES[1], 'EUR'][_TEST_DATE], '115.71')

    def test_api_multiple_currencies_multiple_dates(self):
        _TEST_START_DATE = '2020-05-05'
        _TEST_END_DATE = '2020-05-06'
        _TEST_CURRENCIES = ['USD', 'JPY']
        translation_table = ECBHandler.get_translation_table_to_eur('USD+JPY', _TEST_START_DATE, _TEST_END_DATE)
        self.assertEqual(translation_table[_TEST_CURRENCIES[0], 'EUR'][_TEST_START_DATE], '1.0843')
        self.assertEqual(translation_table[_TEST_CURRENCIES[0], 'EUR'][_TEST_END_DATE], '1.0807')
        self.assertEqual(translation_table[_TEST_CURRENCIES[1], 'EUR'][_TEST_START_DATE], '115.71')
        self.assertEqual(translation_table[_TEST_CURRENCIES[1], 'EUR'][_TEST_END_DATE], '114.65')


if __name__ == '__main__':
    unittest.main()
