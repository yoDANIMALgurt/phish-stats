"""Collection model representing a collection of shows"""
import datetime

import numpy as np
# import requests

from phish_stats import utils
from phish_stats.models import Show
from phish_stats import phishnet_api as api


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
            self.dates = api.query_shows_with_params(api_key, **kwargs)
        else:
            self.dates = api.query_all_show_dates(api_key)

    def create_show_objects(self, api_key):
        """Creates a show object for each show."""
        for date in self.dates:
            self.shows.append(Show(date, api_key))

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)
