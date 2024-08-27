from abc import ABC, abstractmethod

class PipelineInterface(ABC):
    @abstractmethod
    def get_service(self, pipeline_file):
        pass