from notion_client import Client
import os
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import sys

# This script takes in a playlist name from the notion playlist db, and creates a merged youtube url of all the songs in the playlist.
# This url contains a youtube playlist of all the songs in the notion playlist.

# ------------------------ SET UP ------------------------
# Youtube API
# api_key: the api_key for the Youtube_Data_API v3 you obtained from the Google Developers Console.
api_key = ""

# Notion Set Up
# notion_token: should be something like 'secret_abcd123454134123...'
notion_token = ''

# playlist_database_id: the notion id of the playlist database.
# Get the mess of numbers after the "/" and before the "?" on your dashboard URL (no need to split into dashes)
playlist_database_id = ''
# ------------------------ END SET UP ------------------------

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])

playlist = input()

my_page = notion.databases.query(
    **{
        "database_id": playlist_database_id,
        "filter": {
            "and": [
                {
                    "property": "Name",
                    "title": {
                        "contains": playlist
                    }
                },
            ]
        }
    }
)

if my_page['results'] == []:
    print('No results found!')
    sys.exit()

song_urls_array = my_page['results'][0]['properties']['Column']['rollup']['array']
page_id = my_page['results'][0]['id']


playlist_url = 'http://www.youtube.com/watch_videos?video_ids='

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/':
            return query.path.split('/')[1]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
        # below is optional for playlists
        if query.path[:9] == '/playlist':
            return parse_qs(query.query)['list'][0]
   # returns None for invalid YouTube url
    print('failed to parse!')

count = 0
for url in song_urls_array:
    url = url['url']
    if (count == 0):
        playlist_url = playlist_url + extract_video_id(url)
    else:
        playlist_url = playlist_url + ',' + extract_video_id(url)

    count = count + 1

notion.pages.update(
    **{
        "page_id": page_id,
        "properties": {
            'URL': {
                'rich_text': [{
                    'type': 'text',
                    'text': {
                        'content': playlist_url
                    }
                }]
            }
        }
    }
)
