from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

from lpp.ast import (
    Expression,
    Identifier,
    LetStatement,
    Program,
    ReturnStatement,
    Statement,
)
from lpp.lexer import Lexer
from lpp.token import (
    Token,
    TokenType,
)


PrefixParseFn = Callable[[], Optional[Expression]]
InfixParseFn = Callable[[Expression], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFns = Dict[TokenType, InfixParseFn]


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str] = []

        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
        self._infix_parse_fns: InfixParseFns = self._register_infix_fns()

        self._advance_tokens()
        self._advance_tokens()

    @property
    def errors(self) -> List[str]:
        return self._errors

    def parse_program(self) -> Program:
        program = Program(statements=[])

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self._advance_tokens()

        return program

    def _advance_tokens(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_tokens()

            return True

        self._expected_token_error(token_type)
        return False

    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        error = f'Se esperaba que el siguiente token fuera {token_type} ' + \
                f'pero se obtuvo {self._peek_token.token_type}'
        self._errors.append(error)

    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None
        let_statement = LetStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None

        let_statement.name = Identifier(token=self._current_token,
                                        value=self._current_token.literal)

        if not self._expected_token(TokenType.ASSIGN):
            return None

        # TODO: skip expression until we know how to create them
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        # TODO skip expression until we know how to create them
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return return_statement

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        if self._current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.token_type == TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return None

    def _register_infix_fns(self) -> InfixParseFns:
        return {}

    def _register_prefix_fns(self) -> PrefixParseFns:
        return {}

