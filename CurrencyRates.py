import argparse
import itertools
import sys
import os
import json
from typing import List

import ECBHandler


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple tool to get currency rates history")
    parser.add_argument('-f', '--from-currency-list', nargs='+',
                        help='Currencies to find the rate history from', required=True)
    parser.add_argument('-t', '--to-currency-list', nargs='+',
                        help='Currencies to find the rate history to', required=True)
    parser.add_argument('-s', '--from-date', type=str, help='Starting date in the format of yyyy-mm-dd')
    parser.add_argument('-d', '--to-date', type=str, help='Ending date in the format of yyyy-mm-dd')
    parser.add_argument('-o', '--output-file', type=str, help='Path for json output file',
                        default=os.path.join(os.path.abspath(os.path.expanduser('~')), 'currencies.json'))

    return parser.parse_args(args)


def get_currency_conversion_rate(api_handler, from_currency_list: list, to_currency_list: list, from_date: str,
                                 to_date: str) -> dict:
    """
    Generate mapping from all currencies in from_currency_list to all currencies in to_currency_list
    :param api_handler: object with a function get_translation_table_to_eur(currencies, from_date, to_date)
    :param from_currency_list: list of all source currencies
    :param to_currency_list: list of all target currencies
    :param from_date: the first date to search in the format of yyyy-mm-dd
    :param to_date: the last date to search in the format of yyyy-mm-dd
    :return: dict {'(from_currency,to_currency)':{date:exchange_rate}}
    """
    # in order to get get all relevant currencies to EUR add them with + as a separator

    currencies = '+'.join(currency.upper() for currency in set(from_currency_list) | set(to_currency_list))
    translation_table_to_eur = api_handler.get_translation_table_to_eur(currencies, from_date, to_date)

    translation_table = {}
    for src, dest in itertools.product(from_currency_list, to_currency_list):
        key = f'({src},{dest})'
        # if dest is in EUR we already have it
        if dest == 'EUR':
            translation_table[key] = translation_table_to_eur[src, dest]
        # if src is in EUR then we have the 1/ value of it
        elif src == 'EUR':
            translation_table[key] = {
                date: str(1 / float(translation_table_to_eur[dest, 'EUR'][date]))
                for date in translation_table_to_eur[dest, 'EUR']}
        else:
            # use transitive to calculate (i.e USD->JPY by calculating USD->EUR->JPY)
            translation_table[key] = {
                date: str(float(translation_table_to_eur[src, 'EUR'][date]) /
                          float(translation_table_to_eur[dest, 'EUR'][date]))
                for date in translation_table_to_eur[src, 'EUR']}

    return translation_table


def main(args: List[str]):
    args = parse_args(args)
    with open(args.output_file, 'w') as output_file:
        json.dump(get_currency_conversion_rate(api_handler=ECBHandler,
                                               from_currency_list=args.from_currency_list,
                                               to_currency_list=args.to_currency_list,
                                               from_date=args.from_date,
                                               to_date=args.to_date), output_file)
        print(f'Output saved at {args.output_file}')


if __name__ == '__main__':
    main(sys.argv[1:])
