import requests
import pprint



def get_request(request):
    response = requests.get(request).json()
    return response