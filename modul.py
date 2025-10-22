#Об’єкт Замовлення (Список товарів (назва, кількість, ціна) та Спосіб
#оплати (при отриманні, переказ, кредит чи карткою)). Розробити систему яка
#розраховує кінцеву ціну Замовлення враховуючи:
#a. Податок в X відсотків якщо в списку більше ніж N товарів.
#b. Оплата Y відсотків ПДВ при оплаті переказом
#с. Податок в Z відсотків якщо сума покупки більше ніж А грн.
#Врахувати всі можливі комбінації податків та вивести кінцеву сум.
#Вказати шаблон, який доцільно використати для розв'язування задачі.
from __future__ import annotations  
from abc import ABC, abstractmethod
from typing import List

class Product:
    def __init__(self, name: str, quantity: int, price: float) -> None:
        self.name: str = name
        self.quantity: int = quantity
        self.price: float = price

    def total(self) -> float:
        return self.quantity * self.price

class PriceComponent(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass

class BaseOrder(PriceComponent):
    def __init__(self, products: List[Product]) -> None:
        self.products: List[Product] = products

    def get_price(self) -> float:
        return sum(p.total() for p in self.products)

class TaxDecorator(PriceComponent):
    def __init__(self, component: PriceComponent) -> None:
        self.component: PriceComponent = component

class ItemCountTax(TaxDecorator):
    def __init__(self, component: PriceComponent, X: float, N: int, count: int) -> None:
        super().__init__(component)
        self.X: float = X
        self.N: int = N
        self.count: int = count

    def get_price(self) -> float:
        price: float = self.component.get_price()
        if self.count > self.N:
            price += price * self.X / 100
        return price

class TransferTax(TaxDecorator):
    def __init__(self, component: PriceComponent, Y: float, is_transfer: bool) -> None:
        super().__init__(component)
        self.Y: float = Y
        self.is_transfer: bool = is_transfer

    def get_price(self) -> float:
        price: float = self.component.get_price()
        if self.is_transfer:
            price += price * self.Y / 100
        return price

class TotalSumTax(TaxDecorator):
    def __init__(self, component: PriceComponent, Z: float, A: float) -> None:
        super().__init__(component)
        self.Z: float = Z
        self.A: float = A

    def get_price(self) -> float:
        price: float = self.component.get_price()
        if price > self.A:
            price += price * self.Z / 100
        return price

class OrderBuilder:
    def __init__(self) -> None:
        self.products: List[Product] = []
        self.method: str = ""
        self.X: float = 0.0
        self.N: int = 0
        self.Y: float = 0.0
        self.Z: float = 0.0
        self.A: float = 0.0

    def add_product(self, name: str, quantity: int, price: float) -> OrderBuilder:
        self.products.append(Product(name, quantity, price))
        return self

    def set_payment_method(self, method: str) -> OrderBuilder:
        self.method = method.lower()
        return self

    def set_tax_params(self, X: float, N: int, Y: float, Z: float, A: float) -> OrderBuilder:
        self.X, self.N, self.Y, self.Z, self.A = X, N, Y, Z, A
        return self

    def build(self) -> PriceComponent:
        base: PriceComponent = BaseOrder(self.products)
        order: PriceComponent = ItemCountTax(base, self.X, self.N, len(self.products))
        order = TransferTax(order, self.Y, self.method == "переказ")
        order = TotalSumTax(order, self.Z, self.A)
        return order

if __name__ == "__main__":
    print(" Створення замовлення ")
    builder: OrderBuilder = OrderBuilder()
    n: int = int(input("Скільки товарів у замовленні? "))
    for i in range(n):
        name: str = input(f"Назва товару {i+1}: ")
        qty: int = int(input("Кількість: "))
        price: float = float(input("Ціна: "))
        builder.add_product(name, qty, price)

    print("\nСпособи оплати: при отриманні, переказ, кредит, карткою")
    method: str = input("Оберіть спосіб оплати: ")
    builder.set_payment_method(method)

    builder.set_tax_params(X=5, N=2, Y=20, Z=10, A=20000)

    order: PriceComponent = builder.build()
    final_price: float = order.get_price()

    print(f"\nКінцева сума замовлення: {round(final_price, 2)} грн")
