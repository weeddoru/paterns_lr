from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, Protocol

@dataclass
class Task:
    title: str
    description: str
    subject: str
    due_date: date

    def __str__(self) -> str:
        return f"[{self.subject}] {self.title} — здати до {self.due_date.isoformat()}"

class Observer(Protocol):
    def update(self, task: Task) -> None:
        ...

class SubjectPublisher:
    def __init__(self, subject_name: str) -> None:
        self.subject: str = subject_name
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, task: Task) -> None:
        for obs in list(self._observers):
            obs.update(task)

    def publish_task(self, title: str, description: str, due: date) -> Task:
        task = Task(
            title=title,
            description=description,
            subject=self.subject,
            due_date=due
        )
        self.notify(task)
        return task

class Student:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.inbox: List[Task] = []

    def update(self, task: Task) -> None:
        self.inbox.append(task)
        print(f"{self.name} отримав сповіщення: {task}")

    def subscribe_to(self, publisher: SubjectPublisher) -> None:
        publisher.attach(self)

    def unsubscribe_from(self, publisher: SubjectPublisher) -> None:
        publisher.detach(self)

    def __repr__(self) -> str:
        return f"Student({self.name})"

if __name__ == "__main__":
    math_pub = SubjectPublisher("Math")
    phys_pub = SubjectPublisher("Physics")

    alice = Student("Alice")
    bob = Student("Bob")
    lena = Student("Lena")

    alice.subscribe_to(math_pub)
    bob.subscribe_to(math_pub)
    lena.subscribe_to(math_pub)
    lena.subscribe_to(phys_pub)

    math_pub.publish_task(
        "Д/З №1",
        "Розв'язати задачі з рядів",
        date(2025, 12, 20)
    )

    phys_pub.publish_task(
        "Лабораторна 2",
        "Оформити звіт",
        date(2025, 12, 22)
    )

    bob.unsubscribe_from(math_pub)

    math_pub.publish_task(
        "Д/З №2",
        "Ознака Д'Аламбера",
        date(2025, 12, 27)
    )
