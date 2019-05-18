"""Module for making phish.net api requests."""
import datetime
import requests

from phish_stats import utils


def get_single_show_data(date, api_key):
    """Get stats of a show by date"""
    url = ("https://api.phish.net/v3/setlists/get?"
           f"apikey={api_key}&showdate={date}")

    print(f'getting setlist for {date}')
    response = requests.get(url=url, timeout=15)

    assert response.status_code == 200

    return response.json()


def query_shows_with_params(api_key, **kwargs):
    """Query shows"""
    query_string = utils.generate_query_string(kwargs)
    url = f"https://api.phish.net/v3/shows/query?apikey={api_key}&{query_string}&order=ASC"
    response = requests.get(url=url, timeout=15)

    return [show['showdate'] for show in response.json()
            ['response']['data'] if show['artistid'] == 1]


def query_all_show_dates(api_key):
    """Query for all show dates."""
    min_year = 1983
    max_year = datetime.datetime.now().year
    dates = []
    for year in range(min_year, max_year+1):
        query_string = utils.generate_query_string({'year': year})
        url = f"https://api.phish.net/v3/shows/query?apikey={api_key}&{query_string}&order=ASC"
        response = requests.get(url=url, timeout=15)
        assert response.status_code == 200
        dates += [show['showdate'] for show in response.json()
                  ['response']['data'] if show['artistid'] == 1]

    return dates
