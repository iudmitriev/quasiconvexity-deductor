from dataclasses import dataclass

from src.information import ExpressionInformation

@dataclass
class Rule:
    condition_on_first: ExpressionInformation
    condition_on_second: ExpressionInformation
    result: ExpressionInformation

@dataclass
class UnaryRule:
    condition: ExpressionInformation
    result: ExpressionInformation
