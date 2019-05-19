"""Module for testing phish.net api calls."""
import os
import unittest

from phish_stats import phishnet_api as api

API_KEY = os.environ['PHISHNET_API_KEY']


class TestPhishNetApi(unittest.TestCase):
    """Test class phish.net api calls"""

    def test_get_show_data(self):
        """Test get single show data"""
        date = '1995-12-31'
        data = api.get_show_data(date, API_KEY)

        self.assertEqual(
            set(data['response']['data'][0].keys()),
            {
                'relative_date',
                'showid',
                'url',
                'venueid',
                'long_date',
                'venue',
                'setlistdata',
                'showdate',
                'artistid',
                'rating',
                'setlistnotes',
                'artist',
                'short_date',
                'location',
                'gapchart'
            }
        )

    def test_query_show_dates_with_params(self):
        """Test query show dates with params."""
        kwargs = {
            'year': 1998,
            'month': 4
        }

        dates = api.query_shows_with_params(API_KEY, **kwargs)
        self.assertEqual(
            dates, ['1998-04-02', '1998-04-03', '1998-04-04', '1998-04-05'])

    def test_query_all_shows(self):
        """Test query show dates with params."""
        dates = api.query_all_show_dates(API_KEY)
        self.assertGreater(len(dates), 1900)
