import requests


class IDataObtainer:

    def json_data_obtain(self, url):
        return requests.get(url).json()

    def xml_data_obtain(self):
        pass
