from abc import ABC, abstractmethod

from model.curve.ipdata import IPdata

class CurveDATABuilder(ABC):
    """추상 곡선데이터 빌더"""
    @abstractmethod
    def build(self, data, brokenchain) -> list[IPdata]:
        raise NotImplementedError

    @abstractmethod
    def preprocess(self, data, brokenchain) -> IPdata:
        raise NotImplementedError