# Youtube Video Info Scraper
# Given a video url, get the video info

import os
import sys
from notion_client import Client
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# ------------------------ SET UP ------------------------
# See instructions on github to set up this section.

# Notion Set Up
# notion_token: should be something like 'secret_abcd123454134123...'
# database_id: the notion_id of the songs database. Get the mess of numbers after the "/" and before the "?" on your dashboard URL (no need to split into dashes)
# artist_database_id: the notion id of the artist database
notion_token = ''
database_id = '' 
artist_database_id = ''

# Youtube Set Up
# api_key: the api_key you obtained from the Google Developers Console.
api_key = ""

# ------------------------ END OF SET UP ------------------------

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])
youtube = build('youtube', 'v3', developerKey=api_key)

# Converts a youtube url and only retrieves the id
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
    print('failed to parse: ' + url)

# Get info from API by using youtube ID
def scrape(youtube_url):
    video_id = extract_video_id(youtube_url)
    if (video_id == None):
        return
    data = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Extract Important Info
    snippet = data['items'][0]['snippet']
    return snippet

# Get youtube url and get info from video using youtube API
print("Input youtube URL: ")
youtube_url = input("")
snippet = scrape(youtube_url)

if (snippet == None):
    print('Invalid run')
    sys.exit()

# ------------------------ Get Snipped Info
title = snippet['title']
artist_name = snippet['channelTitle']

try:
    thumbnail = snippet['thumbnails']['maxres']['url']
except:
    print('\n\nno maxres')
    try:
        thumbnail = snippet['thumbnails']['standard']['url']
    except:
        print('\n\nno standard')
        thumbnail = snippet['thumbnails']['default']['url']

if (artist_name.find('- Topic') != -1):
    artist_name = artist_name.split(' -')[0]

print("Input Categories: ")
entry_categories = input()
print("Input Mood: ")
entry_mood = input()
print("Input Rating: ")
entry_rating = input()
print("Input Notes: ")
entry_notes = input()

title_query = notion.databases.query(
    **{
        "database_id": database_id,
        "filter": {
            "property": "Name",
            "title": {
                "contains": title
            }
        },
    }
)
artist_query = notion.databases.query(
    **{
        "database_id": artist_database_id,
        "filter": {
            "property": "Name",
            "title": {
                "contains": artist_name
            }
        },
    }
)

# Check if the song and artist is already in the database (do nothing if found)
if title_query['results'] != [] and artist_query['results'] != []:
    print('song is already in database')
    sys.exit()
# Check if the artist already exists
elif (artist_query['results'] != []):
    artist_id = artist_query['results'][0]['id']
    print('artist found: ' + artist_query['results'][0]['properties']
          ['Name']['title'][0]['text']['content'])
else:
    new_artist = notion.pages.create(
        **{
            'parent': {
                'database_id': artist_database_id,
            },
            'properties': {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": artist_name
                            }}]}}})
    artist_id = new_artist['id']
    print('no artist found')
    print('creating new artist with id: ' + artist_id)

# Give basic properties to the notion entry
properties = {
    "Name": {
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ]
    },
    "Link to video": {
        'url': youtube_url
    },
    "Additional Notes": {
        'rich_text': [{
            'text': {
                'content': entry_notes,
            },
        }]
    },
    "Thumbnail": {
        "files": [
            {
                "name": thumbnail,
                "type": "external",
                "external": {
                    "url": thumbnail
                }
            }
        ]
    },
    "Artist": {
        "relation": [
            {
                "id": artist_id
            }
        ]
    }
}

# Check if rating were inputted, and add to notion entry properties if so
if (entry_rating != ""):
    rating = {
        "select": {
            "name": entry_rating
        }
    }

    properties['Rating'] = rating

# Check if categories were inputted, and add to notion entry properties if so
if (entry_categories != ""):
    # If multiple categories are added, 
    if ',' in entry_categories:
        entry_categories = entry_categories.split(', ')
    else:
        entry_categories = [entry_categories]

    multi_categories_array = []

    for entry in entry_categories:
        multi_categories_array.append({
            'name': entry
        })

    categories = {
        'multi_select': multi_categories_array
    }

    properties['Categories'] = categories

# Check if moods were inputted
if (entry_mood != ""):
    if ',' in entry_mood:
        entry_mood = entry_mood.split(', ')
    else:
        entry_mood = [entry_mood]

    multi_moods_array = []

    for entry in entry_mood:
        if entry not in multi_moods_array:
            multi_moods_array.append({
                'name': entry
            })

    moods = {
        'multi_select': multi_moods_array
    }

    properties['Mood'] = moods

new_page = notion.pages.create(
    **{
        'parent': {
            'database_id': database_id,
        },
        'properties': properties
    })

new_id = new_page['id']
print('new page created!')
print(new_id)
