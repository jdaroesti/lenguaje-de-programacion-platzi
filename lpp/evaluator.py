from typing import cast, List, Optional

import lpp.ast as ast
from lpp.object import Boolean, Integer, Null, Object


TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def evaluate(node: ast.ASTNode) -> Optional[Object]:
    node_type = type(node)

    if node_type == ast.Program:
        node = cast(ast.Program, node)

        return _eval_statements(node.statements)
    elif node_type == ast.ExpressionStatement:
        node = cast(ast.ExpressionStatement, node)

        assert node.expression is not None
        return evaluate(node.expression)
    elif node_type == ast.Integer:
        node = cast(ast.Integer, node)

        assert node.value is not None
        return Integer(node.value)
    elif node_type == ast.Boolean:
        node = cast(ast.Boolean, node)

        assert node.value is not None
        return _to_boolean_object(node.value)
    elif node_type == ast.Prefix:
        node = cast(ast.Prefix, node)

        assert node.right is not None
        right = evaluate(node.right)

        assert right is not None
        return _evaluate_prefix_expression(node.operator, right)

    return None


def _eval_statements(statements: List[ast.Statement]) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in statements:
        result = evaluate(statement)

    return result


def _evaluate_bang_operator_expression(right: Object) -> Object:
    if right is TRUE:
        return FALSE
    elif right is FALSE:
        return TRUE
    elif right is NULL:
        return TRUE
    else:
        return FALSE


def _evaluate_minus_operator_expression(right: Object) -> Object:
    if type(right) != Integer:
        return NULL

    right = cast(Integer, right)

    return Integer(-right.value)

def _evaluate_prefix_expression(operator: str, right: Object) -> Object:
    if operator == '!':
        return _evaluate_bang_operator_expression(right)
    elif operator == '-':
        return _evaluate_minus_operator_expression(right)
    else:
        return NULL


def _to_boolean_object(value: bool) -> Boolean:
    return TRUE if value else FALSE

