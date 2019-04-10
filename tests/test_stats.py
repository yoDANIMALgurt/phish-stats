"""Test for generating phish-stats"""

import unittest

from app.config import API_KEY
from app.stats import *
from app.utils import *

class TestPhishStats(unittest.TestCase):
    """Test class for phish stats."""

    def test_get_single_show(self):
        """Can get single show stats."""

        show_date = '2018-10-21'
        response = get_single_show_data(API_KEY, show_date)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()['response']['data'][0].keys()),
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

    def test_generate_query_string(self):
        """Can generate query string."""

        kwargs = {
            'year': '2009',
            'month': '06'
            }
        query_string = generate_query_string(**kwargs)
        self.assertIn(query_string, ['year=2009&month=06',
                                     'month=06&year=2009'])

    def test_query_shows(self):
        """Test query shows."""

        parameters = {'year': '2013',
                      'month': '12',
                      'day': '31'}
        response = query_shows(API_KEY, **parameters)
        self.assertEqual(response.status_code, 200)

    def test_parse_show_dates(self):
        """Can return list of show dates."""

        parameters = {'year': '2010'}
        response = query_shows(API_KEY, **parameters)
        show_dates = parse_show_dates(response, [1])
        self.assertEqual(len(show_dates), 50)

class TestParseShowData_1997_12_07(unittest.TestCase):
    """Test case for parsing raw show data json."""

    @classmethod
    def setUpClass(cls):
        cls.show_data_json = {'error_code': 0, 'error_message': None, 'response': {'count': 1, 'data': [{'showid': 1252695519, 'showdate': '1997-12-07', 'short_date': '12/07/1997', 'long_date': 'Sunday 12/07/1997', 'relative_date': '21 years ago', 'url': 'http://phish.net/setlists/phish-december-07-1997-ervin-j-nutter-center-wright-state-university-dayton-oh-usa.html', 'gapchart': 'http://phish.net/setlists/gap-chart/phish-december-07-1997-ervin-j-nutter-center-wright-state-university-dayton-oh-usa.html', 'artist': "<a href='http://phish.net/setlists/phish'>Phish</a>", 'artistid': 1, 'venueid': 526, 'venue': '<a href="http://phish.net/venue/526/Ervin_J._Nutter_Center%2C_Wright_State_University">Ervin J. Nutter Center, Wright State University</a>', 'location': 'Dayton, OH, USA', 'setlistdata': '<p><span class=\'set-label\'>Set 1</span>: <a href=\'http://phish.net/song/acdc-bag\' class=\'setlist-song\'>AC/DC Bag</a> -> <a href=\'http://phish.net/song/psycho-killer\' class=\'setlist-song\'>Psycho Killer</a><sup title="Unfinished.">[1]</sup> -> <a title="Fantastic -&gt; in from &quot;Psycho Killer.&quot; Played at a faster tempo, this one is more of a rocker and includes a &quot;Rocky Mountain Way&quot; tease." href=\'http://phish.net/song/jesus-just-left-chicago\' class=\'setlist-song\'>Jesus Just Left Chicago</a>, <a href=\'http://phish.net/song/my-minds-got-a-mind-of-its-own\' class=\'setlist-song\'>My Mind\'s Got a Mind of its Own</a> > <a title="&quot;Swept Away&quot; and &quot;Steep&quot; sandwich. Flawless segue to &quot;Swept Away.&quot;" href=\'http://phish.net/song/its-ice\' class=\'setlist-song\'>It\'s Ice</a> -> <a title="-&gt; in from &quot;It\'s Ice.&quot; &quot;Swept Away&quot; and &quot;Steep&quot; form the meat of this &quot;Ice&quot; sandwich. &gt; to &quot;Steep.&quot;" href=\'http://phish.net/song/swept-away\' class=\'setlist-song\'>Swept Away</a> > <a title="> in from &quot;Swept Away.&quot; Part II of the meat of this &quot;Ice&quot; sandwich. > back to &quot;Ice.&quot;" href=\'http://phish.net/song/steep\' class=\'setlist-song\'>Steep</a> > <a title="> in from &quot;Steep&quot; to complete this version of &quot;Ice.&quot;" href=\'http://phish.net/song/its-ice\' class=\'setlist-song\'>It\'s Ice</a> > <a title="Precise and coordinated modulation between major and minor modes by Trey, Page and Mike give this excellent version a subtle sense of tension and release." href=\'http://phish.net/song/theme-from-the-bottom\' class=\'setlist-song\'>Theme From the Bottom</a>, <a title="The first &quot;Tube&quot;to break out of the box begins with sweet funk in the first jam, while the jam reprise drops into some space, builds back up to more funk, and coasts into the -> to &quot;Slave&quot;.  A fan-favorite." href=\'http://phish.net/song/tube\' class=\'setlist-song\'>Tube</a>, <a href=\'http://phish.net/song/jam\' class=\'setlist-song\'>Jam</a> -> <a title="-> in from an awesome &quot;Tube.&quot; Fan favorite version. Trey is really out in front on this one, soloing beautifully." href=\'http://phish.net/song/slave-to-the-traffic-light\' class=\'setlist-song\'>Slave to the Traffic Light</a></p><p><span class=\'set-label\'>Set 2</span>: <a title="&quot;Timber&quot; opens Set II for the 5th consecutive time in as many appearances. This excellent version has a slightly less dark and somber vibe than most and is an almost upbeat, contemplative piece." href=\'http://phish.net/song/timber-jerry-the-mule\' class=\'setlist-song\'>Timber (Jerry The Mule)</a> > <a title="> in from &quot;Timber.&quot; Great, short version loosens out of funk mode briefly, mellows into more funk and -> to the first &quot;Boogie On Reggae Woman&quot; in 988 shows (last seen on 9/13/88). The &quot;Wolfman\'s&quot; release really comes in the sweet jam out of &quot;BORW.&quot;" href=\'http://phish.net/song/wolfmans-brother\' class=\'setlist-song\'>Wolfman\'s Brother</a> -> <a title="Busted out after a 989 show gap and segues smoothly out of Wolfman\'s Brother. The \'97 style outro jam is distinct and deviates from the structure of &quot;Boogie&quot; at 5 minutes and is played at a slower tempo than recent versions. Transitions to a hot &quot;Reba&quot;." href=\'http://phish.net/song/boogie-on-reggae-woman\' class=\'setlist-song\'>Boogie On Reggae Woman</a> > <a href=\'http://phish.net/song/reba\' class=\'setlist-song\'>Reba</a><sup title="No whistling.">[2]</sup>, <a href=\'http://phish.net/song/guyute\' class=\'setlist-song\'>Guyute</a> > <a title="\t&quot;Camel Walk&quot;-like licks and polka scales in the intro. Very tight straightforward jam that ends with more polka-style chords." href=\'http://phish.net/song/possum\' class=\'setlist-song\'>Possum</a></p><p><span class=\'set-label\'>Encore</span>: <a href=\'http://phish.net/song/a-day-in-the-life\' class=\'setlist-song\'>A Day in the Life</a><p class=\'setlist-footer\'>[1] Unfinished.<br>[2] No whistling.<br></p>', 'setlistnotes': 'Psycho Killer was unfinished. JJLC included a Rocky Mountain Way tease.&nbsp;Boogie On Reggae Woman was played for the first time since September 13, 1988 (988&nbsp;shows). Reba did not have the whistling ending. Possum included &quot;Charge!&quot; teases and a We Will Rock You tease from Mike.&nbsp;This show isavailable as an archival release on LivePhish.com.<br>via <a href="http://phish.net">phish.net</a>', 'rating': '4.6645'}]}}        

    def test_get_setlist(self):
        """Test get setlist of specific date."""        
        setlist_data = self.show_data_json['response']['data'][0]['setlistdata']
        setlist = get_setlist(setlist_data)
        self.assertEqual(len(setlist), 19)

    def test_get_show_rating(self):
        """Test get show rating."""
        rating = get_show_rating(self.show_data_json)
        self.assertEqual(rating, 4.6645)

    def test_get_relative_date(self):
        """Test get relative date."""
        relative_date = get_relative_show_date(self.show_data_json)

    def test_parse_location(self):
        """Can get location of show."""

        (city, state, country) = parse_show_location(self.show_data_json['response']['data'][0]['location'])
        self.assertEqual(city, 'Dayton')
        self.assertEqual(state, 'OH')
        self.assertEqual(country, 'USA') 

    def test_create_single_show_stats_array(self):
        """Test create single show vector."""        
        show_stats_array, column_labels = create_single_show_stats_array(self.show_data_json)
        self.assertEqual(str(type(show_stats_array)), "<class 'list'>" )
        self.assertEqual(show_stats_array, ['1997-12-07', 4.6645, 19, 12, 6, 0, 1, 0])
        self.assertEqual(
            column_labels, 
            [
                'show_date',
                'rating',
                'total_song_count',
                'set1_song_count',
                'set2_song_count',
                'set3_song_count',
                'encore_song_count',
                'encore2_song_count'
            ]
        )                 

