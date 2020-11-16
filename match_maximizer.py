#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Callable, List, NewType, Tuple

Contribution = NewType('Contribution', float)
Match = NewType('Match', float)
CompanyMatch = NewType('CompanyMatch', Tuple[Tuple[Contribution, Match]])


def calculate_match(pp_salary: float,
                    company_match: CompanyMatch) -> Callable[[float], float]:
    def calc_match(amt: float) -> float:
        match_amt = 0.
        for contrib_pct, match_pct in company_match:
            contrib_amt = pp_salary * contrib_pct
            match_amt += min(amt, contrib_amt) * match_pct
            amt -= contrib_amt
            if amt <= 0:
                break
        return match_amt

    return calc_match


def display_company_strategy(*args):
    NotImplemented


def frontload_remainder(pay_period_contribs: List[float], target_contrib,
                        pp_salary) -> List[float]:
    contributions = pay_period_contribs[:]
    for idx, pp_amt in enumerate(contributions):
        remainder = pp_salary - pp_amt
        if target_contrib - remainder > 0:
            target_contrib -= remainder
            contributions[idx] += remainder
        else:
            contributions[idx] += target_contrib
            target_contrib = 0
    return contributions


# FIXME we actually need iterate through for each match level to ensure we max
# out the highest match % *first*
def maximize_match(
        pay_period_contribs: List[float], target_contrib: float,
        pp_limit: float,
        calc_match: Callable[[float],
                             float]) -> Tuple[float, float, List[float]]:
    contributions = pay_period_contribs[:]
    total_match = 0.
    for idx in range(len(contributions)):
        if target_contrib - pp_limit > 0.:
            target_contrib -= pp_limit
            contributions[idx] += pp_limit
            total_match += calc_match(pp_limit)
        else:
            contributions[idx] += target_contrib
            total_match += calc_match(target_contrib)
            target_contrib = 0.
            break
    return target_contrib, total_match, contributions


def per_pay_period_salary(salary: int, pay_periods: int) -> float:
    return float(salary) / pay_periods


def per_pay_period_limit(pp_salary, match: CompanyMatch) -> float:
    limit = 0
    for contrib_pct, _ in match:
        limit += pp_salary * contrib_pct
    return limit


def recommend_even(salary: int, pay_periods: int) -> List[float]:
    return [float(salary) / pay_periods] * pay_periods


def recommend_optimized(salary: int, pay_periods: int, match: CompanyMatch,
                        target_contrib: float) -> Tuple[float, List[float]]:
    pp_salary = per_pay_period_salary(salary, pay_periods)
    pp_limit = per_pay_period_limit(pp_salary, match)
    calc_match = calculate_match(pp_salary, match)

    pay_period_contribs = [0.] * pay_periods

    # first pass: max out match
    target_contrib, total_match, pay_period_contribs = maximize_match(
        pay_period_contribs, target_contrib, pp_limit, calc_match)

    # second pass: distribute the rest (frontload)
    if target_contrib > 0:
        pay_period_contribs = frontload_remainder(pay_period_contribs,
                                                  target_contrib, pp_salary)

    return total_match, pay_period_contribs
