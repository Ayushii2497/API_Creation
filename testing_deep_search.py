from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the YouTube Data API client
# api_key = 'YOUR_API_KEY'  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey="AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk")

def search_channel(channel_name):
    try:
        response = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel',
            maxResults=1
        ).execute()
        print("Response Completed")
        if 'items' in response:
            channel = response['items'][0]
            channel_id = channel['id']['channelId']
            channel_title = channel['snippet']['title']

            print('Channel Title:', channel_title)
            print('Channel ID:', channel_id)
        return channel_title
    
    except:
        print("error")

search_channel("sumitkarin")