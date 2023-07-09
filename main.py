from multiprocessing import Process
from data_io.App_Run import app
import nltk
# Download the 'vader_lexicon' package from NLTK for sentiment analysis

# nltk.download('vader_lexicon')
# nltk.download('stopwords')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)