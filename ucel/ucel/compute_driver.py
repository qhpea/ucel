from abc import ABC, abstractmethod

class ComputeDriver(ABC):
    @abstractmethod
    def get_status(self):
        "Get the status of this compute"
        pass
    
    @abstractmethod
    def get_connectivity(self):
        "get ports for this"

    @abstractmethod
    def stop(self):
        "stop this compute"

    @abstractmethod
    def remove(self):
        "remove this compute"
    
    @abstractmethod
    def restart(self):
        "restart this compute"
    
    def start_task(self, task):
        pass

    def tick(self):
        "Update this compute driver"
        # check for commands
        # look for new jobs