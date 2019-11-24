import sqlite3
import sys

import pandas as pd


class Database:
    _history_args = ()
    _param_args = ()
    _data = ""
    _log = ""
    _matched = None
    selected = None

    def __init__(self, history_args, param_args):
        self._history_args = history_args
        self._param_args = param_args
        self._data = self.read(param_args)

    def write(self, name="data.csv", reading_numbers=False):
        """
        Writes data to file
        :param data: data
        :param name: file name
        :param reading_numbers: add a column for reading number
        :return: boolean whether function successfully wrote
        """
        # write file
        self._data.to_csv(name, header=True, index=False)

    def read(self, headers, name="data.csv"):
        try:
            data = pd.read_csv(name)
            if data is not None:
                return data
        except FileNotFoundError:
            return pd.DataFrame({head: [] for head in headers})
        except PermissionError:
            return "NO"


    def add(self, item):
        itm = pd.DataFrame([item], columns=item.keys())
        itm.columns = self._param_args
        self._data = pd.concat([self._data, itm], axis=0)
        self.write()

    def search(self, terms):
        terms = terms.lower().replace(" ", "").split(",")
        matched = []
        for index, item in self._data.iterrows():
            for term in terms:
                if term in [str(x).lower().replace(" ", "") for x in item.values.tolist()]:
                    matched.append(item.values.tolist())
        if matched:
            matched = pd.DataFrame(matched, columns=self._param_args)
            self._matched = matched

    def headers(self):
        headers = []
        for header in self._param_args:
            headers.append(header.capitalize())
        return headers

    def items(self):
        if self._matched is not None:
            matches = self._matched.values.tolist()
            alldata = self._data.values.tolist()
            alldata = [x for x in alldata if x not in matches]
            return matches + alldata
        else:
            return self._data.values.tolist()

    def sort_dict(self, **kwargs):
        return tuple(kwargs.get(x, None) for x in kwargs.get("dict"))

    def update_args(self, new_history_args=None, new_param_args=None):
        if new_param_args is not None:
            self._param_args = new_param_args
        if new_history_args is not None:
            self._history_args = new_history_args
