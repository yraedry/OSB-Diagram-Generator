from abc import ABC, abstractmethod

class BusinessInterface(ABC):
    @abstractmethod
    def get_name(self, business_name):
        pass
    @abstractmethod
    def get_uri(self, business_file):
        pass
    @abstractmethod
    def get_type(self, business_file):
        pass

    