import unittest

import ECBHandler


class APITestCase(unittest.TestCase):
    def test_api_single_currency_single_date(self):
        translation_table = ECBHandler.get_translation_table_to_eur('USD', '2020-05-05', '2020-05-05')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-05'], '1.0843')

    def test_api_single_currency_multiple_dates(self):
        translation_table = ECBHandler.get_translation_table_to_eur('USD', '2020-05-05', '2020-05-06')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-05'], '1.0843')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-06'], '1.0807')

    def test_api_multiple_currencies_single_date(self):
        translation_table = ECBHandler.get_translation_table_to_eur('USD+JPY', '2020-05-05', '2020-05-05')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-05'], '1.0843')
        self.assertEqual(translation_table['JPY', 'EUR']['2020-05-05'], '115.71')

    def test_api_multiple_currencies_multiple_dates(self):
        translation_table = ECBHandler.get_translation_table_to_eur('USD+JPY', '2020-05-05', '2020-05-06')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-05'], '1.0843')
        self.assertEqual(translation_table['USD', 'EUR']['2020-05-06'], '1.0807')
        self.assertEqual(translation_table['JPY', 'EUR']['2020-05-05'], '115.71')
        self.assertEqual(translation_table['JPY', 'EUR']['2020-05-06'], '114.65')


if __name__ == '__main__':
    unittest.main()
