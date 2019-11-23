import json
import logging
import sys

from flask import Flask, render_template, request
from Database import Database as db

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", headers=database.headers(), items=database.items(), )


@app.route('/add_item', methods=["POST"])
def add_item():
    if request.method == "POST":
        item = request.form.to_dict()
        logging.info(item)
        database.add(item)
    return hello()


@app.route('/history', methods=["POST"])
def log():
    log = request.form.to_dict()
    database.requestDB(log)
    return hello()


@app.route('/search', methods=["POST"])
def search():
    search = request.form.to_dict()
    database.search(search["Search"])
    return hello()


@app.route('/select_item', methods=["POST"])
def select():
    item = request.form.to_dict()
    print(item, file=sys.stdout)
    selection = item["id"]
    database.selected = selection
    return "True"


if __name__ == '__main__':
    PARAM_ARGS = ("name", "make", "model", "ID", "room", "teacher", "condition", "movable", "manual", "description")
    HISTORY_ARGS = ('id', 'rto', 'rfrom', 'tin', 'tout')
    database = db(HISTORY_ARGS, PARAM_ARGS)
    app.run(host='0.0.0.0', port=8000, debug=True)
