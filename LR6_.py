from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid
import sys

class AppointmentStatus(Enum):
    """
    Перелік можливих станів запису до лікаря.
    Використання Enum дозволяє уникнути магічних рядків
    та гарантує коректні значення статусів.
    """
    ACTIVE = "active"
    CANCELED = "canceled"


@dataclass
class User:
    """
    Сутність користувача (пацієнта).
    Зберігає мінімально необхідну інформацію для авторизації
    та ідентифікації користувача в системі.
    """
    id: str
    name: str
    password: str

@dataclass
class Doctor:
    """
    Сутність лікаря.
    Містить базову інформацію, яка використовується при створенні запису.
    """
    id: str
    name: str

@dataclass
class ScheduleSlot:
    """
    Сутність часової години прийому.
    Інкапсулює логіку доступності конкретного часу.
    """
    id: str
    date_time: datetime
    is_available: bool = True

    def reserve(self) -> None:
        """Позначає годину як зайняту."""
        self.is_available = False

    def release(self) -> None:
        """Звільняє годину після скасування або перенесення запису."""
        self.is_available = True

@dataclass
class Appointment:
    """
    Сутність запису до лікаря.
    Об'єднує пацієнта, лікаря та часову годину.
    """
    id: str
    patient: User
    doctor: Doctor
    slot: ScheduleSlot
    status: AppointmentStatus

    def cancel(self) -> None:
        """
        Скасовує запис:
        - змінює статус
        - звільняє зайняту годину
        """
        self.status = AppointmentStatus.CANCELED
        self.slot.release()

    def reschedule(self, new_slot: ScheduleSlot) -> None:
        """
        Переносить запис на іншу годину.
        Поточна година звільняється, нова — резервується.
        """
        self.slot.release()
        new_slot.reserve()
        self.slot = new_slot

#  ABSTRACT CLASSES 

class AppointmentFactory(ABC):
    """
    Абстрактна фабрика (Factory Method).
    Визначає інтерфейс створення запису до лікаря.
    """
    @abstractmethod
    def create(
        self,
        user: User,
        doctor: Doctor,
        slot: ScheduleSlot
    ) -> Appointment:
        """Створює та ініціалізує новий запис."""
        ...

class NotificationService(ABC):
    """
    Абстракція сервісу повідомлень.
    Дозволяє змінювати спосіб сповіщення без зміни бізнес-логіки.
    """
    @abstractmethod
    def send(self, user: User, message: str) -> None:
        """Надсилає повідомлення користувачу."""
        ...


class SlotValidationStrategy(ABC):
    """
    Стратегія перевірки доступності годин.
    Реалізує поведінковий патерн Strategy.
    """

    @abstractmethod
    def is_available(self, slot: ScheduleSlot) -> bool:
        """Перевіряє, чи доступна година для запису."""
        ...


class DefaultAppointmentFactory(AppointmentFactory):
    """
    Стандартна реалізація фабрики записів.
    Відповідає за створення запису.
    """
    def create(
        self,
        user: User,
        doctor: Doctor,
        slot: ScheduleSlot
    ) -> Appointment:
        slot.reserve()
        return Appointment(
            id=str(uuid.uuid4()),
            patient=user,
            doctor=doctor,
            slot=slot,
            status=AppointmentStatus.ACTIVE
        )


class ConsoleNotificationService(NotificationService):
    """
    Реалізація сервісу повідомлень через консоль.
    """

    def send(self, user: User, message: str) -> None:
        print(f"[ПОВІДОМЛЕННЯ для {user.name}]: {message}")


class DefaultSlotValidation(SlotValidationStrategy):
    """
    Базова стратегія перевірки доступності години.
    """

    def is_available(self, slot: ScheduleSlot) -> bool:
        return slot.is_available


#  FACADE 

