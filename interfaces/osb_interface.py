from abc import ABC, abstractmethod

class OsbInterface(ABC):
    @abstractmethod
    def get_project_name(self, project_name):
        pass
    @abstractmethod
    def get_proxy_service(self, proxy_service):
        pass
    @abstractmethod
    def get_pipeline(self, pipeline):
        pass
    @abstractmethod
    def get_business_service(self, business_service):
        pass
    