#Задача:Реалізувати систему моделювання поведінки різних типів ворогів, у якій усі вони виконують однакову послідовність дій під час атаки: 
# пошук цілі, наближення, удар та відступ.
#Загальна структура алгоритму повинна бути визначена в базовому абстрактному компоненті, 
# а конкретний спосіб атаки має задаватися у похідних елементах.
#Користь шаблону:
#Гарантує єдиний алгоритм, але з можливістю замінювати окремі частини.
#Мінімізує дублювання коду.
#Додає нових ворогів без зміни базової логіки.
from abc import ABC, abstractmethod
from typing import List

class Enemy(ABC):
    def attack_sequence(self) -> None:
        self.find_target()
        self.move_to_target()
        self.attack()
        self.retreat()
        print("  ")

    def find_target(self) -> None:
        print("Enemy looks for the target")

    def move_to_target(self) -> None:
        print("Enemy moves closer")

    @abstractmethod
    def attack(self) -> None:
        pass

    def retreat(self) -> None:
        print("Enemy moves back")


class Zombie(Enemy):
    def attack(self) -> None:
        print("Zombie bites!")

class Robot(Enemy):
    def attack(self) -> None:
        print("Robot shoots a laser!")

class Dragon(Enemy):
    def attack(self) -> None:
        print("Dragon breathes fire!")

enemies: List[Enemy] = [Zombie(), Robot(), Dragon()]

for e in enemies:
    e.attack_sequence()
