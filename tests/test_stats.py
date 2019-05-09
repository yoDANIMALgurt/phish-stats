"""Test for generating phish-stats"""
import os
import unittest

from phish_stats import *
from phish_stats.utils import *

API_KEY = os.environ['PHISHNET_API_KEY']


class TestShow(unittest.TestCase):
    """Test class for phish show."""

    @classmethod
    def setUpClass(cls):
        """Setup function."""
        cls.show = Show('2018-10-21', API_KEY)

    def test_api_response_data(self):
        """Test expected keys are returned from api call."""

        self.assertEqual(
            set(self.show.data['response']['data'][0].keys()),
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

    def test_setlist(self):
        """Test get setlist of specific date."""
        self.assertEqual(len(self.show.setlist), 19)

    def test_song_counts(self):
        """Test songs counts match expected."""
        self.assertEqual(self.show.song_counts, {
                         'total': 19, 'set1': 9, 'set2': 8, 'set3': 0, 'encore': 1, 'encore2': 1})

    def test_show_rating(self):
        """Test get show rating."""
        self.assertTrue(isinstance(self.show.rating, float))

    def test_relative_date(self):
        """Test get relative date."""
        self.assertTrue(isinstance(self.show.relative_date, str))
        self.assertTrue(self.show.relative_date.endswith('ago'))

    def test_location(self):
        """Can get location of show."""
        self.assertEqual(self.show.location['country'], 'USA')
        self.assertEqual(self.show.location['state'], 'VA')
        self.assertEqual(self.show.location['city'], 'Hampton')


class TestShowQueries(unittest.TestCase):
    """Test class for phish stats."""

    def test_generate_query_string(self):
        """Can generate query string."""

        kwargs = {
            'year': '2009',
            'month': '06'
        }
        query_string = generate_query_string(**kwargs)
        self.assertIn(query_string, ['year=2009&month=06',
                                     'month=06&year=2009'])

    def test_query_shows(self):
        """Test query shows."""

        parameters = {'year': '2013',
                      'month': '12',
                      'day': '31'}
        response = query_shows(API_KEY, **parameters)
        self.assertEqual(response.status_code, 200)

    def test_parse_show_dates(self):
        """Can return list of show dates."""

        parameters = {'year': '2010'}
        response = query_shows(API_KEY, **parameters)
        show_dates = parse_show_dates(response, [1])
        self.assertEqual(len(show_dates), 50)


if __name__ == '__main__':
    unittest.main()
