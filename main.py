from data_io.yt_api_io import *
import nltk
from flask import Flask, request
from flask import Response
from flask import jsonify
app = Flask(__name__)

# # # Download the 'vader_lexicon' package from NLTK for sentiment analysis
nltk.download('vader_lexicon')

@app.route("/getChannelDetails", methods=['GET','POST'])
def getChannelDetails():
    req = request.json
    channel_link=req["Link"]
    
    # Create an instance of th.e Youtube_API class
    yt_obj = Youtube_API()

    # # Retrieve and print the channel data for "atgoogletalks"
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
    
    response = jsonify(channel_data)
    response.status_code = 200
    return response
    # return channel_data
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)