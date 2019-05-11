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
        self.assertTrue(isinstance(self.show.date['relative'], str))
        self.assertTrue(self.show.date['relative'].endswith('ago'))

    def test_location(self):
        """Can get location of show."""
        self.assertEqual(self.show.location['country'], 'USA')
        self.assertEqual(self.show.location['state'], 'VA')
        self.assertEqual(self.show.location['city'], 'Hampton')


class TestCurveball(unittest.TestCase):
    """Test case for a cancelled show :("""

    @classmethod
    def setUpClass(cls):
        """Setup function."""
        cls.show = Show('2018-08-17', API_KEY)

    def test_api_response_data(self):
        """Test expected keys are returned from api call."""

    def test_setlist(self):
        """Test get setlist of specific date."""
        self.assertEqual(self.show.setlist, [])

    def test_song_counts(self):
        """Test songs counts match expected."""
        self.assertEqual(self.show.song_counts, {})

    def test_show_rating(self):
        """Test get show rating."""
        self.assertEqual(self.show.rating, None)

    def test_relative_date(self):
        """Test get relative date."""
        self.assertEqual(self.show.date['relative'], None)

    def test_location(self):
        """Can get location of show."""
        self.assertEqual(self.show.location, {})


if __name__ == '__main__':
    unittest.main()
