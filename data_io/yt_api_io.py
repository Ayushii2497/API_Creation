from googleapiclient.discovery import build
import re
import requests
import os
import configparser
from datetime import datetime,timedelta
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from datetime import datetime, timedelta
import google.auth.transport.requests
from nltk.sentiment import SentimentIntensityAnalyzer
import json

# Read the configuration file
config = configparser.ConfigParser()
print(os.path.join(os.getcwd(),"data_io",'config.ini'))
config.read(os.path.join(os.getcwd(),"data_io",'config.ini'))

youtube_api_key = config.get('creds', 'youtube_api_key')

class Youtube_API:
    def __init__(self):
        self.yt = build('youtube', 'v3', 
                        developerKey=youtube_api_key)
        self.comments_response = ""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                os.path.join(os.getcwd(),"misc",'secrets_1.json'),
                scopes=['https://www.googleapis.com/auth/youtube.readonly']
            )
            credentials.refresh(google.auth.transport.requests.Request())
            self.yt_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        except GoogleAuthError as e:
            print('Failed to obtain access token:', str(e))
            raise


    def channel_respose(self, channel_name):
        ch_resp = self.yt.channels().list(
                forUsername=channel_name,
                part="id, snippet, statistics, contentDetails, topicDetails"
        ).execute()

        channel_data=ch_resp.get("items")[0] 
        subscriber_count = channel_data['statistics']['subscriberCount']
        joining_date = channel_data['snippet']['publishedAt']
        total_views = channel_data['statistics']['viewCount']
        channel_dict = {
            "sub_cnt" : subscriber_count,
            "jng_date" : joining_date,
            "ttl_vws" : total_views
        }
        return channel_dict

    def audience_response(self):
        # Retrieve audience analytics
        analytics_request = self.yt_analytics.reports().query(
            ids=f'channel=={self.channel_id}',
            startDate=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
            endDate=datetime.now().strftime('%Y-%m-%d'),
            metrics='viewerPercentage',
            dimensions='day',
            sort='day'
        )
        analytics_response = analytics_request.execute()

    def demographics_request(self):
        demographics_request = self.yt.channels().list(
	        part='brandingSettings',
	        id="UCbmNph6atAoGfqLoCL_duAg"
	    )
        demographics_response = demographics_request.execute()
        demographics = demographics_response['items'][0]['brandingSettings']['channel']['targetedDemographics']

    def comments_request(self):
        comments_request = self.yt.commentThreads().list(
	        part='snippet',
	        allThreadsRelatedToChannelId="UCbmNph6atAoGfqLoCL_duAg",
	        order='time',
	        maxResults=10
	    )
        self.comments_response = comments_request.execute()

    def sentiment_analyse(self):
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiments = []
        for item in self.comments_response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment_scores = sentiment_analyzer.polarity_scores(comment_text)
            sentiment = sentiment_scores['compound']
            sentiments.append(sentiment)

        sentiment_score = sum(sentiments) / len(sentiments) if sentiments else 0
        return sentiment_score
    
    def top_videos_info(self,channel_name):
        channels_response = self.yt.channels().list(
        forUsername=channel_name,
        part="id, snippet, statistics, contentDetails, topicDetails"
        ).execute()
        channel_id=channels_response['items'][0]['id']
        url=f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=10&order=date&type=video&key={youtube_api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        for ele in data['items']:
            vid_id=ele['id']['videoId']
            video_response= self.yt.videos().list(part='snippet,statistics', id=vid_id).execute()
            likes = video_response['items'][0]['statistics']['likeCount']
            comment_count = video_response['items'][0]['statistics']['commentCount']
            des = video_response['items'][0]['snippet']['description']
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(des))
        response={"Video ID":vid_id,"Likes":likes,"Comments Count":comment_count,"Email ID":emails}
        return response