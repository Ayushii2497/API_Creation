from googleapiclient.discovery import build
import re
from datetime import datetime,timedelta
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from datetime import datetime, timedelta
import google.auth.transport.requests
from nltk.sentiment import SentimentIntensityAnalyzer

class Youtube_API:
    def __init__(self):
        self.yt = build('youtube', 'v3', 
                        developerKey='AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk')
        self.comments_response = ""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                './secrets_1.json',
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