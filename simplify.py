import re
from re import Match
from typing import Dict, List

MONOMIAL_PATTERN = r"(-?)(\d?)(\D+)"


def get_factor_from_monomial(result: Match) -> int:
    """
    Gets number (factor) from single monomial
    :param result: regex matcher
    :return: extracted int from monomial string
    """
    found_factor = result.group(2)
    amount = 1 if not found_factor else int(found_factor)
    return amount if not result.group(1) else -1 * amount


def get_monomial(result: Match) -> str:
    """
    Gets monomial as string
    :param result: regex matcher
    :return: monomial string
    """
    return "".join(sorted(result.group(3)))


def sort_monomials(monomials: Dict[str, int]) -> Dict[str, int]:
    """
    Sorts monomials. For example a+bc-d -> {"a": 1, "d": -1, "bc": 1}
    :param monomials: found monomials
    :return: Sorted monomials as dictionary
    """
    monomial_sorted_increasing = {k: v for k, v in sorted(monomials.items(), key=lambda item: len(item[0]))}
    if len(monomial_sorted_increasing.values()) > len(set([len(value) for value in monomial_sorted_increasing.keys()])):
        return sort_monomial_in_lexicographic_order(monomial_sorted_increasing=monomial_sorted_increasing)
    return monomial_sorted_increasing


def sort_monomial_in_lexicographic_order(monomial_sorted_increasing: Dict[str, int]) -> Dict[str, int]:
    """
    Sorts monomial in lexicographic order. For example {'c': 1, 'a': 1, 'd': 1} -> {1: ['a', 'c', 'd']}
    :param monomial_sorted_increasing:
    :return: sorted monomial dict
    """
    monomials_length = get_monomial_length(monomial_sorted_increasing=monomial_sorted_increasing)
    return {val: monomial_sorted_increasing[val] for vals in monomials_length.values() for val in vals}


def get_monomial_length(monomial_sorted_increasing: Dict[str, int]) -> Dict[int, List[str]]:
    """
    Gets monomial lengths in lexicographic order. For example {'a': 1, 'ac': 1, 'ab': -2} -> {1: ['a'], 2: ['ac', 'ab']}
    :param monomial_sorted_increasing: monomial sorted increasing
    :return: Dict with all monomials length
    """
    monomials_length = {}
    for key in monomial_sorted_increasing.keys():
        key_length = len(key)
        if key_length in monomials_length:
            monomials_length[key_length].append(key)
        else:
            monomials_length[key_length] = [key]
    return {key: sorted(values) for key, values in monomials_length.items()}


def get_prepared_monomials(poly_as_string: str) -> Dict[str, int]:
    """
    Gets prepared monomials as dict. For example 'a+ac-2ab' -> {'a': 1, 'ab': -2, 'ac': 1}
    :param poly_as_string: poly as string
    :return: converted monomials
    """

    monomials = {}
    poly_parts = [part for part in poly_as_string.replace("-", "+-").split("+") if part]
    for part in poly_parts:
        result = re.search(MONOMIAL_PATTERN, part)
        monomial_factor = get_factor_from_monomial(result=result)
        monomial = get_monomial(result=result)
        if monomial in monomials:
            monomials[monomial] += monomial_factor
        else:
            monomials[monomial] = monomial_factor
    monomials_without_zero = {k: v for k, v in monomials.items() if v}
    return sort_monomials(monomials_without_zero)


def get_sing_as_character(number: int, index: int) -> str:
    """
    Gets number as string
    :param number: int number
    :param index: index of monomial in polynomial
    :return: number as string
    """
    if number < 0:
        return f"{number}"
    if index == 0:
        if number != 1:
            return f"{number}"
        else:
            return ""
    return f"+{number}"


def simplify(poly):
    prepared_monomials = get_prepared_monomials(poly_as_string=poly)
    return_string = "".join([f"{get_sing_as_character(number=v, index=index)}{k}" for index, (k, v) in
                             enumerate(prepared_monomials.items())]).replace("1", "")
    return return_string
