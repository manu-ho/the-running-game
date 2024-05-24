import abc


class BaseProcessor(abc.ABC):
    @abc.abstractmethod
    def process(self, data: dict) -> dict:
        pass
