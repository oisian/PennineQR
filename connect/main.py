import requests
import socket
from connect import webServer
import time
from threading import Thread
from collections import deque


class connection:
    def __init__(self):
        self.server = 'http://localhost'
        self.ip = self.get_ip_address()
        self.requests = deque()
        self.stopped = False

    def start(self):
        mydata=[('IP', self.ip)]
        r = self.send_data("/StockMovement/Create_Terminal", mydata)

        Thread(target=self.loop, args=()).start()
        return self

    def loop(self):

        while True:
            if self.stopped:
                return
            if len(self.requests) > 0:
                i = self.requests.popleft()
                r = self.send_data("/StockMovement/receive_code", i)
                print(r.content)


    def disconnect(self):
        #post request to server that pi should be disconnected
        pass

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.0.42", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def heartbeat(self):
        #intercept heartbeat from server
            #respond with ack if still alive
            #else
            #kill connection
        pass

    def send_data(self,path , data):
        url = self.server + path
        print(url, data)
        return requests.post(url, data, allow_redirects=False)