class MedicalSystemFacade:
    """
    Фасад медичної системи.
    Об'єднує всі підсистеми та надає простий інтерфейс
    для взаємодії з бізнес-логікою.
    """

    def __init__(
        self,
        factory: AppointmentFactory,
        notifier: NotificationService,
        validator: SlotValidationStrategy
    ) -> None:
        self.users: List[User] = []
        self.doctors: List[Doctor] = []
        self.slots: List[ScheduleSlot] = []
        self.appointments: List[Appointment] = []
        self.current_user: Optional[User] = None

        self.factory = factory
        self.notifier = notifier
        self.validator = validator

    def register(self, name: str, password: str) -> bool:
        """Реєструє нового користувача."""
        if any(u.name == name for u in self.users):
            return False
        self.users.append(User(str(uuid.uuid4()), name, password))
        return True

    def login(self, name: str, password: str) -> bool:
        """Авторизує користувача."""
        for user in self.users:
            if user.name == name and user.password == password:
                self.current_user = user
                return True
        return False

    def list_doctors(self) -> List[Doctor]:
        """Повертає список лікарів."""
        return self.doctors

    def available_slots(self) -> List[ScheduleSlot]:
        """Повертає всі доступні години."""
        slots = [s for s in self.slots if self.validator.is_available(s)]
        if not slots and self.current_user:
            self.notifier.send(self.current_user, "Немає вільних годин")
        return slots

    def create_appointment(self, doctor: Doctor, slot: ScheduleSlot) -> None:
        """Створює новий запис до лікаря."""
        if not self.current_user:
            print("Спочатку увійдіть у систему")
            return

        if not self.validator.is_available(slot):
            self.notifier.send(self.current_user, "Година зайнята")
            return

        appointment = self.factory.create(self.current_user, doctor, slot)
        self.appointments.append(appointment)
        self.notifier.send(self.current_user, "Запис успішно створено")

    def cancel_appointment(self, appointment_id: str) -> None:
        """Скасовує існуючий запис."""
        for appointment in self.user_appointments():
            if appointment.id == appointment_id:
                appointment.cancel()
                self.notifier.send(self.current_user, "Запис скасовано")
                return

    def reschedule_appointment(self, appointment_id: str, new_slot: ScheduleSlot) -> None:
        """Переносить запис на іншу годину."""
        if not self.validator.is_available(new_slot):
            self.notifier.send(self.current_user, "Година зайнята")
            return

        for appointment in self.user_appointments():
            if appointment.id == appointment_id:
                appointment.reschedule(new_slot)
                self.notifier.send(self.current_user, "Запис перенесено")
                return

    def user_appointments(self) -> List[Appointment]:
        """Повертає активні записи поточного користувача."""
        if not self.current_user:
            return []
        return [
            a for a in self.appointments
            if a.patient == self.current_user
            and a.status == AppointmentStatus.ACTIVE
        ]


#  CONSOLE MENU 

class ConsoleMenu:
    def __init__(self, system: MedicalSystemFacade) -> None:
        self.system: MedicalSystemFacade = system

    def run(self) -> None:
        while True:
            self.print_menu()
            choice: str = input("Оберіть пункт: ")
            self.handle_choice(choice)

    def print_menu(self) -> None:
        print("\nМЕНЮ")
        print("1. Реєстрація")
        print("2. Авторизація")
        print("3. Лікарі")
        print("4. Вільні години")
        print("5. Створити запис")
        print("6. Скасувати запис")
        print("7. Перенести запис")
        print("8. Мої записи")
        print("0. Вийти")

    def handle_choice(self, choice: str) -> None:
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            self.show_doctors()
        elif choice == "4":
            self.show_slots()
        elif choice == "5":
            self.create_appointment()
        elif choice == "6":
            self.cancel_appointment()
        elif choice == "7":
            self.reschedule_appointment()
        elif choice == "8":
            self.show_appointments()
        elif choice == "0":
            sys.exit()
        else:
            print("Невірний пункт")

    def register(self) -> None:
        name: str = input("Логін: ")
        password: str = input("Пароль: ")
        print("Успіх" if self.system.register(name, password) else "Логін існує")

    def login(self) -> None:
        name: str = input("Логін: ")
        password: str = input("Пароль: ")
        print("Успішно" if self.system.login(name, password) else "Помилка авторизації")

    def show_doctors(self) -> None:
        for i, doctor in enumerate(self.system.list_doctors(), 1):
            print(f"{i}. {doctor.name}")

    def show_slots(self) -> None:
        for i, slot in enumerate(self.system.available_slots(), 1):
            print(f"{i}. {slot.date_time}")

    def create_appointment(self) -> None:
        self.show_doctors()
        doctor: Doctor = self.system.doctors[int(input("Лікар: ")) - 1]
        self.show_slots()
        slot: ScheduleSlot = self.system.available_slots()[int(input("Година: ")) - 1]
        self.system.create_appointment(doctor, slot)

    def cancel_appointment(self) -> None:
        apps: List[Appointment] = self.system.user_appointments()
        for i, a in enumerate(apps, 1):
            print(f"{i}. {a.doctor.name} | {a.slot.date_time}")
        self.system.cancel_appointment(apps[int(input("Оберіть: ")) - 1].id)

    def reschedule_appointment(self) -> None:
        apps: List[Appointment] = self.system.user_appointments()
        for i, a in enumerate(apps, 1):
            print(f"{i}. {a.doctor.name} | {a.slot.date_time}")
        appointment: Appointment = apps[int(input("Запис: ")) - 1]
        self.show_slots()
        new_slot: ScheduleSlot = self.system.available_slots()[int(input("Нова година: ")) - 1]
        self.system.reschedule_appointment(appointment.id, new_slot)

    def show_appointments(self) -> None:
        for appointment in self.system.user_appointments():
            print(f"{appointment.doctor.name} | {appointment.slot.date_time}")


def create_system() -> MedicalSystemFacade:
    system: MedicalSystemFacade = MedicalSystemFacade(
        DefaultAppointmentFactory(),
        ConsoleNotificationService(),
        DefaultSlotValidation()
    )

    system.doctors.extend([
        Doctor("1", "Dr. Smith"),
        Doctor("2", "Dr. Brown")
    ])

    now: datetime = datetime.now()
    for i in range(5):
        system.slots.append(
            ScheduleSlot(str(i), now.replace(hour=9 + i, minute=0))
        )

    return system


if __name__ == "__main__":
    menu: ConsoleMenu = ConsoleMenu(create_system())
    menu.run()
