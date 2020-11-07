from abc import abstractmethod, ABC
from enum import auto, Enum


class ObjectType(Enum):
    BOOLEAN = auto()
    INTEGER = auto()
    NULL = auto()


class Object(ABC):

    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


class Integer(Object):

    def __init__(self, value: int) -> None:
        self._value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self._value)


class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self._value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'verdadero' if self._value else 'falso'


class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return 'nulo'

