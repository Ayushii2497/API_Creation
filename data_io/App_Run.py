from data_io.yt_api_io import *
from data_io.redis_io import *
from data_io.celery_task_io import perform_youtube_analysis
from data_io.celery_task_io import r_client
import nltk
from flask import Flask, request, jsonify
from multiprocessing import Process
from data_io.url_check import *

app = Flask(__name__)

# Download the 'vader_lexicon' package from NLTK for sentiment analysis
nltk.download('vader_lexicon')

@app.route("/getChannelDetails", methods=['GET', 'POST'])
def getChannelDetails():
    # channel_name = request.args.get('channel')
    data = request.get_json()
    link = data.get('Link')
    channel_name=check_url(link)
    if channel_name[:1]=='@':
        channel_name=channel_name[1:]
        
    if channel_name==None:
        response = jsonify({"body":"Invalid Input"})
        response.status_code = 400
        return response    
    else:
        resp_info = r_client.get_info(channel_name)
        print(resp_info)
        if resp_info and resp_info["Status"] != "Processing data":
            return jsonify(resp_info), 200
        
        elif resp_info and resp_info["Status"] == "Processing data":
                response = jsonify({"body": "Processing data"})
                response.status_code = 200
                return response
        else:
            r_client.insert_wait_state(channel_name)
            backend_process = Process(
                target=perform_youtube_analysis,
                args=(channel_name,),
                daemon=True
            )
            backend_process.start()

            response = jsonify({"body": "Processing data"})
            response.status_code = 200

            return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
