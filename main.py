from src.expression_deductor import ExpressionInformationDeductor
from src.interval import Interval

import sympy as sym

if __name__ == '__main__':
    deductor = ExpressionInformationDeductor()

    x = sym.Symbol('x')
    
    expr = sym.UnevaluatedExpr(sym.Max(2 - x, 4*x - x**2))
    info = deductor.get_information(
        expression=expr,
        interval = Interval([0, 2])
    )
    print(info.expression_information)
    print(info.interval)

    expr = sym.UnevaluatedExpr(-sym.cos(x) + sym.exp(-x))
    info = deductor.get_information(
        expression=expr,
        interval = Interval([0, 1])
    )
    print(info.expression_information)
    print(info.interval)
    
    expr = sym.UnevaluatedExpr(sym.Abs(x**3 + x**2 + 4 * x))
    info = deductor.get_information(
        expression=expr,
        interval=Interval([-2, 1])
    )
    print(info.expression_information)
    print(info.interval)

    expr = sym.UnevaluatedExpr((x + sym.cos(x))**2)
    info = deductor.get_information(
        expression=expr,
        interval=Interval([-1, 1])
    )
    print(info.expression_information)
    print(info.interval)
    