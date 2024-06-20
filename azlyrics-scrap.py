import requests
from bs4 import BeautifulSoup
import re
import unidecode
import argparse


def clean_artist_name(artist_name):
    """ Helper function to format the artist's name
        according to AZLyrics' URLs.
    """
    artist_name = artist_name.lower().replace(' ','')
    artist_name = re.sub(r'[^\w\s]', '', artist_name)
    artist_name = unidecode.unidecode(artist_name)
    return artist_name

def clean_song_name(song_name):
    """ Helper function to format the track's name
        according to AZLyrics' URLs.
    """
    if ('(feat. ' in song_name):
        song_name = song_name[:song_name.find('(feat. ')-1]
    if ('(with ' in song_name):
        song_name = song_name[:song_name.find('(with ')-1]
    song_name = song_name.lower().replace(' ','')
    song_name = re.sub(r'[^\w\s]', '', song_name)
    song_name = unidecode.unidecode(song_name)
    return song_name

def scrape_lyrics(artist, song):
    """ Given a track's (main) artist and name,
        returns the lyrics as a string.
        An empty string is returned if the
        track was not located on AZLyrics.
    """
    artist_name = clean_artist_name(artist)
    song_name = clean_song_name(song)
    
    url = 'https://www.azlyrics.com/lyrics/'+ artist_name + '/' + song_name + '.html'
    page = requests.get(url)
    if page.status_code != 200:
        print("Could not reach", url)
        return ""
    html = BeautifulSoup(page.text, 'html.parser')
    lyric = html.select_one(".ringtone ~ div").get_text(strip=True, separator="\n")

    return lyric


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("artist", help="Mandatory string with artist name")
    parser.add_argument("song", help="Mandatory string with song name")
    args = parser.parse_args()


    lyrics = scrape_lyrics(args.artist, args.song) 
    print(lyrics)
