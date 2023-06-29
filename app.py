import redis
from googleapiclient.discovery import build
import re
from datetime import datetime, timedelta

# redisClient = redis.Redis(host='localhost', port=6379, db=0)
# redisClient.set("status","ABC")
# redisClient.set("timestamp","")
# redisClient.set("channel_name","")
# redisClient.set("channel_user_name","")
# redisClient.set("subscriber_count","")
# redisClient.set("views","")
# redisClient.set("join_date","")
# redisClient.set("Parsed_email_ids","")
# redisClient.set("latest_videos","")

# print(redisClient.get("status"))
# youtube = build('youtube', 'v3', credentials=creds)
# youtube1 = build('youtube', 'v3',developerKey='AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk')
# search_channel_name = 'atgoogletalks'

# channels_response = youtube1.channels().list(
#         forUsername=search_channel_name,
#         part="id, snippet, statistics, contentDetails, topicDetails"
# ).execute()


# def video_info(channels_response):
#     items=channels_response.get("items")[0]
#     # get the snippet, statistics & content details from the video response
#     snippet         = items["snippet"]
#     statistics      = items["statistics"]
#     content_details = items["contentDetails"]
#     # get infos from the snippet
#     # channel_title = snippet["channelTitle"]
#     title         = snippet["title"]
#     description   = snippet["description"]
#     publish_time  = snippet["publishedAt"]
#     # get stats infos
#     comment_count = statistics["commentCount"]
#     like_count    = statistics["likeCount"]
#     view_count    = statistics["viewCount"]
#     # get duration from content details
#     duration = content_details["duration"]
#     # duration in the form of something like 'PT5H50M15S'
#     # parsing it to be something like '5:50:15'
#     parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
#     duration_str = ""
#     for d in parsed_duration:
#         if d:
#             duration_str += f"{d[:-1]}:"
#     duration_str = duration_str.strip(":")
#     print(f"""\
#     Title: {title}
#     Description: {description}
#     Channel Title: {channel_title}
#     Publish time: {publish_time}
#     Duration: {duration_str}
#     Number of comments: {comment_count}
#     Number of likes: {like_count}
#     Number of views: {view_count}
#     """)


# channel=channels_response.get("items")[0]
# subscriber_count = channel['statistics']['subscriberCount']
# joining_date = channel['snippet']['publishedAt']
# total_views = channel['statistics']['viewCount']
# print(subscriber_count,joining_date,total_views)
# CHANNEL_ID='UCfjTOrCPnAblTngWAzpnlMA'
# # CHANNEL_ID=search_channel_name
# API_SERVICE_NAME = 'youtubeAnalytics'
# API_VERSION = 'v2'

# SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
# CLIENT_SECRETS_FILE = 'client_secret_203437419460-dalavogmhgdkfis3c4ferii6qi698ca8.apps.googleusercontent.comp'
# def get_service():
#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#     credentials = flow.run_console()
#     return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# youtubeAnalytics = get_service()
from google_auth_oauthlib.flow import InstalledAppFlow
from analytix.youtube import YouTubeAnalytics, YouTubeService

# from analytix import youtube

service = YouTubeService("./secrets.json")  # Load from secrets file
service.authorise()
analytics = YouTubeAnalytics(service)
report = analytics.retrieve(dimensions=("day",))
report.to_csv("./analytics-28d.csv")
# analytics_request = youtube.reports().query(
#     ids="channel==" + "UCbmNph6atAoGfqLoCL_duAg",
#     startDate=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
#     endDate=datetime.now().strftime("%Y-%m-%d"),
#     metrics="viewerPercentage",
#     dimensions="day",
#     sort="day",
# )
