"""Test for generating phish-stats"""
import os
import unittest

from phish_stats import utils

API_KEY = os.environ['PHISHNET_API_KEY']


class TestUtils(unittest.TestCase):
    """Test class for phish stats."""

    def test_generate_query_string(self):
        """Can generate query string."""

        query_params = {
            'year': '2009',
            'month': '06'
        }
        query_string = utils.generate_query_string(query_params)
        self.assertIn(query_string, ['year=2009&month=06',
                                     'month=06&year=2009'])


if __name__ == '__main__':
    unittest.main()
