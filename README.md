# Notion_YT_Player

### Demo

Youtube player features:

https://github.com/user-attachments/assets/5161a91c-52a9-43b0-a7f4-b184b4968a48

Scraping demo:

https://github.com/user-attachments/assets/6211d955-ab88-4f82-91d6-53de9d8f4e57




### Description
A project meant to simulate a barebones music player using Youtube as the music player and Notion to store songs. Users are able to access and control Youtube quickly and easily while staying focused on other tasks, which removes the annoyance of having to find or unminimize the Youtube tab when you want to adjust volume, change songs, or see what song is playing so you can add it to your song collection. This music player mainly uses python scripts to communicate with the youtube and notion api, and is also intended to be used with Keyboard Maestro in order to get the full functionality of the music player and the ability to input commands from any screen.

### General Setup
This setup will cover how to hook up your notion database with the python scripts in this collection. It will not cover how to use the Keyboard Maestro macros, since the python scripts can function standalone.

#### Installing Required Dependencies
The dependencies required for the python script are listed in requirements.txt. If there is an issue you only need to install "notion_client" (used version 1.0.0) and "google-auth" (used version 1.35.0).

The setup section of the python scripts will look something like this:
![image](https://user-images.githubusercontent.com/85968705/207165402-7bf23427-c02c-49ed-99ab-489489f6c550.png)

#### Notion Database ID Setup
To set up the notion component, you'll need to make an Artist Database, Songs Database, and Playlist Database in notion. To do this, make a Notion Page, and then select the "Table Database" option.
Here is a sample page containing all three of these databases: https://congruous-chatter-586.notion.site/YT-Songs-Template-49a3e7f4d9ab40868a088f54829d2114

Template Artists Database ID: https://www.notion.so/82e106c8af754923b801331872f5fb4a?v=5b0e5542dfba42ab82f1660ab3edf785

Template Songs Database ID: https://www.notion.so/0f538d08ffb74d86a0ccb48b7afc327a?v=9a498c158fec4dc49e253447cd08543e

Template Playlists Database ID: https://www.notion.so/8a2aecb469e2449fa94db7f3a0a31b32?v=f55435ef46da4b8ebc8646c940e921a5

**Note that the names of the notion columns have to have the same names as the template names**.

Now, you can add in the database ID to the python script. The url of your database should look like this: https://www.notion.so/0f538d08ffb74d86a0ccb48b7afc327a?v=9a498c158fec4dc49e253447cd08543e. The database ID of this page would be '0f538d08ffb74d86a0ccb48b7afc327a'. Copy the IDs from both of your databases and paste them into the python script.

#### Notion_Token Setup
This refers to your api token given from the notion API. First, visit https://www.notion.so/my-integrations and sign in. Then, make a new integration and click the "View integration" link. Then, under the Secrets section, view and copy your Internal Integration Token. **This token should be kept secret and kept to yourself.** Copy this token and paste it into the python script.

For more information, see: https://developers.notion.com/docs/create-a-notion-integration and https://developers.notion.com/docs/authorization.

#### Youtube API_Key Setup
First, go to https://console.developers.google.com/. Create a new project in the console. Now, we will add the Youtube Data API. Click on Library, and search for the **Youtube Data API**. Enable it for your project and visit the "Enabled APIs page" (https://console.cloud.google.com/apis/enabled) to make sure the status is ON for the Youtube Data API v3. Now, create an API key by clicking Credentials (https://console.cloud.google.com/apis/credentials) > Create Credentials > API key.
Copy the API key and paste it in the python script. 

For more information, see: https://developers.google.com/youtube/v3/getting-started and https://developers.google.com/youtube/registering_an_application

Congratulations! The setup is complete and the python script should be set up!
