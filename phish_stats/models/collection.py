"""Collection model representing a collection of shows"""
import numpy as np
import requests

from phish_stats import utils
from phish_stats.models import Show


class Collection():
    """Show collection class"""

    def __init__(self, api_key, **kwargs):
        self.query_data = {}
        self.shows = []
        self.query_shows(api_key, **kwargs)
        self.create_show_objects(api_key)

    def query_shows(self, api_key, **kwargs):
        """Query shows"""
        query_string = utils.generate_query_string(kwargs)
        url = f"https://api.phish.net/v3/shows/query?apikey={api_key}&{query_string}&order=ASC"
        response = requests.get(url=url, timeout=15)
        assert response.status_code == 200
        self.query_data = response.json()['response']['data']

    def create_show_objects(self, api_key):
        """Creates a show object for each show."""
        for show in self.query_data:
            if show["artistid"] == 1:
                self.shows.append(Show(show["showdate"], api_key))

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)
