import requests
import xmltodict


def get_translation_table_to_eur(currencies: str, from_date: str, to_date: str):
    # TODO: validate dates instead of only is empty
    params = {
        **({"startPeriod": from_date} if from_date else {}),
        **({"endPeriod": to_date} if to_date else {}),

    }
    response = requests.get(f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currencies}.EUR.SP00.A', params)
    # in case the API returned error
    if response.status_code != 200:
        raise Exception(f'Error from the API: {response.text}')

    serieses = xmltodict.parse(response.text)["message:GenericData"]["message:DataSet"]["generic:Series"]
    translation_table = {
        # get source and destination currencies and use them as keys
        tuple(curr['@value'] for curr in series["generic:SeriesKey"]["generic:Value"][1:3]):
        # for each currency tuple create a dictionary that maps the date to its value
            {data_point["generic:ObsDimension"]["@value"]: data_point["generic:ObsValue"]["@value"] for data_point in
             series["generic:Obs"]}
        for series in serieses
    }
    # TODO: handle NaNs and missing values
    return translation_table


print(get_translation_table_to_eur('JPY+USD', '2020-05-01', '2020-05-31'))
