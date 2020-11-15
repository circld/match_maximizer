#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple

Contribution, Match = float, float
CompanyMatch = Tuple[Tuple[Contribution, Match]]


def display_company_strategy(*args):
    pass


def maximize_match(pay_period_contribs, target_contrib, pp_limit):
    contributions = pay_period_contribs[:]
    for idx in range(len(contributions)):
        if target_contrib - pp_limit > 0:
            target_contrib -= pp_limit
            contributions[idx] += pp_limit
        else:
            contributions[idx] += target_contrib
            target_contrib = 0

    return target_contrib, contributions


def frontload_remainder(pay_period_contribs, target_contrib, pp_salary):
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


def per_pay_period_salary(salary: int, pay_periods: int):
    return float(salary) / pay_periods


def per_pay_period_limit(pp_salary, match: CompanyMatch):
    limit = 0
    for contrib_pct, _ in match:
        limit += pp_salary * contrib_pct
    return limit


def recommend_optimized(salary: int, pay_periods: int, match: CompanyMatch,
                        target_contrib: float):
    pp_salary = per_pay_period_salary(salary, pay_periods)
    pp_limit = per_pay_period_limit(pp_salary, match)

    pay_period_contribs = [0] * pay_periods

    # first pass: max out match
    target_contrib, pay_period_contribs = maximize_match(
        pay_period_contribs, target_contrib, pp_limit)

    # second pass: distribute the rest (frontload)
    if target_contrib > 0:
        pay_period_contribs = frontload_remainder(pay_period_contribs,
                                                  target_contrib, pp_salary)

    return pay_period_contribs


def recommend_even(salary: int, pay_periods: int):
    return [float(salary) / pay_periods] * pay_periods
