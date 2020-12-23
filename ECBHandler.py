from typing import List, Generator

import requests
import xmltodict


def _get_serieses(parsed_response: dict) -> list:
    """
    Get ECB response parsed to dict and return the relevant serieses of currencies
    :param parsed_response: parsed response from ECB
    :return: list of series parsed as dicts
    """
    serieses = parsed_response["message:GenericData"]["message:DataSet"]["generic:Series"]
    if type(serieses) != list:
        serieses = [serieses]
    return serieses


def _extract_series_currencies(series: dict) -> tuple:
    """
    Extract the currencies from a series
    :param series: series parsed as dict
    :return: tuple with (currency1,currency2)
    """
    return tuple(curr['@value'] for curr in series["generic:SeriesKey"]["generic:Value"][1:3])


def _series_date_value_iter(data_points: List[dict]) -> Generator:
    """
    Generator to traverse (date,value) tuples
    :param data_points: list of data_points parsed as dicts
    :return: generator of (date,value) tuples
    """
    for data_point in data_points:
        yield data_point["generic:ObsDimension"]["@value"], data_point["generic:ObsValue"]["@value"]


def _extract_data_points_from_series(series: dict) -> List[dict]:
    """
    Extract data points list from series parsed as dict
    :param series: series parsed as dict
    :return: list of data points
    """
    data_points = series["generic:Obs"]
    if type(data_points) != list:
        data_points = [data_points]
    return data_points


def _extract_series_date_value_mapping(series):
    """
    Generate mapping between date and its appropriate value
    :param series: series parsed as dict
    :return: dict with dates as keys and currency exchange rate as values
    """
    return {date: value for date, value in _series_date_value_iter(_extract_data_points_from_series(series))}


def get_translation_table_to_eur(currencies: str, from_date: str, to_date: str) -> dict:
    """
    Get the currency exchange rate to euro for all given currencies using ECB api
    :param currencies: string of currencies in uppercase separated by + character
    :param from_date: start date in the format of yyyy-mm-dd
    :param to_date: end date in the format of yyyy-mm-dd
    :return: dict in the format {(currency1,currency2):{date:exchange rate}}
    """
    # TODO: validate dates instead of only is empty
    params = {
        **({"startPeriod": from_date} if from_date else {}),
        **({"endPeriod": to_date} if to_date else {}),

    }
    response = requests.get(f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currencies}.EUR.SP00.A', params)
    # in case the API returned error
    if response.status_code != 200:
        raise Exception(f'Error from the API: {response.text}')
    elif response.text == '':
        raise Exception('The API returned empty result')

    parsed = xmltodict.parse(response.text)
    serieses = _get_serieses(parsed)
    translation_table = {
        # get source and destination currencies and use them as keys
        _extract_series_currencies(series):
        # for each currency tuple create a dictionary that maps the date to its value
            _extract_series_date_value_mapping(series)
        for series in serieses
    }
    # TODO: handle NaNs and missing dates
    return translation_table
