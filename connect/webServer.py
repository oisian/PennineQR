from flask import Flask, request
from threading import Thread

class server:
    def __init__(self):
        self.app = app = Flask(__name__)
        self.stopped = False
        self.reponce = None

    def start(self):
        Thread(target=self.app.run(), args=()).start()
        return self

    def read(self):
        return self.reponce

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True



app = Flask(__name__)

@app.route('/api/heartbeat', methods=['POST'])
def parse_request():
    print(request.method)
    if request.method == 'POST':
        jsonData = request.get_json()

        requestType = jsonData['RequestType']

        print(jsonData['customer'])
    else:
        return False


if __name__ == '__main__':
    app.run()