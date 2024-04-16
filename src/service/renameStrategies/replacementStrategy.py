from abc import ABC, abstractmethod

class ReplacementStrategy(ABC):

    @abstractmethod
    def getVariableName(self):
        pass

    @abstractmethod
    def getFunctionName(self):
        pass

    @abstractmethod
    def getStringReplacer(self):
        pass