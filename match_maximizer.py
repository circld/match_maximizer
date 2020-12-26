from typing import Callable, List, Sequence, Tuple

# type aliases
Contribution = float
Match = float
CompanyMatch = Sequence[Tuple[Contribution, Match]]


def calculate_match(
    pp_salary: float, contrib_pct: Contribution, match_pct: Match
) -> Callable[[float], float]:
    def calc_match(amt: float) -> float:
        contrib_amt = pp_salary * contrib_pct
        match_amt = min(amt, contrib_amt) * match_pct
        return match_amt

    return calc_match


def frontload_remainder(
    pay_period_contribs: List[float], target_contrib: float, pp_salary: float
) -> List[float]:
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


def maximize_match(
    pay_period_contribs: List[float],
    target_contrib: float,
    pp_limit: float,
    calc_match: Callable[[float], float],
) -> Tuple[float, float, List[float]]:
    contributions = pay_period_contribs[:]
    total_match = 0.0
    for idx in range(len(contributions)):
        if target_contrib - pp_limit > 0.0:
            target_contrib -= pp_limit
            contributions[idx] += pp_limit
            total_match += calc_match(pp_limit)
        else:
            contributions[idx] += target_contrib
            total_match += calc_match(target_contrib)
            target_contrib = 0.0
            break
    return target_contrib, total_match, contributions


def per_pay_period_salary(salary: int, pay_periods: int) -> float:
    return float(salary) / pay_periods


def per_pay_period_limit(pp_salary: float, contrib_pct: Contribution) -> float:
    return pp_salary * contrib_pct


# FIXME refactor to return correct total match
def recommend_uniform(target: int, pay_periods: int) -> Tuple[float, List[float]]:
    return (float(target), [float(target) / pay_periods] * pay_periods)


def recommend_optimized(
    salary: int, pay_periods: int, match: CompanyMatch, target_contrib: float
) -> Tuple[float, List[float]]:
    pp_salary = per_pay_period_salary(salary, pay_periods)

    pay_period_contribs = [0.0] * pay_periods
    total_match = 0.0

    # first pass: max out match (at each match level)
    for contrib_pct, match_pct in match:
        calc_match = calculate_match(pp_salary, contrib_pct, match_pct)
        pp_limit = per_pay_period_limit(pp_salary, contrib_pct)
        target_contrib, total_match_, pay_period_contribs = maximize_match(
            pay_period_contribs, target_contrib, pp_limit, calc_match
        )
        total_match += total_match_

    # second pass: distribute the rest (frontload)
    if target_contrib > 0:
        pay_period_contribs = frontload_remainder(
            pay_period_contribs, target_contrib, pp_salary
        )

    return total_match, pay_period_contribs
