import logging
import sys

from flask import Flask, render_template, request
from Database import Database as db

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html", data=database.items())


@app.route('/add_item', methods=["POST"])
def add_item():
    if request.method == "POST":
        item = request.form.to_dict()
        logging.info(item)
        database.add(item)
    return hello()


@app.route('/search', methods=["POST"])
def search():
    search = request.form.to_dict()
    database.search(search["Search"])
    return hello()


@app.route('/checkout', methods=["POST"])
def checkout():
    item_ID = request.form.to_dict()["hidden"]
    if item_ID is not None:
        return render_template("checkout.html", item=database.get_selected(item_ID))
    else:
        return hello()


@app.route('/checkout_item', methods=["POST"])
def checkout_item():
    log = request.form.to_dict()
    print(log, file=sys.stdout)
    database.log(log)
    return hello()


@app.route('/view_history', methods=["POST"])
def history():
    item = request.form.to_dict()
    selection = item["id"]
    database.selected = selection
    return "True"


@app.route('/remove_item', methods=["POST"])
def remove():
    item = request.form.to_dict()
    selection = item["id"]
    database.selected = selection
    return "True"


@app.route('/add_esx', methods=["POST"])
def add_another():
    item = request.form.to_dict()
    selection = item["id"]
    database.selected = selection
    return "True"


if __name__ == '__main__':
    item_attributes = (
        "name", "make", "model", "ID", "room", "teacher", "condition", "manual", "movable", "description", "hidden")
    log_values = ('name', 'to', 'from', 'tout', 'tin')
    condition_key = {"1": "Very Bad",
                     "2": "Bad",
                     "3": "OK",
                     "4": "Good",
                     "5": "Very Good"}
    database = db(log_values, item_attributes, condition_key)
    app.run(host='0.0.0.0', port=8000, debug=True)
