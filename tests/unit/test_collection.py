"""Test for generating phish-stats"""
import json
import os
import unittest

import pandas as pd
from phish_stats import Collection

API_KEY = os.environ['PHISHNET_API_KEY']


class TestCollection(unittest.TestCase):
    """Test class for show collection."""

    @classmethod
    def setUpClass(cls):
        """Setup function."""

        with open('./tests/data/input/island-tour-raw.json', 'r') as json_file:
            island_tour_raw_data = json.load(json_file)

        dates = [date for date in island_tour_raw_data.keys()]
        cls.collection = Collection(dates=dates)
        cls.collection.create_shows()

        for show in cls.collection.shows:
            show.data = island_tour_raw_data[show.date]

        cls.collection.set_show_attributes(API_KEY)

    def test_number_of_shows(self):
        """Test accurate number of shows"""
        self.assertEqual(len(self.collection.shows), 4)

    def test_avg_rating(self):
        """Test average rating by month."""
        avg_rating = self.collection.calculate_avg_rating()
        self.assertTrue(isinstance(avg_rating, float))

    def test_create_df(self):
        """Test create pandas dataframe."""
        collection_df = self.collection.create_collection_df()
        self.assertIsInstance(collection_df, pd.core.frame.DataFrame)


class TestAllTime(unittest.TestCase):
    """Test case for all time show collection."""

    @classmethod
    def setUpClass(cls):
        """Setup function."""

        with open('./tests/data/input/all-shows-raw.json', 'r') as json_file:
            all_shows_raw_data = json.load(json_file)

        dates = [date for date in all_shows_raw_data.keys()]
        cls.collection = Collection(dates=dates)
        cls.collection.create_shows()

        for show in cls.collection.shows:
            show.data = all_shows_raw_data[show.date]

        cls.collection.set_show_attributes(API_KEY)

    def test_shows_by_year(self):
        """Test calculate shows per year."""
        shows_by_year = self.collection.calculate_shows_by_year()

        self.assertEqual(shows_by_year[0:36], [
            (1983, 3),
            (1984, 3),
            (1985, 26),
            (1986, 22),
            (1987, 47),
            (1988, 96),
            (1989, 126),
            (1990, 150),
            (1991, 133),
            (1992, 124),
            (1993, 113),
            (1994, 124),
            (1995, 83),
            (1996, 74),
            (1997, 83),
            (1998, 75),
            (1999, 68),
            (2000, 56),
            (2001, 1),
            (2002, 3),
            (2003, 47),
            (2004, 21),
            (2005, 0),
            (2006, 0),
            (2007, 0),
            (2008, 1),
            (2009, 52),
            (2010, 50),
            (2011, 41),
            (2012, 37),
            (2013, 42),
            (2014, 41),
            (2015, 31),
            (2016, 48),
            (2017, 29),
            (2018, 42)
        ])

    def test_visualize_shows_by_year(self):
        """Test vizualize shows per year."""
        outfile = "tests/data/output/shows_by_year.html"
        self.collection.visualize_shows_by_year(outfile)

    def test_write_to_csv(self):
        """Test write collection data to csv file."""
        filepath = 'tests/data/output/alltime.csv'
        self.collection.write_to_csv(filepath)

    def test_create_df_from_csv(self):
        """Test read collection data from .csv file."""
        columns = [
            'date',
            'year',
            'month',
            'day',
            'relative_date',
            'total_song_count',
            'set1_song_count',
            'set2_song_count',
            'set3_song_count',
            'encore_song_count',
            'encore2_song_count',
            'country',
            'state',
            'city',
            'rating',
            'venue',
            'era'
        ]
        df_collection = self.collection.create_df_from_csv(
            'tests/data/input/alltime.csv', columns)
        self.assertIsInstance(df_collection, pd.DataFrame)

    @unittest.skip('TODO -- update to assert Error')
    def test_create_df_from_invalid_csv(self):
        """Test read collection data from .csv file."""
        # df_collection = self.collection.create_df_from_csv('tests/data/input/invalid.csv')
        with self.assertError:
            df_collection = self.collection.create_df_from_csv('tests/data/input/invalid.csv')

    def test_visualize_shows_by_state(self):
        """Test visualize shows by state."""
        outfile = "tests/data/output/shows_by_state.html"
        self.collection.visualize_shows_by_state(outfile)
             

if __name__ == '__main__':
    unittest.main()
