from abc import ABC, abstractmethod

class ProxyInterface(ABC):
    @abstractmethod
    def get_name(self, proxy_name):
        pass
    @abstractmethod
    def get_uri(self, proxy_file):
        pass
    @abstractmethod
    def get_type(self, proxy_file):
        pass
    @abstractmethod
    def get_invoke(self, proxy_file):
        pass
    