class TestDoubleEncoreShow_2018_10_21(unittest.TestCase):
    """Test case for parsing a double encore show"""

    @classmethod
    def setUpClass(cls):
        cls.show_data_json = {'error_code': 0, 'error_message': None, 'response': {'count': 1, 'data': [{'showid': 1526437700, 'showdate': '2018-10-21', 'short_date': '10/21/2018', 'long_date': 'Sunday 10/21/2018', 'relative_date': '6 months ago', 'url': 'http://phish.net/setlists/phish-october-21-2018-hampton-coliseum-hampton-va-usa.html', 'gapchart': 'http://phish.net/setlists/gap-chart/phish-october-21-2018-hampton-coliseum-hampton-va-usa.html', 'artist': "<a href='http://phish.net/setlists/phish'>Phish</a>", 'artistid': 1, 'venueid': 6, 'venue': '<a href="http://phish.net/venue/6/Hampton_Coliseum">Hampton Coliseum</a>', 'location': 'Hampton, VA, USA', 'setlistdata': '<p><span class=\'set-label\'>Set 1</span>: <a href=\'http://phish.net/song/stealing-time-from-the-faulty-plan\' class=\'setlist-song\'>Stealing Time From the Faulty Plan</a>, <a href=\'http://phish.net/song/skin-it-back\' class=\'setlist-song\'>Skin It Back</a>, <a href=\'http://phish.net/song/brian-and-robert\' class=\'setlist-song\'>Brian and Robert</a>, <a href=\'http://phish.net/song/timber-jerry-the-mule\' class=\'setlist-song\'>Timber (Jerry The Mule)</a> > <a title="\nA creeping late-night stroll accented by a descending progression and mysterious Trey soloing then smoothly transitions to bliss and ignites at minute 17 for a joyous, trill-filled peak before slamming back into &quot;Simple&quot; to end." href=\'http://phish.net/song/simple\' class=\'setlist-song\'>Simple</a>, <a href=\'http://phish.net/song/mexican-cousin\' class=\'setlist-song\'>Mexican Cousin</a>, <a title="Mike and Page lead a funky, exploratory back-end jam. The energy builds when Trey jumps in, adding to the mix. Nice to hear this camel have a walk about." href=\'http://phish.net/song/camel-walk\' class=\'setlist-song\'>Camel Walk</a> > <a href=\'http://phish.net/song/back-on-the-train\' class=\'setlist-song\'>Back on the Train</a> > <a href=\'http://phish.net/song/saw-it-again\' class=\'setlist-song\'>Saw It Again</a></p><p><span class=\'set-label\'>Set 2</span>: <a title="The substantial post-lyrics jam visits places both light and dark and eventually settles into a jazzy minor zone with a vibe similar to &quot;Timber Ho&quot; and, in the last minute, &quot;David Bowie&quot;, as it gathers steam and seems poised to explode but makes a good -> to &quot;Rise/Come Together&quot; instead. " href=\'http://phish.net/song/waves\' class=\'setlist-song\'>Waves</a> -> <a href=\'http://phish.net/song/risecome-together\' class=\'setlist-song\'>Rise/Come Together</a> > <a title="The jam peels away from typical playing at around 5:45, shifting to some soft, warm grooving. Picking up energy, the familiar &quot;bliss&quot; jam feels imminent, but instead, the playing shifts to some darker, spacey, Mike-led punchy rock. The intensity builds to a peak, before grinding down." href=\'http://phish.net/song/light\' class=\'setlist-song\'>Light</a> > <a href=\'http://phish.net/song/the-line\' class=\'setlist-song\'>The Line</a>, <a href=\'http://phish.net/song/wingsuit\' class=\'setlist-song\'>Wingsuit</a> > <a href=\'http://phish.net/song/your-pet-cat\' class=\'setlist-song\'>Your Pet Cat</a>, <a href=\'http://phish.net/song/whats-the-use\' class=\'setlist-song\'>What\'s the Use?</a> > <a title="Following a quality piano solo, Trey grabs the marsupial by the scruff of the neck, and proceeds to give it a serious workout. Like many versions from the early \'90s, Trey explores a number of musical ideas and variation, all within the context of &quot;Possum.&quot; Strong, straightforward jamming here." href=\'http://phish.net/song/possum\' class=\'setlist-song\'>Possum</a></p><p><span class=\'set-label\'>Encore</span>: <a href=\'http://phish.net/song/more\' class=\'setlist-song\'>More</a></p><p><span class=\'set-label\'>Encore 2</span>: <a href=\'http://phish.net/song/you-enjoy-myself\' class=\'setlist-song\'>You Enjoy Myself</a>', 'setlistnotes': 'This show was&nbsp;webcast via&nbsp;<a href="http://www.livephish.com/">Live Phish</a>.&nbsp;Skin It Back was played for the first time since August 11, 2015&nbsp;(113&nbsp;shows). Camel Walk included Skin It Back teases. BOTT included a Streets of Cairo tease&nbsp;and Possum included William Tell Overture tease.<br>via <a href="http://phish.net">phish.net</a>', 'rating': '4.1390'}]}}

    def test_get_setlist(self):
        """Test get setlist of specific date."""        
        setlist_data = self.show_data_json['response']['data'][0]['setlistdata']
        setlist = get_setlist(setlist_data)
        self.assertEqual(len(setlist), 19)

    def test_get_show_rating(self):
        """Test get show rating."""
        rating = get_show_rating(self.show_data_json)
        self.assertEqual(rating, 4.139)

    def test_get_relative_date(self):
        """Test get relative date."""
        relative_date = get_relative_show_date(self.show_data_json)

    def test_parse_location(self):
        """Can get location of show."""

        (city, state, country) = parse_show_location(self.show_data_json['response']['data'][0]['location'])
        self.assertEqual(city, 'Hampton')
        self.assertEqual(state, 'VA')
        self.assertEqual(country, 'USA') 

    def test_create_single_show_stats_array(self):
        """Test create single show vector."""        
        show_stats_array, column_labels = create_single_show_stats_array(self.show_data_json)
        self.assertEqual(str(type(show_stats_array)), "<class 'list'>" )
        self.assertEqual(show_stats_array, ['2018-10-21', 4.139, 19, 9, 8, 0, 1, 1])
        self.assertEqual(
            column_labels, 
            [
                'show_date',
                'rating',
                'total_song_count',
                'set1_song_count',
                'set2_song_count',
                'set3_song_count',
                'encore_song_count',
                "encore2_song_count",           
            ]
        )                 

