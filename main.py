from multiprocessing import Process
from data_io.App_Run import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)