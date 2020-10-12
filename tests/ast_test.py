from unittest import TestCase

from lpp.ast import (
    Identifier,
    LetStatement,
    Program,
)
from lpp.token import (
    Token,
    TokenType,
)

class ASTTest(TestCase):

    def test_let_statement(self) -> None:
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='variable'),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal='mi_var'),
                    value='mi_var'
                ),
                value=Identifier(
                    token=Token(TokenType.IDENT, literal='otra_var'),
                    value='otra_var'
                )
            ),
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'variable mi_var = otra_var;')

