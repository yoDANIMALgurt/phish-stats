"""Test for generating phish-stats"""
import os
import unittest

from phish_stats import Collection
from phish_stats.utils import *

API_KEY = os.environ['PHISHNET_API_KEY']


class TestCollection(unittest.TestCase):
    """Test class for show collection."""

    @classmethod
    def setUpClass(cls):
        """Setup function."""
        kwargs = {
            'year': 1998,
            'month': 4
        }
        cls.collection = Collection(API_KEY, **kwargs)

    def test_number_of_shows(self):
        """Test accurate number of shows"""
        self.assertEqual(len(self.collection.shows), 4)

    def test_avg_rating(self):
        """Test average rating by month."""
        avg_rating = self.collection.calculate_avg_rating()
        self.assertTrue(isinstance(avg_rating, float))


class TestAllTime(unittest.TestCase):
    """Test class for all time shows."""

    @unittest.skip('all time test takes too much time to run')
    def test_get_all_shows(self):
        """Test create all time collection"""
        collection = Collection(API_KEY)


if __name__ == '__main__':
    unittest.main()
