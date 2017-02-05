#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        if(port==None):
            port = 80

        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        parts = data.split("\r\n\r\n")
        statusCode = parts[0].split()[1]
        return int(statusCode)

    def get_headers(self,data):
        return None

    def get_body(self, data):
        bodyData = data.split("\r\n\r\n")[1]
        return bodyData

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def makeRequest(self, method, parsedURL, args=None):
        request = ""
        request = (method + " " + str(parsedURL.path) + " HTTP/1.1\r\n" 
        + "HOST: " + str(parsedURL.hostname) + "\r\n" 
        + "Connection: close\r\n" 
        + "Accept: */*\r\n"
        )

        if(method == "GET"):
            request = request + "\r\n"
        else:
            if(args == None):
                args = ""
            request = (request + "Content-Type: application/x-www-from-urlencoded,application/json; \r\n" 
            + "Content-Length: " + str(len(args)) 
            + "\r\n\r\n" + args
            )

        return request

    def GET(self, url, args=None):
        parsedURL = urlparse(url)
        request = self.makeRequest("GET", parsedURL)
        socket = self.connect(parsedURL.hostname, parsedURL.port)
        socket.sendall(request)
        response = self.recvall(socket)
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        parsedURL = urlparse(url)
        if(args):
            encoded = urllib.urlencode(args)
        else:
            encoded = ""
        request = self.makeRequest("POST", parsedURL, encoded)
        socket = self.connect(parsedURL.hostname, parsedURL.port)
        socket.sendall(request)
        response = self.recvall(socket)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