class TestSetlistCalculations(unittest.TestCase):
    """Test case for testing setlist calculations."""

    @classmethod
    def setUpClass(cls):
        cls.show_date = '1997-12-07'
        cls.setlist = [
            {'song_id': 'acdc-bag', 'element_type': 'song', 'song_url': 'http://phish.net/song/acdc-bag', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'psycho-killer', 'element_type': 'song', 'song_url': 'http://phish.net/song/psycho-killer', 'set_label': 'Set 1', 'notes': [{'note_id': 1, 'element_type': 'note', 'body': 'Unfinished.'}]},
            {'song_id': 'jesus-just-left-chicago', 'element_type': 'song', 'song_url': 'http://phish.net/song/jesus-just-left-chicago', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'my-minds-got-a-mind-of-its-own', 'element_type': 'song', 'song_url': 'http://phish.net/song/my-minds-got-a-mind-of-its-own', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'its-ice', 'element_type': 'song', 'song_url': 'http://phish.net/song/its-ice', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'swept-away', 'element_type': 'song', 'song_url': 'http://phish.net/song/swept-away', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'steep', 'element_type': 'song', 'song_url': 'http://phish.net/song/steep', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'its-ice', 'element_type': 'song', 'song_url': 'http://phish.net/song/its-ice', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'theme-from-the-bottom', 'element_type': 'song', 'song_url': 'http://phish.net/song/theme-from-the-bottom', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'tube', 'element_type': 'song', 'song_url': 'http://phish.net/song/tube', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'jam', 'element_type': 'song', 'song_url': 'http://phish.net/song/jam', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'slave-to-the-traffic-light', 'element_type': 'song', 'song_url': 'http://phish.net/song/slave-to-the-traffic-light', 'set_label': 'Set 1', 'notes': []},
            {'song_id': 'timber-jerry-the-mule', 'element_type': 'song', 'song_url': 'http://phish.net/song/timber-jerry-the-mule', 'set_label': 'Set 2', 'notes': []},
            {'song_id': 'wolfmans-brother', 'element_type': 'song', 'song_url': 'http://phish.net/song/wolfmans-brother', 'set_label': 'Set 2', 'notes': []},
            {'song_id': 'boogie-on-reggae-woman', 'element_type': 'song', 'song_url': 'http://phish.net/song/boogie-on-reggae-woman', 'set_label': 'Set 2', 'notes': []},
            {'song_id': 'reba', 'element_type': 'song', 'song_url': 'http://phish.net/song/reba', 'set_label': 'Set 2', 'notes': [{'note_id': 2, 'element_type': 'note', 'body': 'No whistling.'}]},
            {'song_id': 'guyute', 'element_type': 'song', 'song_url': 'http://phish.net/song/guyute', 'set_label': 'Set 2', 'notes': []},
            {'song_id': 'possum', 'element_type': 'song', 'song_url': 'http://phish.net/song/possum', 'set_label': 'Set 2', 'notes': []},
            {'song_id': 'a-day-in-the-life', 'element_type': 'song', 'song_url': 'http://phish.net/song/a-day-in-the-life', 'set_label': 'Encore', 'notes': []}
        ]

    def test_calculate_total_song_count(self):
        """Get total song count for the setlist."""
        total_song_count = calculate_total_song_count(self.setlist)
        self.assertEqual(total_song_count, 19)

    def test_calculate_set1_song_count(self):
        """Get set 1 song count for the setlist."""
        set1_song_count = calculate_set1_song_count(self.setlist)
        self.assertEqual(set1_song_count, 12)

    def test_calculate_set2_song_count(self):
        """Get set 1 song count for the setlist."""
        set2_song_count = calculate_set2_song_count(self.setlist)
        self.assertEqual(set2_song_count, 6)        

    def test_calculate_set3_song_count(self):
        """Get set 1 song count for the setlist."""
        set3_song_count = calculate_set3_song_count(self.setlist)
        self.assertEqual(set3_song_count, 0)

    def test_calculate_encore_song_count(self):
        """Get set 1 song count for the setlist."""
        encore_song_count = calculate_encore_song_count(self.setlist)
        self.assertEqual(encore_song_count, 1)

    def test_create_df_phish_stats(self):
        """Test create pandas df for list of shows."""
        show_dates = ['1997-12-07', '1997-11-17']
        df_phish_stats = create_df_phish_stats(API_KEY, show_dates)        
        self.assertEqual(str(type(df_phish_stats)),"<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_phish_stats.shape, (2, 8))
        self.assertEqual(
            set(df_phish_stats.columns), 
            {
                'set1_song_count', 
                'encore_song_count',
                'encore2_song_count',
                'set2_song_count',
                'total_song_count',
                'set3_song_count',
                'show_date',
                'rating'
            }
        )

if __name__ == '__main__':
    unittest.main()
