#Задача:в програмі існує старий тип об'єкта — OldNPC, який рухається за допомогою методів:set_direction(degrees),set_speed(speed),start()
# А нова система руху приймає координати у форматі move(x, y).Реалізувати патерн,
#  щоб забезпечити сумісність застарілого API з новим інтерфейсом, не змінюючи код старого класу.
#Користь шаблону:Дозволяє підключати старі або сторонні модулі без зміни їхнього коду.
# Покращує сумісність між новими та старими системами.
# Значно економить час при інтеграції бібліотек або застарілого коду.
import math
from typing import Protocol

class NewMover(Protocol):
    def move(self, x: float, y: float) -> None:
        ...

class OldNPC:
    def set_direction(self, degrees: int) -> None:
        print(f"Setting direction: {degrees}°")

    def set_speed(self, speed: int) -> None:
        print(f"Setting speed: {speed}")

    def start(self) -> None:
        print("NPC started moving")

class NPCAdapter:
    def __init__(self, npc: OldNPC) -> None:
        self.npc: OldNPC = npc

    def move(self, x: float, y: float) -> None:
        degrees: float = math.degrees(math.atan2(y, x))
        speed: int = int((x**2 + y**2)**0.5)

        self.npc.set_direction(int(degrees))
        self.npc.set_speed(speed)
        self.npc.start()

old_npc: OldNPC = OldNPC()
adapted_npc: NewMover = NPCAdapter(old_npc)

adapted_npc.move(3, 4)
