from typing import cast, List, Optional

import lpp.ast as ast
from lpp.object import Integer, Object


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

    return None


def _eval_statements(statements: List[ast.Statement]) -> Optional[Object]:
    result: Optional[Object] = None

    for statement in statements:
        result = evaluate(statement)

    return result

