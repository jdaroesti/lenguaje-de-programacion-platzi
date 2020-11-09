from typing import (
    Any,
    cast,
    List,
    Optional,
    Type,
)

import lpp.ast as ast
from lpp.object import (
    Boolean,
    Environment,
    Error,
    Function,
    Integer,
    Null,
    Object,
    ObjectType,
    Return,
)


TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


_TYPE_MISMATCH = 'Discrepancia de tipos: {} {} {}'
_UNKNOWN_PREFIX_OPERATOR = 'Operador desconocido: {}{}'
_UNKNOWN_INFIX_OPERATOR = 'Operador desconocido: {} {} {}'
_UNKNOWN_IDENTIFIER = 'Identificador no encontrado: {}'


def evaluate(node: ast.ASTNode, env: Environment) -> Optional[Object]:
    node_type: Type = type(node)

    if node_type == ast.Program:
        node = cast(ast.Program, node)

        return _evaluate_program(node, env)
    elif node_type == ast.ExpressionStatement:
        node = cast(ast.ExpressionStatement, node)

        assert node.expression is not None
        return evaluate(node.expression, env)
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
        right = evaluate(node.right, env)

        assert right is not None
        return _evaluate_prefix_expression(node.operator, right)
    elif node_type == ast.Infix:
        node = cast(ast.Infix, node)

        assert node.left is not None and node.right is not None
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)

        assert right is not None and left is not None
        return _evaluate_infix_expression(node.operator, left, right)
    elif node_type == ast.Block:
        node = cast(ast.Block, node)

        return _evaluate_block_statement(node, env)
    elif node_type == ast.If:
        node = cast(ast.If, node)

        return _evaluate_if_expression(node, env)
    elif node_type == ast.ReturnStatement:
        node = cast(ast.ReturnStatement, node)

        assert node.return_value is not None
        value = evaluate(node.return_value, env)

        assert value is not None
        return Return(value)
    elif node_type == ast.LetStatement:
        node = cast(ast.LetStatement, node)

        assert node.value is not None
        value = evaluate(node.value, env)

        assert node.name is not None
        env[node.name.value] = value
    elif node_type == ast.Identifier:
        node = cast(ast.Identifier, node)

        return _evaluate_identifier(node, env)
    elif node_type == ast.Function:
        node = cast(ast.Function, node)

        assert node.body is not None
        return Function(node.parameters,
                        node.body,
                        env)

    return None


def _evaluate_program(program: ast.Program, env: Environment) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in program.statements:
        result = evaluate(statement, env)

        if type(result) == Return:
            result = cast(Return, result)
            return result.value
        elif type(result) == Error:
            return result

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


def _evaluate_block_statement(block: ast.Block, env: Environment) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in block.statements:
        result = evaluate(statement, env)

        if result is not None and \
                (result.type() == ObjectType.RETURN or result.type() == ObjectType.ERROR):
            return result

    return result


def _evaluate_identifier(node: ast.Identifier, env: Environment) -> Object:
    try:
        return env[node.value]
    except KeyError:
        return _new_error(_UNKNOWN_IDENTIFIER, [node.value])


def _evaluate_if_expression(if_expression: ast.If, env: Environment) -> Optional[Object]:
    assert if_expression.condition is not None
    condition = evaluate(if_expression.condition, env)

    assert condition is not None
    if _is_truthy(condition):
        assert if_expression.consequence is not None
        return evaluate(if_expression.consequence, env)
    elif if_expression.alternative is not None:
        return evaluate(if_expression.alternative, env)
    else:
        return NULL


def _evaluate_infix_expression(operator: str, 
                                left: Object, 
                                right: Object) -> Object:
    if left.type() == ObjectType.INTEGER \
            and right.type() == ObjectType.INTEGER:
        return _evaluate_integer_infix_expression(operator, left, right)
    elif operator == '==':
        return _to_boolean_object(left is right)
    elif operator == '!=':
        return _to_boolean_object(left is not right)
    elif left.type() != right.type():
        return _new_error(_TYPE_MISMATCH, [left.type().name, 
                                           operator, 
                                           right.type().name])
    else:
        return _new_error(_UNKNOWN_INFIX_OPERATOR, [left.type().name, 
                                                    operator, 
                                                    right.type().name])


def _evaluate_integer_infix_expression(operator: str,
                                       left: Object,
                                       right: Object) -> Object:
    left_value: int = cast(Integer, left).value
    right_value: int = cast(Integer, right).value

    if operator == '+':
        return Integer(left_value + right_value)
    elif operator == '-':
        return Integer(left_value - right_value)
    elif operator == '*':
        return Integer(left_value * right_value)
    elif operator == '/':
        return Integer(left_value // right_value)
    elif operator == '<':
        return _to_boolean_object(left_value < right_value)
    elif operator == '>':
        return _to_boolean_object(left_value > right_value)
    elif operator == '==':
        return _to_boolean_object(left_value == right_value)
    elif operator == '!=':
        return _to_boolean_object(left_value != right_value)
    else:
        return _new_error(_UNKNOWN_INFIX_OPERATOR, [left.type().name, 
                                                    operator, 
                                                    right.type().name])


def _evaluate_minus_operator_expression(right: Object) -> Object:
    if type(right) != Integer:
        return _new_error(_UNKNOWN_PREFIX_OPERATOR, ['-', right.type().name])

    right = cast(Integer, right)

    return Integer(-right.value)


def _evaluate_prefix_expression(operator: str, right: Object) -> Object:
    if operator == '!':
        return _evaluate_bang_operator_expression(right)
    elif operator == '-':
        return _evaluate_minus_operator_expression(right)
    else:
        return _new_error(_UNKNOWN_PREFIX_OPERATOR, [operator, right.type().name])


def _is_truthy(obj: Object) -> bool:
    if obj is NULL:
        return False
    elif obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return True


def _new_error(message: str, args: List[Any]) -> Error:
    return Error(message.format(*args))


def _to_boolean_object(value: bool) -> Boolean:
    return TRUE if value else FALSE

