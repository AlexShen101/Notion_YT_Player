from notion_client import Client
import os

# This script takes a name input and queries the specified Notion DB to match the name. If found, it will return the youtube url of the song. 
# Otherwise, it will input 'no_link'.

# ------------------------ SET UP ------------------------
# You need to create a Notion Integration and share your database with that integration
# the secret integration token from Notion Integration
# notion_token: should be something like 'secret_abcd123454134123...'
notion_token = ''

# database_id: the notion id of the songs database. Get the mess of numbers after the "/" and before the "?" on your dashboard URL (no need to split into dashes)
database_id = ''
# ------------------------ END SET UP ------------------------

os.environ['notion_token'] = notion_token
notion = Client(auth=os.environ['notion_token'])


input = input()

# search for inputted name
my_page = notion.databases.query(
    **{
        "database_id": database_id,
        "filter": {
            "property": "Name",
            "text": {
                "equals": input
            }
        },
        "sorts": [
            {
                "property": "Rating",
                "direction": "descending"
            }
        ],
    }
)

# array with 'probably' a single song
resultList = my_page['results']

for song in resultList:
    url = ''

    # No need for try here because we filtered by name before
    title = song['properties']['Name']['title'][0]['text']['content']

    # try to get the link to the queried video
    try:
        url = song['properties']['Link to video']['url']
    except:
        url = 'no link'

    # print url as output
    print(url)
    break
