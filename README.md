# CurrencyRates
![Python application](https://github.com/TalShafir/CurrencyRates/workflows/Python%20application/badge.svg)

A Simple tool to get currency rates history using [ECB SDMX 2.1 RESTful web service](https://sdw-wsrest.ecb.europa.eu/help/)

Help message:
```
CurrencyRates.py -h
usage: CurrencyRates.py [-h] -f FROM_CURRENCY_LIST [FROM_CURRENCY_LIST ...] -t TO_CURRENCY_LIST [TO_CURRENCY_LIST ...] [-s FROM_DATE] [-d TO_DATE] [-o OUTPUT_FILE]

Simple tool to get currency rates history

optional arguments:
  -h, --help            show this help message and exit
  -f FROM_CURRENCY_LIST [FROM_CURRENCY_LIST ...], --from-currency-list FROM_CURRENCY_LIST [FROM_CURRENCY_LIST ...]
                        Currencies to find the rate history from
  -t TO_CURRENCY_LIST [TO_CURRENCY_LIST ...], --to-currency-list TO_CURRENCY_LIST [TO_CURRENCY_LIST ...]
                        Currencies to find the rate history to
  -s FROM_DATE, --from-date FROM_DATE
                        Starting date in the format of yyyy-mm-dd
  -d TO_DATE, --to-date TO_DATE
                        Ending date in the format of yyyy-mm-dd
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path for json output file

```

Simple Usage Example:

`python CurrencyRates.py --from-currency-list JPY USD --to-currency-list EUR USD --from-date=2020-05-01 --to-date=2020-05-01 -o ./currency.json`
