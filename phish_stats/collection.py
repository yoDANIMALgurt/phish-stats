"""Collection model representing a collection of shows"""
from collections import Counter
import datetime

from bokeh.plotting import figure, output_file, show
import numpy as np
import pandas as pd

from phish_stats import utils
from phish_stats import Show
from phish_stats import phishnet_api as api


class Collection():
    """Show collection class"""

    def __init__(self, dates=[], shows=[]):
        self.dates = dates
        self.shows = shows

    def set_show_attributes(self, api_key):
        """Calls set_attributes() for each show in the collection."""
        for show in self.shows:
            show.fetch_phishnet_data(api_key)
            show.set_attributes()

    def add_shows(self, api_key, **kwargs):
        """Adds shows to collection."""
        if kwargs:
            self.dates = api.query_shows_with_params(api_key, **kwargs)
        else:
            self.dates = api.query_all_show_dates(api_key)

        for date in self.dates:
            self.shows.append(Show(date))

    def create_shows(self):
        """Create show instances."""
        for date in self.dates:
            self.shows.append(Show(date))

    def create_collection_df(self):
        """Create pandas df from collection of shows."""
        data = [
            {
                'date': show.date,
                'rating': show.rating,
                'total_song_count': show.total_song_count
            } for show in self.shows]

        return pd.DataFrame.from_dict(data)

    def calculate_shows_by_year(self):
        """Returns year to show count dictionary."""
        shows_by_year = Counter()
        min_year = 1983
        max_year = datetime.datetime.now().year

        # Set default count to 0 for all years since 1993
        for year in range(min_year, max_year + 1):
            shows_by_year[year] = 0

        # Increment year count for each show in collection
        for year in [show.year for show in self.shows]:
            shows_by_year[year] += 1

        return sorted(shows_by_year.items())

    def visualize_shows_by_year(self, filepath, show_in_browser=True):
        """Visualizes shows per year."""
        shows_by_year = self.calculate_shows_by_year()
        # prepare some data
        x = [year for year, count in shows_by_year]
        y = [count for year, count in shows_by_year]

        # output to static HTML file
        output_file(filepath)

        # create a new plot with a title and axis labels
        p = figure(title="Phish Shows By Year",
                   x_axis_label='Year', y_axis_label='Number of Shows')

        # add a line renderer with legend and line thickness
        p.line(x, y, legend="Show By Year", line_width=2)

        # show the results
        if show_in_browser:
            show(p)

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)

    def write_to_csv(self, filepath):
        """Writes collection data to csv file."""
        self.create_collection_df().to_csv(filepath)
