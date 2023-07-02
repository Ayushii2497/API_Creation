from urllib.request import urlopen
import json
import nltk
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

key='AIzaSyA8LYPKSMyLyIwwKDCeYsnrfDmz9dGmenk'
no_of_latest_videos = 10
no_of_latest_comments = 100
sentiment_analyzer = SentimentIntensityAnalyzer()

    
def main():
    channel_user_name=str(input('Input Username : ' )).split()
    # channel_user_name='tseries'
    print ("Channel User Name", channel_user_name)
    url_encode_channel_user_name='%20'.join([str(ele) for ele in channel_user_name])
    search_result=urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+url_encode_channel_user_name +'&type=channel&key='+key)
    search_result_json = json.load(search_result)
    print (search_result_json)
    ucid=str(search_result_json.get("items")[0].get("id").get('channelId'))
    channelname=search_result_json.get("items")[0].get("snippet").get('title')
    joindate=search_result_json.get("items")[0].get("snippet").get('publishTime')
    print ("UCID", ucid)
    print ("Channel Name", channelname)
    print ("Join Date", joindate)

    channel_data=urlopen('https://www.googleapis.com/youtube/v3/channels?id='+ucid+'&key='+key+'&part=snippet,contentDetails,statistics,status')
    channel_data_json = json.load(channel_data)
    subs = int(channel_data_json.get("items")[0].get("statistics").get("subscriberCount"))
    videoCount = int(channel_data_json.get("items")[0].get("statistics").get("videoCount"))
    viewCount = int(channel_data_json.get("items")[0].get("statistics").get("viewCount"))
    upload_id = channel_data_json.get("items")[0].get("contentDetails").get("relatedPlaylists").get("uploads")
    print ('Subscriber', subs)
    print ('video count', videoCount)
    print ('viewCount', viewCount)
    print ('upload_id', upload_id)

    video_list = []
    latest_videos=urlopen('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='+upload_id+'&maxResults='+str(no_of_latest_videos)+'&key='+key)
    latest_videos_json = json.load(latest_videos)
    video_items = latest_videos_json.get('items')
    for video_item in video_items:
        title = video_item.get('snippet').get('title')
        description = video_item.get('snippet').get('description')
        videoId = video_item.get('snippet').get('resourceId').get('videoId')
        publishedAt = video_item.get('snippet').get('publishedAt')
        latest_comments=urlopen('https://www.googleapis.com/youtube/v3/commentThreads?key='+key+'&textFormat=plainText&part=snippet&videoId='+videoId+'&maxResults='+str(no_of_latest_comments))
        latest_comments_json = json.load(latest_comments)
        
        comment_items = latest_comments_json.get('items')
        sentiments = []
        for item in comment_items:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment_scores = sentiment_analyzer.polarity_scores(comment_text)
            sentiment = sentiment_scores['compound']
            sentiments.append(sentiment)
        sentiment_score = round (sum(sentiments) / len(sentiments) if sentiments else 0, 3)
        print (title, ':', sentiment_score)
        video_list.append({'title': title, 'description': description, 'videoId': videoId, 'publishedAt': publishedAt, 'sentiment_score': sentiment_score })


if __name__ == '__main__':
    main()