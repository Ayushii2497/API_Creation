from data_io.yt_api_io import *
from data_io.redis_io import *
from data_io.celery_task_io import perform_youtube_analysis
from data_io.celery_task_io import r_client
from data_io.url_check import *
import nltk
from flask import Flask, request
from flask import Response
from flask import jsonify
app = Flask(__name__)

# # # Download the 'vader_lexicon' package from NLTK for sentiment analysis
nltk.download('vader_lexicon')

@app.route("/getChannelDetails", methods=['GET','POST'])
def getChannelDetails():
    channel_name = request.args.get('channel')
    #Newly added
    # output=url_check.check_url(link)
    # if output==None:
    #     response = jsonify({"body":"Invalid Input"})
    #     response.status_code = 400
    resp_info = r_client.get_info(channel_name)
    if resp_info:
        response = jsonify(resp_info)
        response.status_code = 200
        return resp_info
    else:

        # Perform data extraction in the background
        task = perform_youtube_analysis(channel_name)
        print("task_id-",task)

        response = jsonify({"body":"Processing data"})
        response.status_code = 200

        return response
        # return channel_data
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)