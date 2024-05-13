import numpy as np
from sympy.core.expr import Expr as SympyExpression

from typing import List, Dict
from decimal import Decimal

from src.information import ExpressionInformation
from src.rule_set import rule_set
from src.composition_rule_set import composition_rule_set

from src.information import create_information_from_list
from src.interval import Interval

class MetaExpressionPropagator(type):
    def __new__(cls, name, bases, dct):
        propagator_class = super().__new__(cls, name, bases, dct)
        unary_methods = ['__neg__']
        for method in unary_methods:
            def create_method(method):
                def method_func(self):
                    if method not in rule_set:
                        return ExpressionPropagator()
                    rules = rule_set[method]
                    result = ExpressionInformation()
                    for rule in rules:
                        if rule.condition <= self.expression_information:
                            result = result | rule.result
                    interval = getattr(self.interval, method)()
                    return ExpressionPropagator(
                        expression_information=result,
                        interval=interval
                    )
                return method_func
            
            setattr(propagator_class, method, create_method(method))

        methods = ['__add__', '__sub__', '__mul__']
        for method in methods:
            def create_method(method):
                if method in ['__add__', '__mul__']:
                    is_symmetric = True
                else:
                    is_symmetric = False

                def method_func(self, other):
                    if method not in rule_set:
                        return ExpressionPropagator()
                    rules = rule_set[method]
                    result = ExpressionInformation()
                    for rule in rules:
                        if (rule.condition_on_first <= self.expression_information and
                            rule.condition_on_second <= other.expression_information):
                            result = result | rule.result
                        if (is_symmetric and
                            rule.condition_on_first <= other.expression_information and
                            rule.condition_on_second <= self.expression_information):
                            result = result | rule.result
                    interval = getattr(self.interval, method)(
                        other.interval
                    )
                    return ExpressionPropagator(
                        expression_information=result,
                        interval=interval
                    )
                return method_func
            
            setattr(propagator_class, method, create_method(method))
        return propagator_class


