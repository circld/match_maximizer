import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import match_maximizer.core as mm


def test_calc_match() -> None:
    calc_match = mm.calculate_match(1200, 0.05, 0.5)
    assert 20.0 == calc_match(40.0)
    assert 30.0 == calc_match(70.0)


def test_maximize_match() -> None:
    pp_limit = 100
    target_contrib = 5000
    pay_period_contribs = [0.0] * 12
    calc_match = mm.calculate_match(1000, 0.1, 0.5)
    contributions = mm.maximize_match(
        pay_period_contribs, target_contrib, pp_limit, calc_match
    )
    assert (3800, 600.0, [100.0] * 12) == contributions


def test_per_pay_period_salary() -> None:
    assert 112.5 == mm.per_pay_period_salary(900, 8)


def test_per_pay_period_limit() -> None:
    assert 90 == mm.per_pay_period_limit(3000, 0.03)


def test_recommend_optimized_maxed() -> None:
    salary = 60000
    pay_periods = 24
    company_match = ((0.03, 1.0), (0.02, 0.5))
    target_contrib = 19500
    expected_total_match = salary * 0.04
    total_contrib, total_match, recommendation = mm.recommend_optimized(
        salary, pay_periods, company_match, target_contrib
    )
    expected = [2500.0] * 6 + [2375.0] + [125.0] * 17
    assert total_contrib == target_contrib + total_match
    assert target_contrib == sum(recommendation)
    assert expected_total_match == total_match
    assert expected == recommendation


def test_recommend_optimized_not_maxed() -> None:
    salary = 60000
    pay_periods = 24
    company_match = ((0.03, 1.0), (0.02, 0.5))
    target_contrib = 2000
    total_contrib, total_match, recommendation = mm.recommend_optimized(
        salary, pay_periods, company_match, target_contrib
    )
    expected = [125.0] * 4 + [75.0] * 20
    assert total_contrib == target_contrib + total_match
    assert target_contrib == sum(recommendation)
    assert 1900 == total_match
    assert expected == recommendation


def test_recommend_uniform() -> None:
    assert (13200.0 + 1815.0, 1815.0, [660.0] * 20) == mm.recommend_uniform(
        33000, 20, ((0.03, 1.0), (0.05, 0.5)), 13200.0
    )
