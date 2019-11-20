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

    def _convertDictToTuple(self, **kwargs):
        '''
        Uses key word arguments to take an unordered dict and return an ordered tuple

        args: unpacked dict
        returns: tuple
        '''
        return tuple(kwargs.get(x, None) for x in kwargs.get("dict"))


    def sortData(self, idict):
        '''
        Takes raw URL input and converts it to a tuple

        args: idict (dict) (dictionary to look at for arguments)
        returns: tuple
        '''
        args = "BULL SHIT"
        return self._convertDictToTuple(dict = idict, **args)

    def do_POST(self):
        """
        formal POST method
        required by http module to handle POST requests
        """
        if self.path == "submit_data":
            sortedData = self.sortData(PARAM_ARGS)
            updateDB(sortedData)

        elif self.path == "req_trans":
            hData = self.sortData(HISTORY_ARGS)
            requestDB(hData)



class ThreadHandler(ThreadingMixIn, HTTPServer):
    pass

def requestDB(hData):
    '''
    Handles request to make transaction

    args: hData (tuple) | tuple for data to go to history table
    returns: none
    '''
    db = sqlite3.connect("inventory.db")
    c = db.cursor()

    try:
        f = open("log.txt", 'r')
    except:
        f = open("log.txt", 'w')
    finally:
        f.close()
        f = open("log.txt", 'a')

    rto = [x for x in c.execute("SELECT rto FROM history WHERE id='" + str(hData[0]) + "'")][0][0]
    rfrom = [x for x in c.execute("SELECT rfrom FROM history WHERE id='" + str(hData[0]) + "'")][0][0]
    tin = [x for x in c.execute("SELECT tin FROM history WHERE id='" + str(hData[0]) + "'")][0][0]
    tout = [x for x in c.execute("SELECT tout FROM history WHERE id='" + str(hData[0]) + "'")][0][0]

    # print(rto, rfrom, tin, tout)
    f.write(str(rto) + " " + str(rfrom) + " " + str(tin) + " " + str(tout) + "\n")

    insertData = "".join([HISTORY_ARGS[hData[1:].index(x)] + "='" + str(x) + "', " if hData.index(x) != len(hData) - 1 else HISTORY_ARGS[hData[1:].index(x)] + "='" + str(x) + "'" for x in hData[1:]])

    c.execute("UPDATE history SET " + insertData + " WHERE id='" + hData[0] + "'")

    db.commit()
    c.close()

def updateDB(data):
    '''
    Updates the DB with new data

    args: data (tuple)
    returns: nix
    '''
    db = sqlite3.connect("inventory.db")
    c = db.cursor()

    c.execute("INSERT INTO data VALUES (" + "?, " * (len(PARAM_ARGS) - 1) + "?)", data)
    c.execute("INSERT INTO history VALUES (" + "?, " * (len(HISTORY_ARGS) - 1) + "?)", (data[0], None, data[4], None, None))

    #do stuff with data here for archival purposes

    db.commit()
    c.close()

def checkDB():
    '''
    Checks DB for presence of tables, appending them if nonexistant

    args: nix
    returns: nix
    '''
    db = sqlite3.connect("inventory.db")
    c = db.cursor()

    hasTables = len([x for x in c.execute("SELECT * FROM sqlite_master WHERE type='table'")]) > 1

    if not hasTables:
        c.execute("CREATE TABLE data (" + ", ".join(PARAM_ARGS) + ")")
        c.execute("CREATE TABLE history (" + ", ".join(HISTORY_ARGS) + ")")

    db.commit()
    c.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    IP = "0.0.0.0"

    Port = 80

    PARAM_ARGS = ("id", "name", "make", "model", "room", "teacher", "condition", "desc", "moveable", "manual")
    HISTORY_ARGS = ('id', 'rto', 'rfrom', 'tin', 'tout')

    # updateDB(PARAM_ARGS)
    # requestDB(HISTORY_ARGS)

    checkDB()

    httpd = ThreadHandler((IP, Port), Serve)
    httpd.serve_forever()
