from abc import ABC, abstractmethod
from typing import List, Generator

class House:
    def __init__(self, address: str, residents: int) -> None:
        self.address: str = address
        self.residents: int = residents

    def is_empty(self) -> bool:
        return self.residents == 0

class TraversalStrategy(ABC):
    @abstractmethod
    def traverse(self, matrix: List[List[House]]) -> Generator[House, None, None]:
        pass

class RowByRowTraversal(TraversalStrategy):
    def traverse(self, matrix: List[List[House]]) -> Generator[House, None, None]:
        for row in matrix:
            for house in row:
                yield house

class SpiralTraversal(TraversalStrategy):
    def traverse(self, matrix: List[List[House]]) -> Generator[House, None, None]:
        top: int = 0
        bottom: int = len(matrix) - 1
        left: int = 0
        right: int = len(matrix[0]) - 1

        while left <= right and top <= bottom:
            for col in range(left, right + 1):
                yield matrix[top][col]
            top += 1

            for row in range(top, bottom + 1):
                yield matrix[row][right]
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    yield matrix[bottom][col]
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    yield matrix[row][left]
                left += 1

class City:
    def __init__(self, matrix: List[List[House]], strategy: TraversalStrategy) -> None:
        self.matrix: List[List[House]] = matrix
        self.strategy: TraversalStrategy = strategy

    def set_strategy(self, strategy: TraversalStrategy) -> None:
        self.strategy = strategy

    def print_empty_houses(self) -> None:
        print("Порожні будинки:")
        for house in self.strategy.traverse(self.matrix):
            if house.is_empty():
                print(house.address)

city_map: List[List[House]] = [
    [House("A1", 3), House("A2", 0), House("A3", 1)],
    [House("B1", 0), House("B2", 2), House("B3", 0)],
    [House("C1", 1), House("C2", 0), House("C3", 4)]
]

print("Обхід по рядках :")
city = City(city_map, RowByRowTraversal())
city.print_empty_houses()

print("\nСпіральний обхід:")
city.set_strategy(SpiralTraversal())
city.print_empty_houses()
