# nltk.download('vader_lexicon')

# import redis
from googleapiclient.discovery import build
import re
# from datetime import datetime, timedelta
# dict={"status":"ABC","timestamp":"","channel_name":"","channel_user_name":"","subscriber_count":"","views":"","join_date":"","Parsed_email_ids":"","latest_videos":""}
# redisClient = redis.Redis(host='localhost', port=6379, db=0)
# redisClient.mset(dict)
import requests
import json
from nltk.sentiment import SentimentIntensityAnalyzer
# # print(redisClient.get("status"))
# # youtube = build('youtube', 'v3', credentials=creds)
youtube1 = build('youtube', 'v3',developerKey='AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk')
# # search_channel_name = 'atgoogletalks'
search_channel_name="tseries"

# channels_response = youtube1.channels().list(
#         forUsername=search_channel_name,
#         part="id, snippet, statistics, contentDetails, topicDetails,"
# ).execute()
# channel_data=channels_response.get("items")[0]
# print(channel_data)
# # print(channels_response['items'][0]['id'])
# CHANNEL_ID='UCfjTOrCPnAblTngWAzpnlMA'
CHANNEL_ID='UCq-Fj5jknLsUf-MWSy4_brA'
dv_key='AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk'
video_url= f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&maxResults=10&order=date&type=video&key={dv_key}"

json_url = requests.get(video_url)
data = json.loads(json_url.text)
# items=data.get("items")[0]
# retrieve youtube video results 

lst=[]
replygre=[]
likesmore=[]
normal=[]
for ele in data['items']:
        vid_id=ele['id']['videoId']
        video_request=youtube1.videos().list(
        part='snippet,statistics',
        id=vid_id
        )
        video_response = video_request.execute()
        # print(video_response)
        # print(video_response)
        des = video_response['items'][0]['snippet']['description']
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(des))
        # print(emails)
        comment_count = video_response['items'][0]['statistics']['commentCount']
        # print(comment_count)
        video_response_2=youtube1.commentThreads().list(
        part='snippet,replies',
        videoId=vid_id
        ).execute()
        # sentiment_analyzer = SentimentIntensityAnalyzer()
        # sentiments = []
        # latest_Video=[]
        # channel_title=video_response['items'][0]['snippet']['channelTitle']
        # title=video_response['items'][0]['snippet']['title']
        # # print(channel_title[0])

        for i in video_response_2['items']:
                comment=i['snippet']['topLevelComment']['snippet']['textDisplay']
                # print(i['snippet']['topLevelComment']['snippet'])
        #         sentiment_scores = sentiment_analyzer.polarity_scores(comment)
        #         sentiment = sentiment_scores['compound']
        #         sentiments.append(sentiment)
        #         emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(comment))
        #         # print (emails)
                # replycount = i['snippet']
                # print(replycount)
                replycount = i['snippet']['totalReplyCount']
                # likecount = i['snippet']['likeCount']
                likes=i['snippet']['topLevelComment']['snippet']['likeCount']
                # print(likes,comment,replycount)
                dic={'likes':likes,"comment":comment,"replycount":replycount} 
                if replycount>0 and likes<replycount:
                        replygre.append(dic)
                elif likes>replycount:
                        likesmore.append(dic)
                elif likes==0 and replycount==0:
                        normal.append(dic)
        from operator import itemgetter
        newlist = sorted(likesmore, key=itemgetter('likes'), reverse=True) 

# for i in newlist:
#         if newlist['replycount']>newlist['likes']
        import itertools
        ab = itertools.chain(replygre,newlist,normal)
# # final=replygre+likesmore+normal
# # # print(final[:10])
        out=list(ab)
        res=out[:10]
        print(res)
# for i in res:
#         print(i['comment'])
# a={'abc':123}
# print(a.get('ab'))


                
                # replies = []
                # if replycount>0:
                   
                #         for reply in i['replies']['comments']:
                #                 reply = reply['snippet']['textDisplay']
                #                 replies.append(reply)
        
                # # print comment with list of reply
                # print(replies, end = '\n\n')
        # sentiment_score = sum(sentiments) / len(sentiments) if sentiments else 0
        # print(sentiment_score)
        # dic=["title":title]
        
        
        
#             # empty reply list
#         #     replies = []
#         # snippet= i["snippet"]
#         # print(snippet["title"])
#         # statistics= i["statistics"]
#         # like_count= statistics["likeCount"]
#         # print(like_count)
#         # print(i)
# #get number of likes:-


# # def video_info(channels_response):
# #     items=channels_response.get("items")[0]
# #     # get the snippet, statistics & content details from the video response
# #     snippet         = items["snippet"]
# #     statistics      = items["statistics"]
# #     content_details = items["contentDetails"]
# #     # get infos from the snippet
# #     # channel_title = snippet["channelTitle"]
# #     title         = snippet["title"]
# #     description   = snippet["description"]
# #     publish_time  = snippet["publishedAt"]
# #     # get stats infos
# #     comment_count = statistics["commentCount"]
# #     like_count    = statistics["likeCount"]
# #     view_count    = statistics["viewCount"]
# #     # get duration from content details
# #     duration = content_details["duration"]
# #     # duration in the form of something like 'PT5H50M15S'
# #     # parsing it to be something like '5:50:15'
# #     parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
# #     duration_str = ""
# #     for d in parsed_duration:
# #         if d:
# #             duration_str += f"{d[:-1]}:"
# #     duration_str = duration_str.strip(":")
# #     print(f"""\
# #     Title: {title}
# #     Description: {description}
# #     Channel Title: {channel_title}
# #     Publish time: {publish_time}
# #     Duration: {duration_str}
# #     Number of comments: {comment_count}
# #     Number of likes: {like_count}
# #     Number of views: {view_count}
# #     """)


# # channel=channels_response.get("items")[0]
# # subscriber_count = channel['statistics']['subscriberCount']
# # joining_date = channel['snippet']['publishedAt']
# # total_views = channel['statistics']['viewCount']

# # print(subscriber_count,joining_date,total_views)
# # CHANNEL_ID='UCfjTOrCPnAblTngWAzpnlMA'
# # # CHANNEL_ID=search_channel_name
# # API_SERVICE_NAME = 'youtubeAnalytics'
# # API_VERSION = 'v2'

# # SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
# # CLIENT_SECRETS_FILE = 'client_secret_203437419460-dalavogmhgdkfis3c4ferii6qi698ca8.apps.googleusercontent.comp'
# # def get_service():
# #     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# #     credentials = flow.run_console()
# #     return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# # youtubeAnalytics = get_service()

# # emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
# # print (emails)
# # from analytix import youtube

# # service = YouTubeService("./secrets.json")  # Load from secrets file
# # service.authorise()
# # analytics = YouTubeAnalytics(service)
# # report = analytics.retrieve(dimensions=("day",))
# # report.to_csv("./analytics-28d.csv")
# # analytics_request = youtube.reports().query(
# #     ids="channel==" + "UCbmNph6atAoGfqLoCL_duAg",
# #     startDate=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
# #     endDate=datetime.now().strftime("%Y-%m-%d"),
# #     metrics="viewerPercentage",
# #     dimensions="day",
# #     sort="day",
# # )
