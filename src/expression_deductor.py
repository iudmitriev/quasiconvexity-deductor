from typing import List, Optional
from decimal import Decimal

import sympy as sym 

from src.information import ExpressionInformation
from src.propagator import ExpressionPropagator, create_propagator_from_list
from src.interval import Interval

CUSTOM_MODULES = [
    {
        'amax': ExpressionPropagator.max,
        'amin': ExpressionPropagator.min,
        'sin': ExpressionPropagator.sin,
        'cos': ExpressionPropagator.cos,
        'exp': ExpressionPropagator.exp,
        'ln': ExpressionPropagator.ln,
        'log': ExpressionPropagator.ln,
        'abs': ExpressionPropagator.abs
    },
    'numpy'
]


class ExpressionInformationDeductor:
    def __init__(self) -> None:
        self.diff_call_counter = 0

    def _match_atomic(self, atomic_expr: sym.Expr, interval: Optional[Interval] = None) \
                                                     -> Optional[ExpressionPropagator]:
        if isinstance(atomic_expr, sym.core.symbol.Symbol):
            if interval is not None:
                interval = interval
            else:
                interval = None
            return create_propagator_from_list([
                'increasing', 'convex', 'concave'
            ], interval=interval)
        
        if isinstance(atomic_expr, sym.core.numbers.Integer):
            interval = Interval([int(atomic_expr), int(atomic_expr)])
            return create_propagator_from_list([
                'constant'
            ], interval=interval)

        if isinstance(atomic_expr, sym.core.numbers.Float | sym.core.numbers.Half):
            interval = Interval([float(atomic_expr), float(atomic_expr)])
            return create_propagator_from_list([
                'constant'
            ], interval=interval)
        
        if isinstance(atomic_expr, sym.core.numbers.Float | sym.core.numbers.Half):
            interval = Interval([float(atomic_expr), float(atomic_expr)])
            return create_propagator_from_list([
                'constant'
            ], interval=interval)
        return None

    def get_information(self, expression: sym.Expr, interval: Optional[Interval] = None) \
                                                       -> Optional[ExpressionPropagator]:
        template_interval = self._match_atomic(expression, interval=interval)
        if template_interval is not None:
            return template_interval
        
        sub_information = []
        for sub_tree in expression.args:
            sub_information.append(self.get_information(sub_tree, interval=interval))
        combined_information = self._combine_information(expression, sub_information)

        bounds = self.get_bounds_based_on_information(
            expression=expression,
            interval=interval,
            information=combined_information.expression_information
        )

        if self.diff_call_counter < 2:
            self.diff_call_counter += 1
            try:
                combined_information = self.update_information_based_on_diff(expression, interval, combined_information)
            except Exception as e:
                pass
            self.diff_call_counter -= 1

        combined_information.interval = Interval([
            max(combined_information.interval[0], bounds[0]),
            min(combined_information.interval[1], bounds[1])
        ])
        return combined_information

    def _combine_information(self, expression: sym.Expr, sub_information: List[ExpressionPropagator],
                             interval: Optional[Interval] = None) -> Optional[ExpressionPropagator]:
        symbols = []
        for i in range(len(sub_information)):
            symbols.append(sym.Symbol(f'x{i}'))

        root_expression = expression.func(*symbols)
        root_expression_func = sym.utilities.lambdify(symbols, root_expression, modules=CUSTOM_MODULES)
        information = root_expression_func(*sub_information)
        
        return information

    @staticmethod
    def get_bounds_based_on_information(expression: sym.Expr, interval: Interval, 
                                        information: ExpressionInformation) -> Interval:
        expression_func = sym.utilities.lambdify(sym.Symbol(f'x'), expression)

        upper_bound = float('inf')
        lower_bound = float('-inf')
        if information.quasiconvexity_information.is_quasiconvex:
            quasiconvex_bound = max(expression_func(float(interval[0])), 
                                    expression_func(float(interval[1])))
            upper_bound = min(upper_bound, quasiconvex_bound)
        if information.quasiconvexity_information.is_quasiconcave:
            quasiconcave_bound = min(expression_func(float(interval[0])), 
                                     expression_func(float(interval[1])))
            lower_bound = max(lower_bound, quasiconcave_bound)
        
        if information.monotonic_information.is_nondecreasing:
            monotonic_upper_bound = expression_func(float(interval[1]))
            upper_bound = min(upper_bound, monotonic_upper_bound)

            monotonic_lower_bound = expression_func(float(interval[0]))
            lower_bound = max(lower_bound, monotonic_lower_bound)
        
        if information.monotonic_information.is_nonincreasing:
            monotonic_upper_bound = expression_func(float(interval[0]))
            upper_bound = min(upper_bound, monotonic_upper_bound)

            monotonic_lower_bound = expression_func(float(interval[1]))
            lower_bound = max(lower_bound, monotonic_lower_bound)
        return Interval([lower_bound, upper_bound])
    

    def update_information_based_on_diff(self, expression: sym.Expr, interval: Interval,
                                         current_propagator: ExpressionPropagator) -> ExpressionInformation:
        information = ExpressionInformation()

        expression_copy_for_eval = expression.func(*expression.args)
        diff = sym.diff(expression_copy_for_eval, sym.Symbol('x'))
        diff = sym.simplify(diff)
        diff_info = self.get_information(diff, interval)

        if diff_info.expression_information.sign_information.is_positive:
            information.monotonic_information.is_increasing = True
        if diff_info.expression_information.sign_information.is_nonnegative:
            information.monotonic_information.is_nondecreasing = True
        if diff_info.expression_information.sign_information.is_negative:
            information.monotonic_information.is_decreasing = True
        if diff_info.expression_information.sign_information.is_nonpositive:
            information.monotonic_information.is_nonincreasing = True
        information.propagate_information()

        current_propagator.expression_information = current_propagator.expression_information | information
        is_convex = current_propagator.expression_information.convexity_information.is_convex
        is_concave = current_propagator.expression_information.convexity_information.is_concave

        if is_convex or is_concave:
            a, b = interval[0], interval[1]
            f = sym.utilities.lambdify(sym.Symbol(f'x'), expression, modules=CUSTOM_MODULES)
            diff = sym.utilities.lambdify(sym.Symbol(f'x'), diff, modules=CUSTOM_MODULES)
            
            
            if is_convex and diff(a) >= 0:
                bound = f(a)
            elif is_convex and diff(b) <= 0:
                bound = f(b)
            elif is_concave and diff(a) <= 0:
                bound = f(a)
            elif is_concave and diff(b) >= 0:
                bound = f(b)
            else: 
                bound = (diff(b) * f(a) - diff(a) * f(b) + diff(b) * diff(a) * (b - a) ) / (diff(b) - diff(a))
            if not isinstance(bound, Decimal):
                bound = bound[1]
            
            if current_propagator.expression_information.convexity_information.is_convex:
                current_propagator.interval[0] = max(current_propagator.interval[0], bound)
            else:
                current_propagator.interval[1] = min(current_propagator.interval[1], bound)
        return current_propagator
