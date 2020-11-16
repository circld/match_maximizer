import match_maximizer as mm


def test_calc_match():
    calc_match = mm.calculate_match(1200, ((.05, 0.5), (.05, 0.25)))
    assert 20. == calc_match(40.)
    assert 32.5 == calc_match(70.)
    assert 45. == calc_match(1200.)


def test_maximize_match_maxed():
    pp_limit = 100
    target_contrib = 5000
    pay_period_contribs = [0.] * 12
    calc_match = mm.calculate_match(1000, ((.1, 1.), (.1, 0.5)))
    contributions = mm.maximize_match(pay_period_contribs, target_contrib,
                                      pp_limit, calc_match)
    assert (3800, 1200., [100.] * 12) == contributions


def test_maximize_match_not_maxed():
    pp_limit = 350.
    target_contrib = 4000
    pay_period_contribs = [0.] * 12
    calc_match = mm.calculate_match(5000, ((.05, 1.), (.02, 0.5)))
    contributions = mm.maximize_match(pay_period_contribs, target_contrib,
                                      pp_limit, calc_match)
    assert (0., 3500., [350.] * 11 + [150.]) == contributions


def test_per_pay_period_salary():
    assert 112.5 == mm.per_pay_period_salary(900, 8)


def test_per_pay_period_limit():
    salary = 3000
    company_match = ((.03, 1.), (.02, .5))
    assert 150 == mm.per_pay_period_limit(salary, company_match)


def test_recommend_optimized():
    salary = 60000
    pay_periods = 24
    company_match = ((.03, 1.), (.02, .5))
    target_contrib = 19500
    total_match, recommendation = mm.recommend_optimized(
        salary, pay_periods, company_match, target_contrib)
    expected = [2500.0] * 6 + [2375.] + [125.] * 17
    assert expected == recommendation
    assert target_contrib == sum(recommendation)
    assert 0 == total_match


def test_recommend_even():
    assert [2750] * 12 == mm.recommend_even(33000, 12)
