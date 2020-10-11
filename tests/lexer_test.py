from unittest import TestCase
from typing import List

from lpp.token import (
    Token,
    TokenType,
)
from lpp.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '@¡¿'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '@'),
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_one_character_operators(self) -> None:
        source: str = '=+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        self.fail('Not implemented yet')
        source = '(){},;'



