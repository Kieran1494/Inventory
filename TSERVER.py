from glob import glob
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, sys, time, requests
from socketserver import ThreadingMixIn
import threading
from multiprocessing import Process
import sqlite3


class Serve(BaseHTTPRequestHandler):
    def validate(self, ip):
        """
        checks if ip can access site

        args: ip
        returns: boolean
        """

        pass

    def getValidFiles(self):
        """
        gives all valid file paths in the folder(s)

        returns: all valid path urls (list)
        """
        okPaths = [
            ".html",
            ".png",
            ".css",
            ".jpg",
            ".gif",
            ".ico",
            ".js",
            ".php",
            ".pdf"
        ]
        final = []

        for path in okPaths:
            final.append(glob("[!~$]*." + path))

        return final

    def getpage(self):
        """
        does the get method

        args: nix
        returns: nix
        """

        small = self.path.lower()
        validfiles = self.getValidFiles()

        main_page = "/index"
        if small == main_page + ".html" or small == main_page or small == "/":
            # return the index page
            self.send_response(200)
            self.end_headers()
            self.wfile.write(open("index.html", 'rb').read())
            return True

        elif self.path[1:] in validfiles or self.path[1:] + ".html" in validfiles:
            # gets a file if it is defined as accesible through getValidFiles()
            try:
                opener = validfiles[validfiles.index(self.path[1:])]
            except FileNotFoundError:
                opener = validfiles[validfiles.index(self.path[1:] + ".html")]

            f = open(opener, 'rb')
            t = f.read()
            f.close()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(t)
            return t

        else:
            # return 404 - file not found
            print("FUCK")
            did404 = True
            f = "404 file not found<br>fuck off<br><img " \
                "src='https://i.pinimg.com/originals/2b/d2/4d/2bd24db551316d5694321317c26fa69a.jpg'/> "
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f.encode())
            return f

    def formatError(self, ip):
        """
        formats an error message

        args: ip
        returns: error message as str
        """

        pass

    def errorPage(self):
        """
        writes an error page

        returns: nothing
        """

        pass

    def do_GET(self):
        """
        formal GET method for http module

        checks if ip is valid then writes page
        else write error page
        """

        ip = self.address_string()
        valid = self.validate(ip)
        errorString = self.formatError(ip)

        if valid:
            self.getpage()

        else:
            print(errorString)
            self.errorPage()

    def replace(self, string, replacelist=None):

        """
        -= Does NOT overwrite the default replace() method (this is called with self.replace(args*)) =-

        replaces all parts of the string that are in replacelist

        args:
            string - string to be replaced
            replacelist (key arg) - dict of {word to replace: replacement word}

        returns: replaced string
        """
        if not replacelist:
            replacelist = {
                "%0D%0A": "\n",
                "+": " ",
                "%22": "\"",
                "%25": "%",
                "%2E": ".",
                "%2D": "-",
                "%3F": "?",
                "%2C": ",",
                "%92": "'",
                "%3B": ";",
                "%28": "(",
                "%29": ")",
                "%26": "&",
                "%93": "\"",
                "%94": "\"",
                "%3A": ":",
                "%2F": "/",
                "%21": "!",
                "%23": "#",
                "%40": "@",
                "%3C": "&lt;",
                "%3E": "&gt;",
                "%3D": "=",
                "%27": "'",
                "%20": " "
            }
        for key in replacelist:
            string = string.replace(key, replacelist.get(key))
        return string

    def do_POST(self):
        """
        formal POST method
        required by http module to handle POST requests
        """
        pass


class ThreadHandler(ThreadingMixIn, HTTPServer):
    pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    IP = "0.0.0.0"

    Port = 80

    httpd = ThreadHandler((IP, Port), Serve)
    httpd.serve_forever()
