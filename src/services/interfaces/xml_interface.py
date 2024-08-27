from abc import ABC, abstractmethod

class XmlInterface(ABC):
    @abstractmethod
    def get_path_repositories(self):
        pass
    @abstractmethod
    def get_path(self, repo, file_type):
        pass
    @abstractmethod
    def get_file_path(self, path, file_type):
        pass