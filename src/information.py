from __future__ import annotations

from dataclasses import dataclass, field
from types import UnionType
from typing import Any

@dataclass
class MonotonicInformation:
    is_monotonic: bool = False
    is_increasing: bool = False
    is_nondecreasing: bool = False
    is_decreasing: bool = False
    is_nonincreasing: bool = False
    is_constant: bool = False
 
    def __or__(self, other) -> MonotonicInformation:
        return MonotonicInformation(
            is_monotonic=self.is_monotonic or other.is_monotonic,
            is_increasing=self.is_increasing or other.is_increasing,
            is_nondecreasing=self.is_nondecreasing or other.is_nondecreasing,
            is_decreasing=self.is_decreasing or other.is_decreasing,
            is_nonincreasing=self.is_nonincreasing or other.is_nonincreasing,
            is_constant = self.is_constant or other.is_constant
        )
    
    def __le__(self, other) -> bool:
        return (
            self.is_monotonic <= other.is_monotonic and
            self.is_increasing <= other.is_increasing and  
            self.is_nondecreasing <= other.is_nondecreasing and    
            self.is_decreasing <= other.is_decreasing and
            self.is_nonincreasing <= other.is_nonincreasing and
            self.is_constant <= other.is_constant
        )
    
    def __str__(self) -> str:
        fields = [field for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))
                     and getattr(self, field)]
        return ', '.join(fields)

@dataclass
class ConvexityInformation:
    is_convex: bool = False
    is_concave: bool = False
    is_strict_convex: bool = False
    is_strict_concave: bool = False

    def __or__(self, other) -> ConvexityInformation:
        return ConvexityInformation(
            is_convex=self.is_convex or other.is_convex,
            is_concave=self.is_concave or other.is_concave,
            is_strict_convex=self.is_strict_convex or other.is_strict_convex,
            is_strict_concave=self.is_strict_concave or other.is_strict_concave,
        )

    def __le__(self, other) -> bool:
        return (
            self.is_convex <= other.is_convex and
            self.is_concave <= other.is_concave and
            self.is_strict_convex <= other.is_strict_convex and
            self.is_strict_concave <= other.is_strict_concave
        )
    
    def __str__(self) -> str:
        fields = [field for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))
                     and getattr(self, field)]
        return ', '.join(fields)

@dataclass
class QuasiconvexityInformation:
    is_quasiconvex: bool = False
    is_quasiconcave: bool = False

    def __or__(self, other) -> QuasiconvexityInformation:
        return QuasiconvexityInformation(
            is_quasiconvex=self.is_quasiconvex or other.is_quasiconvex,
            is_quasiconcave=self.is_quasiconcave or other.is_quasiconcave
        )
    
    def __le__(self, other) -> bool:
        return (
            self.is_quasiconvex <= other.is_quasiconvex and
            self.is_quasiconcave <= other.is_quasiconcave  
        )
    
    def __str__(self) -> str:
        fields = [field for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))
                     and getattr(self, field)]
        return ', '.join(fields)

@dataclass
class StrictQuasiconvexityInformation:
    is_strict_quasiconvex: bool = False
    is_strict_quasiconcave: bool = False
    is_semistrict_quasiconvex: bool = False
    is_semistrict_quasiconcave: bool = False

    def __or__(self, other) -> StrictQuasiconvexityInformation:
        return StrictQuasiconvexityInformation(
            is_strict_quasiconvex=self.is_strict_quasiconvex or other.is_strict_quasiconvex,
            is_strict_quasiconcave=self.is_strict_quasiconcave or other.is_strict_quasiconcave,
            is_semistrict_quasiconvex=self.is_semistrict_quasiconvex or other.is_semistrict_quasiconvex,
            is_semistrict_quasiconcave=self.is_semistrict_quasiconcave or other.is_semistrict_quasiconcave
        )

    def __le__(self, other) -> bool:
        return (
            self.is_strict_quasiconvex <= other.is_strict_quasiconvex and
            self.is_strict_quasiconcave <= other.is_strict_quasiconcave and  
            self.is_semistrict_quasiconvex <= other.is_semistrict_quasiconvex and    
            self.is_semistrict_quasiconcave <= other.is_semistrict_quasiconcave    
        )
    
    def __str__(self) -> str:
        fields = [field for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))
                     and getattr(self, field)]
        return ', '.join(fields)
    

@dataclass
class SignInformation:
    is_positive: bool = False
    is_negative: bool = False
    is_nonnegative: bool = False
    is_nonpositive: bool = False

    def __or__(self, other) -> SignInformation:
        return SignInformation(
            is_positive=self.is_positive or other.is_positive,
            is_negative=self.is_negative or other.is_negative,
            is_nonnegative=self.is_nonnegative or other.is_nonnegative,
            is_nonpositive=self.is_nonpositive or other.is_nonpositive
        )

    def __le__(self, other) -> bool:
        return (
            self.is_positive <= other.is_positive and
            self.is_negative <= other.is_negative and  
            self.is_nonnegative <= other.is_nonnegative and    
            self.is_nonpositive <= other.is_nonpositive    
        )
    
    def __str__(self) -> str:
        fields = [field for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))
                     and getattr(self, field)]
        return ', '.join(fields)

