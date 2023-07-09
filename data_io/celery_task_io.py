from celery import Celery
from data_io.yt_api_io import *
from data_io.redis_io import *
import time

# Create a Celery instance
celery = Celery(
    'youtube_api',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
# Create an instance of th.e Youtube_API class
yt_obj = Youtube_API()

#instantite the redis server
r_client = Redis_IO()

@celery.task
def perform_youtube_analysis(channel_name):
    # Perform YouTube analysis and other time-consuming tasks here
    channel_name = ''.join(channel_name)
    # Retrieve and print the channel data for
    channel_data = yt_obj.channel_respose(channel_name)
    if channel_data:
        print(channel_data)
        
        # Retrieve audience response (uncommented line)
        # audience_resp = yt_obj.audience_response()

        # Make a request for demographics data (uncommented line)
        # yt_obj.demographics_request()

        # Make a request for comments data
        yt_obj.comments_request()

        # Perform sentiment analysis
        senti_score = yt_obj.sentiment_analyse()
        print(f"The Sentiment score obtained - {senti_score}")

        #Get latest videos information
        video_resp=yt_obj.top_videos_info(channel_name)
        channel_data.update(video_resp)
        
        channel_data.update(
            {"Status" : "Processed",
            "Timestamp" : str(int(time.time()))}
        )
        
        r_client.insert_info(channel_name, channel_data)
        print("Data inserted into redis")
        return 
    
    channel_data = (
            {"Status" : "Channel not found",
             "Channel Name" : channel_name,
            "Timestamp" : str(int(time.time()))}
        )
    r_client.insert_info(channel_name, channel_data)
    print("Data inserted into redis")