import sys

import pandas as pd


def read(headers, name="data.csv"):
    try:
        data = pd.read_csv(name)
        if data is not None:
            return data
        else:
            return pd.DataFrame({head: [] for head in headers})
    except FileNotFoundError:
        return pd.DataFrame({head: [] for head in headers})
    except PermissionError:
        return "NO"


class Database:
    _log_data = ()
    _item_attributes = ()
    _data = pd.DataFrame
    _log = pd.DataFrame
    _condition_key = ()
    _matched = None
    selected = None

    def __init__(self, log_data, item_attributes, condition_key):
        self._log_data = log_data
        self._item_attributes = item_attributes
        self._condition_key = condition_key
        self._data = read(item_attributes)

    def write(self, name="data.csv", reading_numbers=False):
        """
        Writes data to file
        :param name: file name
        :param reading_numbers: add a column for reading number
        :return: boolean whether function successfully wrote
        """
        # write file
        self._data.to_csv(name, header=True, index=False)

    def add(self, item):
        item = list(item.values())
        item.append(str(self._data.shape[0]))
        itm = pd.DataFrame(item).transpose()
        itm.columns = self._item_attributes
        self._data = pd.concat([self._data, itm], axis=0)
        self.write()

    def get_selected(self):
        row = self._data.loc[self._data['hidden'].isin([self.selected])]
        row = row.values.tolist()[0]
        return row[:4]

    def search(self, terms):
        terms = terms.lower().replace(" ", "").split(",")
        matched = []
        for index, item in self._data.iterrows():
            for term in terms:
                if term in [str(x).lower().replace(" ", "") for x in item.values.tolist()]:
                    matched.append(item.values.tolist())
        if matched:
            matched = pd.DataFrame(matched, columns=self._item_attributes)
            self._matched = matched

    def headers(self):
        headers = []
        for header in self._item_attributes:
            headers.append(header.capitalize())
        return headers

    def items(self):
        if self._matched is not None:
            matches = self._matched.values.tolist()
            alldata = self._data.values.tolist()
            alldata = [x for x in alldata if x not in matches]
            ordered = matches + alldata
        else:
            ordered = self._data.values.tolist()
        for i in range(len(ordered)):
            ordered[i][6] = self._condition_key[str(ordered[i][6])]
        return ordered


def sort_dict(self, **kwargs):
    return tuple(kwargs.get(x, None) for x in kwargs.get("dict"))


def update_args(self, new_history_args=None, new_param_args=None):
    if new_param_args is not None:
        self._item_attributes = new_param_args
    if new_history_args is not None:
        self._log_data = new_history_args
