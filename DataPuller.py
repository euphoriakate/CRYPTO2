from abc import ABCMeta, abstractmethod
import requests


class DataPuller:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_request(self, request):
        response = requests.get(request).json()
        return response

'''
class Animal:
    __metaclass__ = ABCMeta

    @abstractmethod
    def say_something(self): pass

class Cat(Animal):
    def say_something(self):
        return "Miauuu!"
'''