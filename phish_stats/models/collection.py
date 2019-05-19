"""Collection model representing a collection of shows"""
from collections import Counter
import datetime

import numpy as np
# import requests

from phish_stats import utils
from phish_stats.models import Show
from phish_stats import phishnet_api as api


class Collection():
    """Show collection class"""

    def __init__(self, dates=[], shows=[]):
        self.dates = dates
        self.shows = shows

    def set_show_attributes(self, api_key):
        """Calls get_set_phishnet_data() for each show in the collection."""
        for show in self.shows:
            show.get_set_phishnet_data(api_key)

    def add_shows(self, api_key, **kwargs):
        """Adds shows to collection."""
        if kwargs:
            self.dates = api.query_shows_with_params(api_key, **kwargs)
        else:
            self.dates = api.query_all_show_dates(api_key)

        for date in self.dates:
            self.shows.append(Show(date))

    def calculate_shows_per_year(self):
        """Returns year to show count dictionary."""
        shows_per_year = Counter()
        for year in [show.year for show in self.shows]:
            shows_per_year[year] += 1

        return sorted(shows_per_year.items())

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)
