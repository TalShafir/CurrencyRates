import itertools

import ECBHandler


def get_currency_conversion_rate(from_currency_list: list, to_currency_list: list, from_date: str, to_date: str):
    # in order to get get all relevant currencies to EUR add them with + as a separator
    currencies = '+'.join(set(from_currency_list) | set(to_currency_list))
    translation_table_to_eur = ECBHandler.get_translation_table_to_eur(currencies, from_date, to_date)

    translation_table = {}
    for src, dest in itertools.product(from_currency_list, to_currency_list):
        # if dest is in EUR we already have it
        if dest == 'EUR':
            translation_table[src, dest] = translation_table_to_eur[src, dest]
        # if src is in EUR then we have the 1/ value of it
        elif src == 'EUR':
            translation_table[src, dest] = {date: str(1 / float(translation_table_to_eur[dest, 'EUR'][date]))
                                            for date in translation_table_to_eur[dest, 'EUR']}
        else:
            # use transitive to calculate (i.e USD->JPY by calculating USD->EUR->JPY)
            translation_table[src, dest] = {
                date: str(float(translation_table_to_eur[src, 'EUR'][date]) /
                          float(translation_table_to_eur[dest, 'EUR'][date]))
                for date in translation_table_to_eur[src, 'EUR']}

    return translation_table


print(get_currency_conversion_rate(['JPY', 'USD'], ['EUR', 'USD'], '2020-05-01', '2020-05-31'))
