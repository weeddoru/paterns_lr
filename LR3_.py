#Варіант 9. ЗВО складається із структурних підрозділів та працівників. 
#Кожен структурний підрозділ має свою назву, працівників та підпорядковані структурні підрозділи. 
#Працівник має ПІБ, посаду. Розробити клас для збереження структури ЗВО.
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class OrganizationUnit(ABC):
    @abstractmethod
    def show_info(self, level: int = 0) -> None:
        pass

class Employee(OrganizationUnit):
    def __init__(self, name: str, position: str) -> None:
        self.name: str = name
        self.position: str = position

    def show_info(self, level: int = 0) -> None:
        print("  " * level + f"- {self.name} ({self.position})")

class Department(OrganizationUnit):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.elements: List[OrganizationUnit] = []

    def add(self, unit: OrganizationUnit) -> None:
        self.elements.append(unit)

    def show_info(self, level: int = 0) -> None:
        print("  " * level + f"Підрозділ: {self.name}")
        for element in self.elements:
            element.show_info(level + 1)

if __name__ == "__main__":
    university: Department = Department("Університет")
    faculty: Department = Department("Математичний факультет")
    department: Department = Department("Кафедра інформатики")

    faculty.add(Employee("Іваненко І.І.", "Декан"))
    department.add(Employee("Петренко П.П.", "Завідувач кафедри"))
    department.add(Employee("Сидоренко С.С.", "Викладач"))

    faculty.add(department)
    university.add(faculty)
    university.add(Employee("Коваленко К.К.", "Ректор"))
    
    university.show_info()
