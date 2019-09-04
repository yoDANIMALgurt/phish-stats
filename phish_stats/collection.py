"""Collection model representing a collection of shows"""
from collections import Counter
import datetime

from bokeh.core.properties import value
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
                'year': show.year,
                'month': show.month,
                'day': show.day,
                'relative_date': show.relative_date,
                'total_song_count': show.total_song_count,
                'set1_song_count': show.set1_song_count,
                'set2_song_count': show.set2_song_count,
                'set3_song_count': show.set3_song_count,
                'encore_song_count': show.encore_song_count,
                'encore2_song_count': show.encore2_song_count,
                'country': show.country,
                'state': show.state,
                'city': show.city,
                'rating': show.rating,
                'venue': show.venue,
                'era': show.era             
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

    def visualize_shows_by_year(self, outfile):
        """Visualizes shows per year."""
        shows_by_year = self.calculate_shows_by_year()
        # prepare some data
        x = [year for year, count in shows_by_year]
        y = [count for year, count in shows_by_year]

        # output to static HTML file
        output_file(outfile)

        # create a new plot with a title and axis labels
        p = figure(title="Phish Shows By Year",
                   x_axis_label='Year', y_axis_label='Number of Shows')

        # add a line renderer with legend and line thickness
        p.line(x, y, legend="Show By Year", line_width=2)

        show(p)

    def visualize_shows_by_state(self, outfile):
        """Visualizes shows by state."""
        df_collection = self.create_collection_df()
        country_mask = df_collection['country'] == 'USA'
        df_us_shows = df_collection[country_mask]
        group_by_state = df_us_shows.groupby(
            by=['state'],
            axis=0, 
            as_index=False
        ).count()[['state', 'city']].rename(columns={'city': 'count'})

        states = group_by_state['state'].unique().tolist()
        eras = ["1.0", "2.0", "3.0"]
        colors = ["#c9d9d3", "#718dbf", "#e84d60"]
        counts = group_by_state['count'].tolist()

        data = {'states' : states}
     
        for era in eras:
            data[era] = []
            for state in states:
                state_mask = df_us_shows['state'] == state
                era_mask = df_us_shows['era'] == era
                count = df_us_shows[
                    state_mask & 
                    era_mask
                ].shape[0]
                data[era].append(count)

        # sorting the state means sorting the range factors
        sorted_states = sorted(
            states,
            key=lambda x: counts[states.index(x)],
            reverse=True
        )

        # output to static HTML file
        output_file(outfile)

        # create a new plot with a title and axis labels
        p = figure(
            title="Phish Shows By State",
            x_axis_label='State',
            y_axis_label='Number of Shows',
            x_range=sorted_states,
            plot_width=2000,
            toolbar_location=None, tools="hover", tooltips="$name: @$name"
            )

        # add a line renderer with legend and line thickness
        p.vbar_stack(eras, x='states', source=data, color=colors, width=0.9, legend=[value(x) for x in eras])
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"

        show(p)
        

    def calculate_avg_rating(self):
        """Returns the average rating of the collection of shows"""
        ratings = np.array([show.rating for show in self.shows])
        return np.mean(ratings)

    def write_to_csv(self, filepath):
        """Writes collection data to csv file."""
        self.create_collection_df().to_csv(
            filepath,
            index=False
        )

    def create_df_from_csv(self, filepath, columns=[
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
    ]):
        """Create pandas df from csv file."""
        df_collection = pd.read_csv(filepath)
        if set(df_collection.columns) != set(columns):
            raise TypeError('Not a valid phish-stats collection csv')

        return df_collection       
