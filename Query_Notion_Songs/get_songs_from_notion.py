from notion_client import Client
import os

# Script will query notion for 100 songs with the highest rating and output them to a specified file

# ------------------------ SET UP ------------------------
# You need to create a Notion Integration and share your database with that integration
# the secret integration token from Notion Integration
notion_token = ''

# the database id of your notion songs database
# get the mess of numbers after the "/" and before the "?" on your dashboard URL (no need to split into dashes)
database_id = ''

# absolute path to the desired output file (must also include the file name and extension)
song_list_path = ''

# ------------------------ END SET UP ------------------------

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])


# queries top 100 songs from rating S to 3 stars
my_page = notion.databases.query(
    **{
        "database_id": database_id,
        "sorts": [
            {
                "property": "Rating",
                "direction": "descending"
            }
        ]

    }
)

result_list1 = my_page['results']
title_array = []

for song in result_list1:
    title = ''

    try:
        title = song['properties']['Name']['title'][0]['text']['content']
    except:
        title = 'no name'

    title_array.append(title)

title_array = list(dict.fromkeys(title_array))

with open(song_list_path, 'w') as f:
    for title in title_array:
        f.write(title + "\n")
    
