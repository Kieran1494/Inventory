#http, beautiful soup, requests, latter 2 for client?

#read about creating a server -- you have no clue :^(

from http.server import BaseHTTPRequestHandler, HTTPServer
import os, sys, time
from socketserver import ThreadingMixIn
import threading



class Serve(BaseHTTPRequestHandler):
    allData = ""
    rightArnow = "%3C"
    leftArnow = "%3E"

    def do_GET(self):
        did404 = False
        opener = "index.html"

        os.chdir(os.path.abspath(os.path.dirname(__file__)))

        try:
            print(self.path)
            if self.path == "/":
                self.path = "/index.html"

            with open(self.path[1:], 'rb') as f:
                t = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(t)
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 FILE NOT FOUND")
            

class ThreadHandler(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    IP = "0.0.0.0"

    Port = 80

    httpd = ThreadHandler((IP, Port), Serve)
    httpd.serve_forever()
    
    