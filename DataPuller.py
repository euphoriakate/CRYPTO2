from abc import ABCMeta
import requests


class DataPuller:
    __metaclass__ = ABCMeta

    def json_data_obtain(self, url, param=None):
        return requests.get(url=url, params=param).json()

    def xml_data_obtain(self):
        pass
