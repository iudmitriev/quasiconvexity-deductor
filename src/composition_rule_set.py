from src.rule import Rule, UnaryRule
from src.information import create_information_from_list

composition_rule_set = [
    Rule(
            condition_on_first=create_information_from_list(['increasing']),
            condition_on_second=create_information_from_list(['increasing']),
            result=create_information_from_list(['increasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['nondecreasing']),
            condition_on_second=create_information_from_list(['nondecreasing']),
            result=create_information_from_list(['nondecreasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['increasing']),
            condition_on_second=create_information_from_list(['decreasing']),
            result=create_information_from_list(['decreasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['nondecreasing']),
            condition_on_second=create_information_from_list(['nonincreasing']),
            result=create_information_from_list(['nonincreasing'])
    ),

    Rule(
            condition_on_first=create_information_from_list(['decreasing']),
            condition_on_second=create_information_from_list(['increasing']),
            result=create_information_from_list(['decreasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['nonincreasing']),
            condition_on_second=create_information_from_list(['nondecreasing']),
            result=create_information_from_list(['nonincreasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['decreasing']),
            condition_on_second=create_information_from_list(['decreasing']),
            result=create_information_from_list(['increasing'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['nonincreasing']),
            condition_on_second=create_information_from_list(['nonincreasing']),
            result=create_information_from_list(['nondecreasing'])
    ),
    
    Rule(
            condition_on_first=create_information_from_list(['strict_convex', 'nondecreasing']),
            condition_on_second=create_information_from_list(['strict_convex']),
            result=create_information_from_list(['strict_convex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['convex', 'nondecreasing']),
            condition_on_second=create_information_from_list(['convex']),
            result=create_information_from_list(['convex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['strict_convex', 'nonincreasing']),
            condition_on_second=create_information_from_list(['strict_concave']),
            result=create_information_from_list(['strict_convex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['convex', 'nonincreasing']),
            condition_on_second=create_information_from_list(['concave']),
            result=create_information_from_list(['convex'])
    ),

    Rule(
            condition_on_first=create_information_from_list(['strict_concave', 'nonincreasing']),
            condition_on_second=create_information_from_list(['strict_convex']),
            result=create_information_from_list(['strict_concave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['concave', 'nonincreasing']),
            condition_on_second=create_information_from_list(['convex']),
            result=create_information_from_list(['concave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['strict_concave', 'nondecreasing']),
            condition_on_second=create_information_from_list(['strict_concave']),
            result=create_information_from_list(['strict_concave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['concave', 'nondecreasing']),
            condition_on_second=create_information_from_list(['concave']),
            result=create_information_from_list(['concave'])
    ),

    Rule(
            condition_on_first=create_information_from_list(['nondecreasing']),
            condition_on_second=create_information_from_list(['quasiconvex']),
            result=create_information_from_list(['quasiconvex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['increasing']),
            condition_on_second=create_information_from_list(['strict_quasiconvex']),
            result=create_information_from_list(['strict_quasiconvex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['increasing']),
            condition_on_second=create_information_from_list(['semistrict_quasiconvex']),
            result=create_information_from_list(['semistrict_quasiconvex'])
    ),

    Rule(
            condition_on_first=create_information_from_list(['nonincreasing']),
            condition_on_second=create_information_from_list(['quasiconcave']),
            result=create_information_from_list(['quasiconcave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['decreasing']),
            condition_on_second=create_information_from_list(['strict_quasiconcave']),
            result=create_information_from_list(['strict_quasiconcave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['decreasing']),
            condition_on_second=create_information_from_list(['semistrict_quasiconcave']),
            result=create_information_from_list(['semistrict_quasiconcave'])
    ),

    Rule(
            condition_on_first=create_information_from_list(['quasiconvex']),
            condition_on_second=create_information_from_list(['monotonic']),
            result=create_information_from_list(['quasiconvex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['strict_quasiconvex']),
            condition_on_second=create_information_from_list(['monotonic']),
            result=create_information_from_list(['strict_quasiconvex'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['quasiconcave']),
            condition_on_second=create_information_from_list(['monotonic']),
            result=create_information_from_list(['quasiconcave'])
    ),
    Rule(
            condition_on_first=create_information_from_list(['strict_quasiconcave']),
            condition_on_second=create_information_from_list(['monotonic']),
            result=create_information_from_list(['strict_quasiconcave'])
    )
]
