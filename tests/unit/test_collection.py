"""Test for generating phish-stats"""
import os
import unittest

from phish_stats import Collection

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
        cls.collection = Collection()
        cls.collection.add_shows(API_KEY, **kwargs)
        cls.collection.set_show_attributes(API_KEY)

    def test_number_of_shows(self):
        """Test accurate number of shows"""
        self.assertEqual(len(self.collection.shows), 4)

    def test_avg_rating(self):
        """Test average rating by month."""
        avg_rating = self.collection.calculate_avg_rating()
        self.assertTrue(isinstance(avg_rating, float))


class TestAllTime(unittest.TestCase):
    """Test case for all time show collection."""

    @classmethod
    def setUpClass(cls):
        """Setup function."""
        cls.collection = Collection()
        cls.collection.add_shows(API_KEY)

    def test_shows_per_year(self):
        """Test calculate shows per year."""
        shows_per_year = self.collection.calculate_shows_per_year()

        self.assertEqual(shows_per_year[0:33], [
            (1983, 3),
            (1984, 3),
            (1985, 30),
            (1986, 22),
            (1987, 47),
            (1988, 96),
            (1989, 126),
            (1990, 150),
            (1991, 133),
            (1992, 124),
            (1993, 114),
            (1994, 128),
            (1995, 83),
            (1996, 74),
            (1997, 84),
            (1998, 75),
            (1999, 69),
            (2000, 58),
            (2001, 1),
            (2002, 3),
            (2003, 47),
            (2004, 21),
            (2008, 1),
            (2009, 52),
            (2010, 50),
            (2011, 41),
            (2012, 37),
            (2013, 42),
            (2014, 42),
            (2015, 31),
            (2016, 48),
            (2017, 29),
            (2018, 42)
        ])


if __name__ == '__main__':
    unittest.main()
