from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.value = None

    def __get__(self, instance: object, owner: type) -> int:
        return self.value

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"Value must be between "
                             f"{self.min_amount} and {self.max_amount}.")
        self.value = value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def validate(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def validate(self, visitor: Visitor) -> bool:
        try:
            self.age = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation_instance = self.limitation_class()
        return limitation_instance.validate(visitor)
