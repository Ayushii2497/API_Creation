from googleapiclient.discovery import build
import re
import requests
import os
import configparser
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from datetime import datetime, timedelta
import google.auth.transport.requests
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import itertools
from operator import itemgetter
# Read the configuration file
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), "data_io", "config.ini"))

youtube_api_key = config.get("creds", "youtube_api_key")


class Youtube_API:
    def __init__(self):
        self.yt = build("youtube", "v3", developerKey=youtube_api_key)
        self.comments_response = ""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                os.path.join(os.getcwd(), "misc", "secrets_1.json"),
                scopes=["https://www.googleapis.com/auth/youtube.readonly"],
            )
            credentials.refresh(google.auth.transport.requests.Request())
            self.yt_analytics = build("youtubeAnalytics", "v2", credentials=credentials)
        except GoogleAuthError as e:
            print("Failed to obtain access token:", str(e))
            raise

    def channel_respose(self, channel_name):
        ch_resp = (
            self.yt.channels()
            .list(
                forUsername=channel_name,
                part="id, snippet, statistics, contentDetails, topicDetails",
            )
            .execute()
        )
        if ch_resp.get("items",""):
            channel_data = ch_resp.get("items")[0]
            subscriber_count = channel_data["statistics"]["subscriberCount"]
            joining_date = channel_data["snippet"]["publishedAt"]
            total_views = channel_data["statistics"]["viewCount"]
            channel_dict = {
                "Subscriber_Count": subscriber_count,
                "Join_Date": joining_date,
                "Views": total_views,
                "Channel_Name": channel_name,
            }
            return channel_dict
        return False

    def audience_response(self):
        # Retrieve audience analytics
        analytics_request = self.yt_analytics.reports().query(
            ids=f"channel=={self.channel_id}",
            startDate=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            endDate=datetime.now().strftime("%Y-%m-%d"),
            metrics="viewerPercentage",
            dimensions="day",
            sort="day",
        )
        analytics_response = analytics_request.execute()

    def demographics_request(self):
        demographics_request = self.yt.channels().list(
            part="brandingSettings", id="UCbmNph6atAoGfqLoCL_duAg"
        )
        demographics_response = demographics_request.execute()
        demographics = demographics_response["items"][0]["brandingSettings"]["channel"][
            "targetedDemographics"
        ]

    def comments_request(self):
        comments_request = self.yt.commentThreads().list(
            part="snippet",
            allThreadsRelatedToChannelId="UCbmNph6atAoGfqLoCL_duAg",
            order="time",
            maxResults=10,
        )
        self.comments_response = comments_request.execute()

    def sentiment_analyse(self):
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiments = []
        for item in self.comments_response["items"]:
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            sentiment_scores = sentiment_analyzer.polarity_scores(comment_text)
            sentiment = sentiment_scores["compound"]
            sentiments.append(sentiment)

        sentiment_score = sum(sentiments) / len(sentiments) if sentiments else 0
        return sentiment_score

    def top_videos_info(self, channel_name):
        final_resp = []
        email_list = []
        channels_response = (
            self.yt.channels()
            .list(
                forUsername=channel_name,
                part="id, snippet, statistics, contentDetails, topicDetails",
            )
            .execute()
        )
        channel_id = channels_response["items"][0]["id"]
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=10&order=date&type=video&key={youtube_api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        sentiment_analyzer = SentimentIntensityAnalyzer()
        for ele in data["items"]: 
            sentiments = []
            title = ele["snippet"]["title"]
            # print(f"Processing - {title}")
            vid_id = ele["id"]["videoId"]
            video_response = (
                self.yt.videos().list(part="snippet,statistics", id=vid_id).execute()
            )
            # likes = video_response["items"][0]["statistics"]["likeCount"]
            comment_count = video_response["items"][0]["statistics"].get(
                "commentCount", 0
            )
            des = video_response["items"][0]["snippet"]["description"]
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(des))
            if emails:
                email_list.append(emails)

            sentiment_score = 0
            replygre=[]
            likesmore=[]
            normal=[]
            # print(comment_count)
            if comment_count:
                video_replies = (
                    self.yt.commentThreads().list(part="snippet,replies", videoId=vid_id, maxResults=100).execute()
                )
                for rep in video_replies["items"]:
                    comment = rep["snippet"]["topLevelComment"]["snippet"].get(
                        "textDisplay"
                    )
                    
                    replycount = rep["snippet"]["totalReplyCount"]
                    likes=rep['snippet']['topLevelComment']['snippet']['likeCount']
                    dic = {'likes': likes, 'comment': comment, 'replycount': replycount}
                    if replycount > 0 and likes < replycount:
                        replygre.append(dic)
                    elif likes > replycount:
                        likesmore.append(dic)
                    elif likes == 0 and replycount == 0:
                        normal.append(dic)
                likes_lst = sorted(likesmore, key=itemgetter('likes'), reverse=True) 
                all_data=list(itertools.chain(replygre,likes_lst,normal))
                top_comments=all_data[:150]
                for ele in top_comments:
                    sentiment_scores = sentiment_analyzer.polarity_scores(ele['comment'])
                    sentiments.append(sentiment_scores["compound"])
                    
                    
                    # if replycount > 0:
                    #     for reply in rep["replies"]["comments"]:
                    #         reply = reply["snippet"]["textDisplay"]
                    #         replies.append(reply)
                sentiment_score = sum(sentiments) / len(sentiments) if sentiments else 0

            response = {
                "Title": title,
                "Comments Count": comment_count,
                "sentiment_score": sentiment_score,
            }
            final_resp.append(response)

        return {
                "Parsed_email_ids": email_list,
                "latest_videos":final_resp
            }
