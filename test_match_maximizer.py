import match_maximizer as mm


def test_calc_match():
    calc_match = mm.calculate_match(1200, .05, 0.5)
    assert 20. == calc_match(40.)
    assert 30. == calc_match(70.)


def test_maximize_match():
    pp_limit = 100
    target_contrib = 5000
    pay_period_contribs = [0.] * 12
    calc_match = mm.calculate_match(1000, .1, .5)
    contributions = mm.maximize_match(pay_period_contribs, target_contrib,
                                      pp_limit, calc_match)
    assert (3800, 600., [100.] * 12) == contributions


def test_per_pay_period_salary():
    assert 112.5 == mm.per_pay_period_salary(900, 8)


def test_per_pay_period_limit():
    assert 90 == mm.per_pay_period_limit(3000, .03)


def test_recommend_optimized_maxed():
    salary = 60000
    pay_periods = 24
    company_match = ((.03, 1.), (.02, .5))
    target_contrib = 19500
    expected_total_match = salary * 0.04
    total_match, recommendation = mm.recommend_optimized(
        salary, pay_periods, company_match, target_contrib)
    expected = [2500.0] * 6 + [2375.] + [125.] * 17
    assert target_contrib == sum(recommendation)
    assert expected_total_match == total_match
    assert expected == recommendation


def test_recommend_optimized_not_maxed():
    salary = 60000
    pay_periods = 24
    company_match = ((.03, 1.), (.02, .5))
    target_contrib = 2000
    total_match, recommendation = mm.recommend_optimized(
        salary, pay_periods, company_match, target_contrib)
    expected = [125.0] * 4 + [75.] * 20
    assert target_contrib == sum(recommendation)
    assert 1900 == total_match
    assert expected == recommendation


def test_recommend_even():
    assert [2750] * 12 == mm.recommend_even(33000, 12)
