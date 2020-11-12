from typing import (
    Any,
    cast,
    List,
    Tuple,
    Optional,
)
from unittest import TestCase

from lpp.evaluator import (
    evaluate,
    NULL,
)
from lpp.lexer import Lexer
from lpp.object import (
    Boolean,
    Environment,
    Error,
    Function,
    Integer,
    Object,
    String,
)
from lpp.parser import Parser


class EvaluatorTest(TestCase):

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('10', 10),
            ('-5', -5),
            ('-10', -10),
            ('5 + 5', 10),
            ('5 - 10', -5),
            ('2 * 2 * 2 * 2', 16),
            ('2 * 5 - 3', 7),
            ('50 / 2', 25),
            ('2 * (5 - 3)', 4),
            ('(2 + 7) / 3', 3),
            ('50 / 2 * 2 + 10', 60),
            ('5 / 2', 2),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('verdadero', True),
            ('falso', False),
            ('1 < 2', True),
            ('1 > 2', False),
            ('1 < 1', False),
            ('1 > 1', False),
            ('1 == 1', True),
            ('1 != 1', False),
            ('1 == 2', False),
            ('1 != 2', True),
            ('verdadero == verdadero', True),
            ('falso == falso', True),
            ('verdadero == falso', False),
            ('verdadero != falso', True),
            ('(1 < 2) == verdadero', True),
            ('(1 < 2) == falso', False),
            ('(1 > 2) == verdadero', False),
            ('(1 > 2) == falso', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_bang_operator(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('!verdadero', False),
            ('!falso', True),
            ('!!verdadero', True),
            ('!!falso', False),
            ('!5', False),
            ('!!5', True),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('si (verdadero) { 10 }', 10),
            ('si (falso) { 10 }', None),
            ('si (1) { 10 }', 10),
            ('si (1 < 2) { 10 }', 10),
            ('si (1 > 2) { 10 }', None),
            ('si (1 < 2) { 10 } si_no { 20 }', 10),
            ('si (1 > 2) { 10 } si_no { 20 }', 20),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            
            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_return_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('regresa 10;', 10),
            ('regresa 10; 9;', 10),
            ('regresa 2 * 5; 9;', 10),
            ('9; regresa 3 * 6; 9;', 18),
            ('''
                si (10 > 1) {
                    si (20 > 10) {
                        regresa 1;
                    }

                    regresa 0;
                }
            ''', 1)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('5 + verdadero',
             'Discrepancia de tipos: INTEGER + BOOLEAN'),
            ('5 + verdadero; 9;',
             'Discrepancia de tipos: INTEGER + BOOLEAN'),
            ('-verdadero',
             'Operador desconocido: -BOOLEAN'),
            ('verdadero + falso;',
             'Operador desconocido: BOOLEAN + BOOLEAN'),
            ('5; verdadero - falso; 10;',
             'Operador desconocido: BOOLEAN - BOOLEAN'),
            ('''
                si (10 > 7) {
                    regresa verdadero + falso;
                }
            ''',
             'Operador desconocido: BOOLEAN + BOOLEAN'),
            ('''
                si (10 > 1) {
                    si (verdadero) {
                        regresa verdadero * falso
                    }

                    regresa 1;
                }
            ''',
             'Operador desconocido: BOOLEAN * BOOLEAN'),
            ('''
                si (5 < 2) {
                    regresa 1;
                } si_no {
                    regresa verdadero / falso;
                }
            ''',
             'Operador desconocido: BOOLEAN / BOOLEAN'),
            ('foobar;',
             'Identificador no encontrado: foobar'),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)

    def test_assignment_statements(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('variable a = 5; a;', 5),
            ('variable a = 5 * 5; a;', 25),
            ('variable a = 5; variable b = a; b;', 5),
            ('variable a = 5; variable b = a; variable c = a + b + 5; c;', 15),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_evaluation(self) -> None:
        source: str = 'procedimiento(x) { x + 2; };'

        evaluated = self._evaluate_tests(source)

        self.assertIsInstance(evaluated, Function)

        evaluated = cast(Function, evaluated)

        self.assertEquals(len(evaluated.parameters), 1)
        self.assertEquals(str(evaluated.parameters[0]), 'x')
        self.assertEquals(str(evaluated.body), '(x + 2)')

    def test_function_calls(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('variable identidad = procedimiento(x) { x }; identidad(5);', 5),
            ('''
                variable identidad = procedimiento(x) { 
                    regresa x; 
                }; 
                identidad(5);
            ''', 5),
            ('''
                variable doble = procedimiento(x) {
                    regresa 2 * x;
                };
                doble(5);
            ''', 10),
            ('''
                variable suma = procedimiento(x, y) {
                    regresa x + y;
                };
                suma(3, 8);
            ''', 11),
            ('''
                variable suma = procedimiento(x, y) {
                    regresa x + y;
                };
                suma(5 + 5, suma(10, 10));
            ''', 30),
            ('procedimiento(x) { x }(5)', 5),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_string_evaluation(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('"Hello world!"', 'Hello world!'),
            ('procedimiento() { regresa "Platzi is great"; }()', 
             'Platzi is great'),
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self.assertIsInstance(evaluated, String)

            evaluated = cast(String, evaluated)
            self.assertEquals(evaluated.value, expected)

    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program = parser.parse_program()
        env = Environment()

        evaluated = evaluate(program, env)

        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEquals(evaluated, NULL)

