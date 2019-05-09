
"""Phish Stats"""
from multiprocessing import Pool

from bs4 import BeautifulSoup
import pandas as pd
import requests

from phish_stats import utils


class Show(object):
    """Show class"""

    def __init__(self, date, api_key):
        self.date = date
        self.data = {}
        self.setlist = []
        self.song_counts = {}
        self.location = {}
        self.rating = ''
        self.relative_date = ''
        self.venue = ''
        # Set all the show attributes
        self.get_single_show_data(api_key)
        self.set_attributes()

    def set_attributes(self):
        self.parse_setlist()
        self.set_total_song_count()
        self.set_set1_song_count()
        self.set_set2_song_count()
        self.set_set3_song_count()
        self.set_encore_song_count()
        self.set_encore2_song_count()
        self.set_show_rating()
        self.set_relative_date()
        self.set_venue()
        self.set_show_location()

    def get_single_show_data(self, api_key):
        """Get stats of a show by date"""
        url = (
            "https://api.phish.net/v3/setlists/get?"
            "apikey={api_key}&showdate={date}".format(
                api_key=api_key, date=self.date
            )
        )

        response = requests.get(url=url, timeout=15)

        assert response.status_code == 200

        self.data = response.json()

    def parse_setlist(self):
        setlist = []
        soup = BeautifulSoup(
            self.data["response"]["data"][0]['setlistdata'], features="html.parser")

        for p in soup.find_all("p"):

            setlist_tags = p.contents
            for i, tag in enumerate(setlist_tags):
                # handle Navigable Strings
                if str(type(tag)) == "<class 'bs4.element.NavigableString'>":
                    # string. Need to add special handling
                    continue

                if tag.name == "br":
                    continue

                # handle setlist notes
                elif tag.name == "sup":
                    element = {
                        "note_id": int(tag.contents[0][1:2]),
                        "element_type": "note",
                        "body": tag["title"],
                    }

                    setlist[-1]["notes"].append(element)

                elif tag["class"] == ["setlist-song"]:
                    phishnet_url = tag["href"]
                    element = {
                        "song_id": phishnet_url.split("/")[-1],
                        "element_type": "song",
                        "song_url": phishnet_url,
                        "set_label": tag.parent.span.contents[0],
                        "notes": [],
                    }

                    setlist.append(element)

        self.setlist = setlist

    def set_total_song_count(self):
        """Get total song count for the setlist."""
        self.song_counts['total'] = len(self.setlist)

    def set_set1_song_count(self):
        """Get set 1 song count for the setlist."""
        self.song_counts['set1'] = len(
            [song for song in self.setlist if song["set_label"] == "Set 1"])

    def set_set2_song_count(self):
        """Get set 2 song count for the setlist."""
        self.song_counts['set2'] = len(
            [song for song in self.setlist if song["set_label"] == "Set 2"])

    def set_set3_song_count(self):
        """Get set 3 song count for the setlist."""
        self.song_counts['set3'] = len(
            [song for song in self.setlist if song["set_label"] == "Set 3"])

    def set_encore_song_count(self):
        """Get encore song count for the setlist."""
        self.song_counts['encore'] = len(
            [song for song in self.setlist if song["set_label"] == "Encore"])

    def set_encore2_song_count(self):
        """Get encore 2 song count for the setlist."""
        self.song_counts['encore2'] = len(
            [song for song in self.setlist if song["set_label"] == "Encore 2"])

    def set_show_rating(self):
        """Parse show_data_json for rating."""
        self.rating = float(self.data["response"]["data"][0]["rating"])

    def set_relative_date(self):
        """Parse relative show date."""
        self.relative_date = self.data["response"]["data"][0]["relative_date"]

    def set_venue(self):
        """Parse venue and venueid."""
        self.venue = self.data["response"]["data"][0]["venue"]

    def set_show_location(self):
        """Set show location."""
        show_location = self.data['response']['data'][0]['location']
        self.location['country'] = show_location.split(",")[2].strip()
        self.location['state'] = state = show_location.split(",")[1].strip()
        self.location['city'] = state = show_location.split(",")[0].strip()

    def parse_show_location(self):
        """Returns the City, State, Country of a show."""

        city = show_location.split(",")[0].strip()
        state = show_location.split(",")[1].strip()
        country = show_location.split(",")[2].strip()

        return city, state, country


def query_shows(api_key, **kwargs):
    """Query shows"""
    query_str = utils.generate_query_string(**kwargs)
    url = (
        "https://api.phish.net/v3/shows/query?"
        "apikey={api_key}&{query_str}&order=ASC".format(
            api_key=api_key, query_str=query_str
        )
    )

    response = requests.get(url=url, timeout=15)

    return response


def parse_show_dates(show_query_response, artists=[1]):
    """Returns list of show dates from show query response."""
    show_data = show_query_response.json()["response"]["data"]

    show_dates = []
    for show in show_data:
        if show["artistid"] in artists:
            show_dates.append(show["showdate"])
    return show_dates
