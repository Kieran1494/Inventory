import os
import sys

import pandas as pd


class Database:
    _log_data = ()
    _item_attributes = ()
    _data = pd.DataFrame
    _log = {}

    def __init__(self, log_data, item_attributes):
        """
        load data to ram and column headers
        :param log_data: tuple or list of log data headers
        :param item_attributes: tuple or list of item attributes
        """
        self._log_data = log_data
        self._item_attributes = item_attributes
        self._data = read(item_attributes, "data.csv")
        self._log = read(log_data, "log.xlsx")
        if self._log == {}:
            for i in range(self._data.shape[0]):
                self._log[str(i)] = pd.DataFrame(columns=self._log_data)

    def write(self, name):
        """
        Writes data to file
        if the file is a csv it writes item database
        if the file is a xlsx it writes log
        :param name: file name
        """
        # get file extension
        ext = os.path.splitext(name)[1]
        # write appropriate way
        if ext == ".csv":
            self._data.to_csv(name, header=True, index=False)
        elif ext == ".xlsx":
            writer = pd.ExcelWriter(name)
            for sheet, frame in self._log.items():
                frame.to_excel(writer, sheet_name=sheet, index=False)
            writer.save()
        else:
            print("INVALID FILE NAME")

    def add(self, item):
        """
        add item to database and write new database
        :param item: item to add
        """
        # convert dict to dict of lists
        for key in item.keys():
            item[key] = [item[key]]
        # add hidden id
        item["hidden"] = str(self._data.shape[0])
        # add dataframe to log database for item
        self._log[item["hidden"]] = pd.DataFrame(columns=self._log_data)
        # convert dict to database
        itm = pd.DataFrame(item)
        # add to database
        self._data = pd.concat([self._data, itm], axis=0)
        # write
        self.write("data.csv")
        self.write("log.xlsx")

    def get_selected(self, item_ID):
        """
        get information to display for item checkout or history
        :param item_ID: hidden id of item
        :return important display info
        """
        # grab row with id
        row = self._data.loc[self._data['hidden'].isin([item_ID])]
        # convert to list and return important info
        row = row.values.tolist()[0]
        return row[:4]

    def items(self):
        """
        return all items in database for display
        :return all items in database
        """
        return {"items": self._data.to_dict('records')}

    def log(self, transaction, hidden):
        """
        log new transaction
        :param transaction: information from post in dict from
        :param hidden: hidden id of item being checked out
        """
        # make data frame for checkout
        frame = pd.DataFrame([transaction], columns=transaction.keys())
        frame.columns = self._log_data
        # add to log for that item
        self._log[hidden] = pd.concat([self._log[hidden], frame], axis=0)
        # write
        self.write("log.xlsx")

    def get_log(self, hidden):
        """
        get all transactions for an item
        :param hidden: hidden id for the item
        :return listified dicts of log info
        """
        return {"items": self._log[hidden].to_dict('records')}

    def add_esc(self, new, hidden_ID):
        """
        adds an existing item
        :param new: new item info
        :param hidden_ID: id
        """
        # get row for id and convert to dict
        row = self._data.loc[self._data['hidden'].isin([hidden_ID])]
        row = row.to_dict('records')[0]
        # add all column info transaction does not already have except hidden
        for key in list(row.keys())[:-1]:
            if key not in new.keys():
                new[key] = row[key]
        # add to database
        self.add(new)

    def update_args(self, new_history_args=None, new_param_args=None):
        """
        update column headers
        !!! SHOULD NOT BE USED UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING !!!
        :param new_history_args: new headers for the log
        :param new_param_args: new headers for the items
        """
        if new_param_args is not None:
            self._item_attributes = new_param_args
        if new_history_args is not None:
            self._log_data = new_history_args


def sort_dict(self, **kwargs):
    return tuple(kwargs.get(x, None) for x in kwargs.get("dict"))


def read(headers, name):
    """
    read in data from storage
    if the file is a csv it reads into item database
    if the file is a xlsx it reads into log
    :param headers: column headers
    :param name: file name
    :return dataframe or dict of loaded in data or defaults
    """
    # get whether it is a csv or xlsx
    ext = os.path.splitext(name)[1]
    # change path
    os.chdir(r"C:\Users\Kieran\OneDrive\School\High School\AOS\Science\Senior Research Project\Inventory\Python")
    try:
        # read in files defaults to empty
        if ext == ".csv":
            data = pd.read_csv(name)
        elif ext == ".xlsx":
            data = pd.read_excel(name, sheet_name=None)
        else:
            data = None
        # return full version
        if data is not None:
            return data
        # if nothing was read give defaults
        else:
            if ext == ".csv":
                return pd.DataFrame({head: [] for head in headers})
            elif ext == ".xlsx":
                return {}
            else:
                print("ur gay", file=sys.stdout)
    # manage errors
    except FileNotFoundError:
        if ext == ".csv":
            return pd.DataFrame({head: [] for head in headers})
        elif ext == ".xlsx":
            return {}
        else:
            print("ur gay", file=sys.stdout)
    except PermissionError:
        print("ur mega gay", file=sys.stdout)