@dataclass
class ExpressionInformation:
    monotonic_information: MonotonicInformation = field(default_factory=MonotonicInformation)
    convexity_information: ConvexityInformation = field(default_factory=ConvexityInformation)
    quasiconvexity_information: QuasiconvexityInformation = field(default_factory=QuasiconvexityInformation)
    strictquasiconvexity_information: StrictQuasiconvexityInformation = field(default_factory=StrictQuasiconvexityInformation)
    sign_information: SignInformation = field(default_factory=SignInformation)

    def __or__(self, other) -> ExpressionInformation:
        return ExpressionInformation(
            monotonic_information=self.monotonic_information | other.monotonic_information,
            convexity_information=self.convexity_information | other.convexity_information,
            quasiconvexity_information=self.quasiconvexity_information | other.quasiconvexity_information,
            strictquasiconvexity_information=self.strictquasiconvexity_information | other.strictquasiconvexity_information,
            sign_information=self.sign_information | other.sign_information
        )
    
    def __le__(self, other) -> bool:
        return (
            self.monotonic_information <= other.monotonic_information and
            self.convexity_information <= other.convexity_information and  
            self.quasiconvexity_information <= other.quasiconvexity_information and    
            self.strictquasiconvexity_information <= other.strictquasiconvexity_information and
            self.sign_information <= other.sign_information
        )
    
    def __str__(self) -> str:
        fields = [str(getattr(self, field)) for field in dir(self) 
                  if not field.startswith('__') and not callable(getattr(self, field))]
        fields = [field for field in fields if field]
        return ', '.join(fields)
    
    def propagate_information(self) -> None:
        if self.monotonic_information.is_increasing:
            self.monotonic_information.is_nondecreasing = True

        if self.monotonic_information.is_decreasing:
            self.monotonic_information.is_nonincreasing = True

        if self.monotonic_information.is_constant:
            self.monotonic_information.is_nondecreasing = True
            self.monotonic_information.is_nonincreasing = True
            self.convexity_information.is_convex = True
            self.convexity_information.is_concave = True

        if (self.monotonic_information.is_nondecreasing or
            self.monotonic_information.is_nonincreasing):
            self.monotonic_information.is_monotonic = True

        if (self.monotonic_information.is_nondecreasing and
            self.monotonic_information.is_nonincreasing):
            self.monotonic_information.is_constant = True
        
    
        if self.monotonic_information.is_monotonic:
            self.quasiconvexity_information.is_quasiconvex = True
            self.quasiconvexity_information.is_quasiconcave = True

        if self.convexity_information.is_strict_convex:
            self.convexity_information.is_convex = True
            self.strictquasiconvexity_information.is_strict_quasiconvex = True

        if self.convexity_information.is_strict_concave:
            self.convexity_information.is_concave = True
            self.strictquasiconvexity_information.is_strict_quasiconcave = True

        if (self.convexity_information.is_convex or
            self.strictquasiconvexity_information.is_strict_quasiconvex):
            self.quasiconvexity_information.is_quasiconvex = True
            self.strictquasiconvexity_information.is_semistrict_quasiconvex = True
        if (self.convexity_information.is_concave or
            self.strictquasiconvexity_information.is_strict_quasiconcave):
            self.quasiconvexity_information.is_quasiconcave = True
            self.strictquasiconvexity_information.is_semistrict_quasiconcave = True

        if self.sign_information.is_positive:
            self.sign_information.is_nonnegative = True
        if self.sign_information.is_negative:
            self.sign_information.is_nonpositive = True


def create_information_from_list(statements):
    information = ExpressionInformation()
    for statement in statements:
        if statement in ['monotonic', 'increasing', 'nondecreasing', 
                         'decreasing', 'nonincreasing', 'constant']:
            setattr(information.monotonic_information, f'is_{statement}', True)
        elif statement in ['convex', 'concave', 'strict_convex', 'strict_concave']:
            setattr(information.convexity_information, f'is_{statement}', True)
        elif statement in ['quasiconvex', 'quasiconcave']:
            setattr(information.quasiconvexity_information, f'is_{statement}', True)
        elif statement in ['strict_quasiconvex', 'strict_quasiconcave', 
                           'semistrict_quasiconvex', 'semistrict_quasiconcave']:
            setattr(information.strictquasiconvexity_information, f'is_{statement}', True)
        elif statement in ['positive', 'negative', 
                           'nonnegative', 'nonpositive']:
            setattr(information.sign_information, f'is_{statement}', True)
        else:
            raise ValueError(f'Unknown information: {statement}')
    information.propagate_information()
    return information
