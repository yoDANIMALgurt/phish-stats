"""Phish Stats"""
from bs4 import BeautifulSoup
import requests


class Show():
    """Show class"""

    def __init__(self, date, api_key):
        self.date = date
        self.year = int(date.split('-')[0])
        self.month = int(date.split('-')[1])
        self.day = int(date.split('-')[2])
        self.relative_date = None
        self.data = {}
        self.setlist = []
        self.song_counts = {}
        self.country = None
        self.state = None
        self.city = None
        self.rating = None
        self.venue = None
        self.song_booleans = {
            'you-enjoy-myself': 0,
            'tweezer': 0,
        }
        # Set all the show attributes
        self.get_single_show_data(api_key)
        if self.data['response']['data']:
            self.set_attributes()

    def __repr__(self):
        """Representation of a show."""
        return self.date

    def set_attributes(self):
        """Set attributes of Show"""
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
        self.set_song_booleans()

    def get_single_show_data(self, api_key):
        """Get stats of a show by date"""
        url = ("https://api.phish.net/v3/setlists/get?"
               "apikey={api_key}&showdate={date}".format(
                   api_key=api_key, date=self.date))

        print(f'getting setlist for {self.date}')
        response = requests.get(url=url, timeout=15)

        assert response.status_code == 200

        self.data = response.json()

    def parse_setlist(self):
        """Parses setlist from raw setlist data"""
        setlist = []
        soup = BeautifulSoup(self.data["response"]["data"][0]['setlistdata'],
                             features="html.parser")

        for p_tag in soup.find_all("p"):

            setlist_tags = p_tag.contents
            for tag in setlist_tags:
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
        self.relative_date = self.data["response"]["data"][0][
            "relative_date"]

    def set_venue(self):
        """Parse venue and venueid."""
        self.venue = self.data["response"]["data"][0]["venue"]

    def set_show_location(self):
        """Set show location."""
        show_location = self.data['response']['data'][0]['location']
        self.country = show_location.split(",")[2].strip()
        self.state = show_location.split(",")[1].strip()
        self.city = show_location.split(",")[0].strip()

    def set_song_booleans(self):
        """Sets song booleans to 1 if hit songs were played."""
        setlist_song_ids = [song['song_id'] for song in self.setlist]
        for song_id in self.song_booleans:
            self.song_booleans[song_id] = 1 if song_id in setlist_song_ids else 0
