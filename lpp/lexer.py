from re import match
from lpp.token import (
    Token,
    TokenType,
)

class Lexer:

    def __init__(self, source: str) -> None:
        self._source: str = source
        self._position: int = 0
        self._read_position: int = 0
        self._character: str = ''

        self._read_character()

    def next_token(self) -> Token:
        if match(r'^=$', self._character):
            token = Token(TokenType.ASSIGN, self._character)
        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, self._character)
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()

        return token

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

