"""Phish Stats"""
from multiprocessing import Pool

from bs4 import BeautifulSoup
import pandas as pd
import requests

from app import utils


def get_single_show_data(api_key, showdate="2009-06-21"):
    """Get stats of a show by date"""
    url = (
        "https://api.phish.net/v3/setlists/get?"
        "apikey={api_key}&showdate={showdate}".format(
            api_key=api_key, showdate=showdate
        )
    )

    response = requests.get(url=url, timeout=15)

    return response


def get_setlist(setlist_data):
    setlist = []
    soup = BeautifulSoup(setlist_data, features="html.parser")

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

    return setlist


def create_single_show_stats_array(show_data_json):
    """Returns data array and column label array."""
    show_data = show_data_json["response"]["data"][0]
    setlist = get_setlist(show_data["setlistdata"])

    return (
        [
            show_data["showdate"],
            float(show_data["rating"]),
            calculate_total_song_count(setlist),
            calculate_set1_song_count(setlist),
            calculate_set2_song_count(setlist),
            calculate_set3_song_count(setlist),
            calculate_encore_song_count(setlist),
        ],
        [
            "show_date",
            "rating",
            "total_song_count",
            "set1_song_count",
            "set2_song_count",
            "set3_song_count",
            "encore_song_count",
        ],
    )


def calculate_total_song_count(setlist):
    """Get total song count for the setlist."""
    return len(setlist)


def calculate_set1_song_count(setlist):
    """Get set 1 song count for the setlist."""
    return len([song for song in setlist if song["set_label"] == "Set 1"])


def calculate_set2_song_count(setlist):
    """Get set 1 song count for the setlist."""
    return len([song for song in setlist if song["set_label"] == "Set 2"])


def calculate_set3_song_count(setlist):
    """Get set 1 song count for the setlist."""
    return len([song for song in setlist if song["set_label"] == "Set 3"])


def calculate_encore_song_count(setlist):
    """Get set 1 song count for the setlist."""
    return len([song for song in setlist if song["set_label"] == "Encore"])


def get_show_rating(show_data_json):
    """Parse show_data_json for rating."""
    return float(show_data_json["response"]["data"][0]["rating"])


def get_relative_show_date(show_data_json):
    """Parse relative show date."""
    return show_data_json["response"]["data"][0]["relative_date"]


def get_venue(show_data_json):
    """Parse venue and venueid."""
    return show_data_json["response"]["data"][0]["venue"]


def get_relative_show_date(show_data_json):
    """Parse relative show date."""
    return show_data_json["response"]["data"][0]["relative_date"]


def parse_show_location(show_location):
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


def create_df_phish_stats(api_key, show_dates):
    """Returns a pandas dataframe of phish stats."""

    multi_show_data = []
    # Generate data array for each show
    for date in show_dates:
        show_data_json = get_single_show_data(api_key, date).json()
        single_show_stats, column_labels = create_single_show_stats_array(
            show_data_json
        )
        multi_show_data.append(single_show_stats)
    columns = column_labels
    return pd.DataFrame(multi_show_data, columns=columns)
