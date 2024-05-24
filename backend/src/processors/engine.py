from functools import lru_cache
from typing import Mapping, Type

from src.processors.base import BaseProcessor
from src.utils import get_all_subclasses


class ProcessorEngine:

    def __init__(self):
        self._processors = ProcessorEngine._find_all_processors()

    def run(self, data: dict, processor: str | Type[BaseProcessor]) -> dict:
        if isinstance(processor, str):
            processor = self._processors.get(self._processors, None)
        if processor is None:
            raise ValueError(
                f"Error running processor. Could not load processor of type "
                f"{processor}. Available processor implementations are "
                f"{self._processors.keys()}"
            )
        return processor().process(input=data)

    @lru_cache(1)
    @staticmethod
    def _find_all_processors() -> Mapping[str, Type[BaseProcessor]]:
        processors = {}
        subclasses = get_all_subclasses(BaseProcessor)
        for processor in subclasses:
            registry_key = str(processor.__class__.__name__).split(".")[-1]
            processors[registry_key] = processor
        return processors