class ExpressionPropagator(metaclass=MetaExpressionPropagator):
    def __init__(self, expression_information: ExpressionInformation = None,
                       interval: Interval = None) -> None:
        if expression_information is None:
            self.expression_information = ExpressionInformation()
        else:
            self.expression_information = expression_information

        if interval is None:
            self.interval = Interval([-float('inf'), float('inf')])
        else:
            self.interval = interval
        self.propagate_bounds()
    
    @staticmethod
    def max(propagators, axis=None):
        rules = rule_set['max']

        current_info = propagators[0].expression_information
        current_interval = propagators[0].interval
        for propagator in propagators[1:]:
            result_info = ExpressionInformation()
            for rule in rules:
                if (rule.condition_on_first <= current_info and
                    rule.condition_on_second <= propagator.expression_information):
                    result_info = result_info | rule.result
            current_info = result_info
            current_interval = current_interval._max(propagator.interval)

        return ExpressionPropagator(
            expression_information=current_info,
            interval=current_interval
        )

    @staticmethod
    def min(propagators, axis=None):
        rules = rule_set['min']

        current_info = propagators[0].expression_information
        current_interval = propagators[0].interval
        for propagator in propagators[1:]:
            result_info = ExpressionInformation()
            for rule in rules:
                if (rule.condition_on_first <= current_info and
                    rule.condition_on_second <= propagator.expression_information):
                    result_info = result_info | rule.result
            current_info = result_info
            current_interval = current_interval._min(propagator.interval)

        return ExpressionPropagator(
            expression_information=current_info,
            interval=current_interval
        )
    
    def __pow__(self, other):
        if other.interval[0] != other.interval[1]:
            raise ValueError('Only constant degrees are supported for __pow__')
        degree = int(other.interval[0])

        if degree % 2 == 0:
            if self.interval > 0:
                information = create_information_from_list(['convex', 'increasing'])
            elif self.interval < 0:
                information = create_information_from_list(['convex', 'decreasing'])
            else:
                information = create_information_from_list(['convex'])
        else:
            if self.interval > 0:
                information = create_information_from_list(['increasing', 'convex'])
            elif self.interval < 0:
                information = create_information_from_list(['increasing', 'concave'])
            else:
                information = create_information_from_list(['increasing'])
        composition_information = ExpressionPropagator.get_composition_information(
            information,
            self.expression_information
        )
        
        return ExpressionPropagator(
            expression_information=composition_information,
            interval=self.interval ** other.interval
        )

    
    @staticmethod
    def sin(expression):
        if not isinstance(expression, ExpressionPropagator):
            return Interval.sin(expression)

        interval = expression.interval

        information = ExpressionInformation()
        pi = Decimal(np.pi)

        left_end = (interval[0] % (2*pi) + 2*pi) % (2*pi)
        right_end = (interval[1] % (2*pi) + 2*pi) % (2*pi)
        if (interval.width() <= pi and 
            left_end >= pi / 2 and
            right_end <= 3 * pi / 2):
            information = information | create_information_from_list(['decreasing'])
        if (interval.width() <= pi and 
            (left_end + 3 * pi/2) % (2*pi) >= pi and
            (right_end + 3 * pi/2) % (2*pi) <= 2 * pi):
            information = information | create_information_from_list(['increasing'])
        
        if (interval.width() <= pi and 
            left_end >= 0-1e-9 and
            right_end <= pi):
            information = information | create_information_from_list(['concave'])

        if (interval.width() <= pi and 
            left_end >= pi and
            right_end <= 2 * pi):
            information = information | create_information_from_list(['convex'])
        
        composition_information = ExpressionPropagator.get_composition_information(
            information,
            expression.expression_information
        )
        return ExpressionPropagator(
            expression_information=composition_information,
            interval=Interval.sin(interval)
        )
    
    @staticmethod
    def cos(expression):
        if not isinstance(expression, ExpressionPropagator):
            return Interval.cos(expression)
        
        interval = expression.interval

        information = ExpressionInformation()
        pi = Decimal(np.pi)

        left_end = (interval[0] % (2*pi) + 2*pi) % (2*pi)
        right_end = (interval[1] % (2*pi) + 2*pi) % (2*pi)
        if (interval.width() <= pi and 
            left_end >= pi / 2 and
            right_end <= 3 * pi / 2):
            information = information | create_information_from_list(['convex'])
        
        if (interval.width() <= pi and 
            (left_end + 3 * pi/2) % (2*pi) >= pi and
            (right_end + 3 * pi/2) % (2*pi) <= 2 * pi):
            information = information | create_information_from_list(['concave'])
        
        if (interval.width() <= pi and 
            left_end >= 0-1e-9 and
            right_end <= pi):
            information = information | create_information_from_list(['decreasing'])

        if (interval.width() <= pi and 
            left_end >= pi and
            right_end <= 2 * pi):
            information = information | create_information_from_list(['increasing'])
        

        composition_information = ExpressionPropagator.get_composition_information(
            information,
            expression.expression_information
        )

        return ExpressionPropagator(
            expression_information=composition_information,
            interval=Interval.cos(interval)
        )
    
    @staticmethod
    def exp(expression):
        if not isinstance(expression, ExpressionPropagator):
            return Interval.exp(expression)
        
        information = create_information_from_list(['increasing', 'convex'])
        composition_information = ExpressionPropagator.get_composition_information(
            information,
            expression.expression_information
        )
        return ExpressionPropagator(
            expression_information=composition_information,
            interval=Interval.exp(expression.interval)
        )
    
    @staticmethod
    def ln(expression):
        if not isinstance(expression, ExpressionPropagator):
            return Interval.ln(expression)
        
        information = create_information_from_list(['increasing', 'concave'])
        composition_information = ExpressionPropagator.get_composition_information(
            information,
            expression.expression_information
        )
        return ExpressionPropagator(
            expression_information=composition_information,
            interval=Interval.ln(expression.interval)
        )
    
    @staticmethod
    def abs(expression):
        if not isinstance(expression, ExpressionPropagator):
            return abs(Interval.valueToInterval(expression))
        
        if expression.interval > 0:
            information = create_information_from_list(['increasing', 'convex', 'concave'])
        elif expression.interval < 0:
            information = create_information_from_list(['decreasing', 'convex', 'concave'])
        else:
            information = create_information_from_list(['convex'])
        
        composition_information = ExpressionPropagator.get_composition_information(
            information,
            expression.expression_information
        )
        return ExpressionPropagator(
            expression_information=composition_information,
            interval=abs(expression.interval)
        )
    
    def propagate_bounds(self):
        information = ExpressionInformation()
        if self.interval >= 0:
            information.sign_information.is_nonnegative = True
            if self.interval > 0:
                information.sign_information.is_positive = True
        if self.interval <= 0:
            information.sign_information.is_negative = True
            if self.interval < 0:
                information.sign_information.is_nonpositive = True
        self.expression_information = self.expression_information | information 



    @staticmethod
    def get_composition_information(external_expression_information: ExpressionInformation, 
                                    internal_expression_information: ExpressionInformation):
        result = ExpressionInformation()
        for rule in composition_rule_set:
            if (rule.condition_on_first <= external_expression_information and
                rule.condition_on_second <= internal_expression_information):
                result = result | rule.result
        return result

def create_propagator_from_list(statements: List[str], interval=None):
    information = create_information_from_list(statements)
    return ExpressionPropagator(
        expression_information=information,
        interval=interval
    )
