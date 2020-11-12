from abc import abstractmethod, ABC
from enum import auto, Enum
from typing import (
    Dict,
    List,
    Optional,
)

from lpp.ast import (
    Block,
    Identifier,
)


class ObjectType(Enum):
    BOOLEAN = auto()
    ERROR = auto()
    FUNCTION = auto()
    INTEGER = auto()
    NULL = auto()
    RETURN = auto()
    STRING = auto()


class Object(ABC):

    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass


class Integer(Object):

    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'verdadero' if self.value else 'falso'


class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return 'nulo'


class Return(Object):

    def __init__(self, value: Object):
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.RETURN

    def inspect(self) -> str:
        return self.value.inspect()


class Error(Object):

    def __init__(self, message: str) -> None:
        self.message = message

    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f'Error: {self.message}'


class Environment(Dict):

    def __init__(self, outer = None):
        self._store: Dict = dict()
        self._outer = outer

    def __getitem__(self, key):
        try:
            return self._store[key]
        except KeyError as e:
            if self._outer is not None:
                return self._outer[key]

            raise e

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]


class Function(Object):

    def __init__(self,
                 parameters: List[Identifier],
                 body: Block,
                 env: Environment) -> None:
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        params: str = ', '.join([str(param) for param in self.parameters])

        return 'procedimiento({}) {{\n{}\n}}'.format(params, str(self.body))


class String(Object):

    def __init__(self, value: str) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.STRING

    def inspect(self) -> str:
        return self.value

