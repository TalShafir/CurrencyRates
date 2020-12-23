import requests
import xmltodict
import itertools


class ECBHandler:
    def _get_serieses(self, parsed_response: dict) -> list:
        return parsed_response["message:GenericData"]["message:DataSet"]["generic:Series"]

    def _extract_series_currencies(self, series: dict) -> tuple:
        return tuple(curr['@value'] for curr in series["generic:SeriesKey"]["generic:Value"][1:3])

    def _series_date_value_iter(self, data_points):
        for data_point in data_points:
            yield data_point["generic:ObsDimension"]["@value"], data_point["generic:ObsValue"]["@value"]

    def _extract_series_date_value_mapping(self, series):
        return {date: value for date, value in self._series_date_value_iter(series["generic:Obs"])}

    def get_translation_table_to_eur(self, currencies: str, from_date: str, to_date: str):
        # TODO: validate dates instead of only is empty
        params = {
            **({"startPeriod": from_date} if from_date else {}),
            **({"endPeriod": to_date} if to_date else {}),

        }
        response = requests.get(f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currencies}.EUR.SP00.A', params)
        # in case the API returned error
        if response.status_code != 200:
            raise Exception(f'Error from the API: {response.text}')

        parsed = xmltodict.parse(response.text)
        serieses = self._get_serieses(parsed)
        translation_table = {
            # get source and destination currencies and use them as keys
            self._extract_series_currencies(series):
            # for each currency tuple create a dictionary that maps the date to its value
                self._extract_series_date_value_mapping(series)
            for series in serieses
        }
        # TODO: handle NaNs and missing dates
        return translation_table


def get_currency_conversion_rate(from_currency_list: list, to_currency_list: list, from_date: str, to_date: str):
    # in order to get get all relevant currencies to EUR add them with + as a separator
    currencies = '+'.join(set(from_currency_list) | set(to_currency_list))
    translation_table_to_eur = ECBHandler().get_translation_table_to_eur(currencies, from_date, to_date)

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
