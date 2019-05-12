"""Collection model representing a collection of shows"""
import datetime

import numpy as np
import requests

from phish_stats import utils
from phish_stats.models import Show


class Collection():
    """Show collection class"""

    def __init__(self, api_key, **kwargs):
        self.dates = []
        self.shows = []
        self.get_show_dates(api_key, **kwargs)
        self.create_show_objects(api_key)

    def get_show_dates(self, api_key, **kwargs):
        """Gets show dates based on params or fetch all shows."""
        if kwargs:
            self.query_shows_with_params(api_key, **kwargs)
        else:
            self.query_all_show_dates(api_key)

    def query_shows_with_params(self, api_key, **kwargs):
        """Query shows"""
        query_string = utils.generate_query_string(kwargs)
        url = f"https://api.phish.net/v3/shows/query?apikey={api_key}&{query_string}&order=ASC"
        response = requests.get(url=url, timeout=15)

        self.dates = [show['showdate'] for show in response.json()
                      ['response']['data'] if show['artistid'] == 1]

    def query_all_show_dates(self, api_key):
        """Query for all show dates."""
        min_year = 1983
        max_year = datetime.datetime.now().year
        for year in range(min_year, max_year+1):
            query_string = utils.generate_query_string({'year': year})
            url = f"https://api.phish.net/v3/shows/query?apikey={api_key}&{query_string}&order=ASC"
            response = requests.get(url=url, timeout=15)
            assert response.status_code == 200
            self.dates += [show['showdate'] for show in response.json()
                           ['response']['data'] if show['artistid'] == 1]

    def create_show_objects(self, api_key):
        """Creates a show object for each show."""
        for date in self.dates:
            self.shows.append(Show(date, api_key))

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)
