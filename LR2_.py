#Варіант 9. Розробити підсистему для завантаження збереження гри в 2D. Описати клас для 
#створення NPC (Ім'я, координати x та y, кількість життів) та декорацій ( вид, наприклад, камінь, дерево та координати) .
# Передбачити існування підводних та наземних рівнів. Врахувати, що підводні NPC не можуть взаємодіяти з наземними декораціями і навпаки.
# Система отримє список об'єктів, вид рівня (наземний чи підводний) 
#та розміри карти, а повертає рівень гри - .двовимірний масив із розставленими об'єктами.
from abc import ABC, abstractmethod
from typing import List, Union, Optional
import random

class NPC(ABC):
    def __init__(self, name: str, x: int, y: int, hp: int):
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp

    @abstractmethod
    def info(self) -> str:
        pass

class Decoration(ABC):
    def __init__(self, type_name: str, x: int, y: int):
        self.type_name = type_name
        self.x = x
        self.y = y

    @abstractmethod
    def info(self) -> str:
        pass

class LandNPC(NPC):
    def info(self) -> str:
        return f"Наземний NPC: {self.name} ({self.x},{self.y}), HP={self.hp}"

class LandDecoration(Decoration):
    def info(self) -> str:
        return f"Наземна декорація: {self.type_name} ({self.x},{self.y})"

class UnderwaterNPC(NPC):
    def info(self) -> str:
        return f"Підводний NPC: {self.name} ({self.x},{self.y}), HP={self.hp}"

class UnderwaterDecoration(Decoration):
    def info(self) -> str:
        return f"Підводна декорація: {self.type_name} ({self.x},{self.y})"

class GameFactory(ABC):
    @abstractmethod
    def create_npc(self, name: str) -> NPC:
        pass

    @abstractmethod
    def create_decoration(self, type_name: str) -> Decoration:
        pass

class LandFactory(GameFactory):
    def create_npc(self, name: str) -> LandNPC:
        return LandNPC(name, random.randint(0, 9), random.randint(0, 9), random.randint(50, 100))

    def create_decoration(self, type_name: str) -> LandDecoration:
        return LandDecoration(type_name, random.randint(0, 9), random.randint(0, 9))

class UnderwaterFactory(GameFactory):
    def create_npc(self, name: str) -> UnderwaterNPC:
        return UnderwaterNPC(name, random.randint(0, 9), random.randint(0, 9), random.randint(50, 100))

    def create_decoration(self, type_name: str) -> UnderwaterDecoration:
        return UnderwaterDecoration(type_name, random.randint(0, 9), random.randint(0, 9))

class GameLevel:
    def __init__(self, width: int, height: int, factory: GameFactory):
        self.width = width
        self.height = height
        self.factory = factory
        self.map: List[List[Optional[Union[NPC, Decoration]]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]
        self.objects: List[Union[NPC, Decoration]] = []

    def add_object(self, obj: Union[NPC, Decoration]) -> None:
        if 0 <= obj.y < self.height and 0 <= obj.x < self.width:
            if self.map[obj.y][obj.x] is None:
                self.map[obj.y][obj.x] = obj
                self.objects.append(obj)

    def display(self) -> None:
        for row in self.map:
            line = ""
            for cell in row:
                if isinstance(cell, NPC):
                    line += "N "
                elif isinstance(cell, Decoration):
                    line += "D "
                else:
                    line += ". "
            print(line)
        print("\n Об’єкти рівня:")
        for obj in self.objects:
            print(obj.info())

def main() -> None:
    land_npc_names = ["Ork", "Elf", "Human", "Troll"]
    land_decorations = ["Tree", "Rock", "House", "Bush"]

    water_npc_names = ["Mermaid", "Shark", "Octopus", "Crab"]
    water_decorations = ["Coral", "Seaweed", "Shell", "Rock"]

    print("Виберіть тип рівня:")
    print("1. Наземний рівень")
    print("2. Підводний рівень")
    choice = input("Ваш вибір: ")

    if choice == "1":
        factory = LandFactory()
        npc_names = land_npc_names
        deco_names = land_decorations
        print("Створено наземний рівень!")
    elif choice == "2":
        factory = UnderwaterFactory()
        npc_names = water_npc_names
        deco_names = water_decorations
        print("Створено підводний рівень!")
    else:
        print("Помилка: вибрано неправильний рівень!")
        return
    level = GameLevel(width=10, height=6, factory=factory)

    for name in random.sample(npc_names, 3):
        level.add_object(factory.create_npc(name))

    for deco in random.sample(deco_names, 3):
        level.add_object(factory.create_decoration(deco))

    print("\n=== Поточна карта ===")
    level.display()


if __name__ == "__main__":
    main()
