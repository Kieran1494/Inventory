import logging
import sys
from flask import Flask, render_template, request

from Database import Database as db

app = Flask(__name__)


@app.route('/')
@app.route("/index", methods=["POST"])
def hello():
    """
    default page display
    """
    return render_template("index.html", data=database.items())


@app.route('/add_item', methods=["POST"])
def add_item():
    """
    add item to database using dict from post
    """
    if request.method == "POST":
        item = request.form.to_dict()
        logging.info(item)
        database.add(item)
    return hello()


@app.route('/search', methods=["POST"])
def search():
    """
    TODO: search for item in database, do in js?
    currently not working
    """
    search = request.form.to_dict()
    return hello()


@app.route('/checkout', methods=["POST"])
def checkout():
    """
    checkout item based on hidden item id from table
    """
    item_ID = request.form.to_dict()["hidden"]
    if item_ID is not None:
        return render_template("checkout.html", item=database.get_selected(item_ID),
                               location=database.get_current_loc(item_ID))
    else:
        return hello()


@app.route('/checkout_item', methods=["POST"])
def checkout_item():
    """
    log checkout of item using form info
    """
    info = request.form.to_dict()
    hidden = info["hidden"]
    log = dict()
    for key, value in info.items():
        if "hidden" not in str(key):
            log[key] = value
    database.log(log, hidden)
    return hello()


@app.route('/history', methods=["POST"])
def history():
    """
    display item's log history
    """
    item_ID = request.form.to_dict()["hidden"]
    if item_ID is not None:
        return render_template("history.html", item=database.get_selected(item_ID), log=database.get_log(item_ID))
    else:
        return hello()


@app.route('/remove', methods=["POST"])
def remove():
    """
    TODO: remove item from database
    currently not working
    """
    item = request.form.to_dict()
    return "True"


@app.route('/add_esx', methods=["POST"])
def add_esx():
    """
    currently not working
    """
    item_ID = request.form.to_dict()["hidden"]
    return render_template("add_another.html", item=database.get_selected(item_ID)[:3])


@app.route('/add_another', methods=["POST"])
def add_another():
    """
    currently not working
    """
    addition = request.form.to_dict()
    item_ID = addition["hidden"]
    info = dict()
    for key, value in addition.items():
        if "hidden" not in str(key):
            info[key] = value
    database.add_esc(info, item_ID)
    return hello()


if __name__ == '__main__':
    item_attributes = (
        "name", "make", "model", "ID", "room", "teacher", "condition", "manual", "movable", "description", "hidden")
    log_values = ('name', 'to', 'from', 'tout', 'tin')
    database = db(log_values, item_attributes)
    app.run(host='0.0.0.0', port=8000, debug=True)
    print("", file=sys.stdout)
