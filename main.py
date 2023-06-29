from data_io.yt_api_io import *
import nltk

# Download the 'vader_lexicon' package from NLTK for sentiment analysis
nltk.download('vader_lexicon')

# Create an instance of the Youtube_API class
yt_obj = Youtube_API()

# Retrieve and print the channel data for "atgoogletalks"
channel_data = yt_obj.channel_respose("atgoogletalks")
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

