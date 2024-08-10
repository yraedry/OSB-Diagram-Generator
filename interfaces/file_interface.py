from abc import ABC, abstractmethod

class FileInterface(ABC):
    @abstractmethod
    def get_content_file(self, path, file_name):
        pass