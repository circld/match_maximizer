import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import match_maximizer.cli as cli


def test_parse_company_match() -> None:
    args = ["0.05", "1", "0.03", ".5"]
    expected: cli.mm.CompanyMatch = ((0.05, 1.0), (0.03, 0.5))
    actual = cli.parse_company_match(args)
    assert expected == actual


def test_target_bigger_than_salary() -> None:
    args = cli.ap.Namespace(
        pay_periods=12,
        company_match=("0.09", "1.0"),
        optimize=False,
        salary=12000,
        target_contribution=120000,
    )
    actual = cli.main(args)

    expected = (12000.0 + 1080.0, 1080.0, [1000.0] * 12)
    assert expected == actual


def test_no_optimized() -> None:
    args = cli.ap.Namespace(
        pay_periods=12,
        company_match=("0.09", "1.0"),
        optimize=False,
        salary=12000,
        target_contribution=1200,
    )
    actual = cli.main(args)

    expected = (1200.0 + 1080.0, 1080.0, [100.0] * 12)
    assert expected == actual


def test_optimized() -> None:
    args = cli.ap.Namespace(
        pay_periods=12,
        company_match=("0.09", "1.0"),
        optimize=True,
        salary=12000,
        target_contribution=1200,
    )
    actual = cli.main(args)

    expected = (1200.0 + 1080.0, 1080.0, [210.0] + [90.0] * 11)
    assert expected == actual
