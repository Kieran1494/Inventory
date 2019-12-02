import os
import sys

import pandas as pd


def read(headers, name):
    ext = os.path.splitext(name)[1]
    try:
        if ext == ".csv":
            data = pd.read_csv(name)
        elif ext == ".xlsx":
            data = pd.read_excel(name, sheet_name=None)
        else:
            print("ur gay", file=sys.stdout)
            data = None
        if data is not None:
            return data
        else:
            if ext == ".csv":
                return pd.DataFrame({head: [] for head in headers})
            elif ext == ".xlsx":
                return {}
            else:
                print("ur gay", file=sys.stdout)
    except FileNotFoundError:
        if ext == ".csv":
            return pd.DataFrame({head: [] for head in headers})
        elif ext == ".xlsx":
            return {}
        else:
            print("ur gay", file=sys.stdout)
    except PermissionError:
        return "NO"


class Database:
    _log_data = ()
    _item_attributes = ()
    _data = pd.DataFrame
    _log = {}
    _condition_key = ()
    _matched = None

    def __init__(self, log_data, item_attributes, condition_key):
        self._log_data = log_data
        self._item_attributes = item_attributes
        self._condition_key = condition_key
        self._data = read(item_attributes, "data.csv")
        self._log = read(log_data, "log.xlsx")

    def write(self, name):
        """
        Writes data to file
        :param name: file name
        :param reading_numbers: add a column for reading number
        :return: boolean whether function successfully wrote
        """
        # write file
        ext = os.path.splitext(name)[1]
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
        item = list(item.values())
        item.append(str(self._data.shape[0]))
        self._log[item[len(item) - 1]] = pd.DataFrame(columns=self._log_data)
        itm = pd.DataFrame(item).transpose()
        itm.columns = self._item_attributes
        self._data = pd.concat([self._data, itm], axis=0)
        self.write("data.csv")
        self.write("log.xlsx")

    def get_selected(self, item_ID):
        row = self._data.loc[self._data['hidden'].isin([item_ID])]
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

    def items(self):
        # if self._matched is not None:
        #     matches = self._matched.values.tolist()
        #     alldata = self._data.values.tolist()
        #     alldata = [x for x in alldata if x not in matches]
        #     ordered = matches + alldata
        # else:
        #     ordered = self._data.values.tolist()
        return {"items": self._data.to_dict('records')}
        # for i in range(len(ordered)):
        #     ordered[i][6] = self._condition_key[str(ordered[i][6])]
        # return ordered

    def log(self, transaction):
        frame = pd.DataFrame([transaction], columns=transaction.keys())
        print(frame, file=sys.stdout)
        frame.columns = self._log_data
        print(self._log, file=sys.stdout)
        self._log[self.selected] = pd.concat([self._log[self.selected], frame], axis=0)
        print(self._log, file=sys.stdout)
        self.write("log.xlsx")


def sort_dict(self, **kwargs):
    return tuple(kwargs.get(x, None) for x in kwargs.get("dict"))


def update_args(self, new_history_args=None, new_param_args=None):
    if new_param_args is not None:
        self._item_attributes = new_param_args
    if new_history_args is not None:
        self._log_data = new_history_args
