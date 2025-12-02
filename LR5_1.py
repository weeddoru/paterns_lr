#Задача:Реалізувати систему побудови об’єктів типу Pizza з різними параметрами: розмір, тип тіста, соус та набір додаткових інгредієнтів.
#Користь шаблону:Дозволяє гнучко будувати складні об’єкти крок за кроком.
# Запобігає створенню конструкторів із 10+ параметрами.
# Дозволяє мати різні стилі побудови (наприклад, “М’ясна піца”, “Веганська піца”) без дублювання коду.
from typing import List, Optional

class Pizza:
    def __init__(self) -> None:
        self.size: Optional[str] = None
        self.dough: Optional[str] = None
        self.sauce: Optional[str] = None
        self.toppings: List[str] = []

    def __str__(self) -> str:
        return f"Pizza({self.size}, {self.dough}, {self.sauce}, {self.toppings})"

class PizzaBuilder:
    def __init__(self) -> None:
        self.pizza: Pizza = Pizza()

    def set_size(self, size: str) -> "PizzaBuilder":
        self.pizza.size = size
        return self

    def set_dough(self, dough: str) -> "PizzaBuilder":
        self.pizza.dough = dough
        return self

    def set_sauce(self, sauce: str) -> "PizzaBuilder":
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self.pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        return self.pizza

pizza: Pizza = (
    PizzaBuilder()
    .set_size("Large")
    .set_dough("Thin")
    .set_sauce("Tomato")
    .add_topping("Cheese")
    .add_topping("Pepperoni")
    .build()
)

print(pizza)
