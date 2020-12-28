import argparse as ap

import match_maximizer.core as mm


# - pay periods (semi-monthly, monthly)
# - company match % (e.g., -m 1 .03 -m 0.5 0.02)
#   (include match approach in printed output)
# - target *annual* contribution
# - flag to optimize (false means easier of administration)
#
# $ python match_maximizer 50000 12 --company_match 1 .03 .5 .02 --frontload
def parse_args() -> ap.Namespace:
    parser = ap.ArgumentParser()
    parser.add_argument(
        "salary",
        help="Annual salary off of which company match is calculated against.",
        type=float,
    )
    parser.add_argument("pay_periods", help="Number of pay periods per year.")
    parser.add_argument(
        "target_contribution", help="Amount to contribute for the year.", type=float
    )
    parser.add_argument(
        "-o",
        "--optimize",
        action="store_true",
        help="Frontload contributions in addition to maximizing company match. Default: True",
    )
    parser.add_argument(
        "-m",
        "--company_match",
        help=" ".join(
            [
                "Company match. For instance, if your company matches 100%% up",
                "to 5%% and 50%% for the next 4%%, then you would enter:\n",
                "0.05 1 0.04 .5\n",
                "If not provided, it is assumed that there is no company match.",
            ]
        ),
        nargs="*",
    )
    return parser.parse_args()


def parse_company_match(args: mm.Sequence[str]) -> mm.CompanyMatch:
    n = len(args)
    if n % 2 != 0:
        raise ValueError(
            "Invalid number of arguments to --company_match. "
            "Input must include contribution limit, match percentage pairs."
        )
    floats = tuple(map(float, args))
    return tuple((floats[i], floats[i + 1]) for i in range(0, n, 2))


# TODO pretty formatting
def format_output(
    total_contribution: float, total_match: float, contributions: mm.List[float]
) -> str:
    return f"Total contribution: {total_contribution}\nTotal match: {total_match}\nContributions: {contributions}"


def main(args: ap.Namespace) -> mm.Tuple[float, float, mm.List[float]]:

    # if empty, assume no match
    company_match = (
        parse_company_match(args.company_match) if args.company_match else ((1.0, 0.0),)
    )

    # target cannot exceed salary
    target = min(args.salary, args.target_contribution)

    # select recommendation strategy
    recommend = mm.recommend_optimized if args.optimize else mm.recommend_uniform

    # calculate recommended contributions for every pay period
    total_contribution, total_match, recommendation = recommend(
        args.salary, args.pay_periods, company_match, target
    )

    return (total_contribution, total_match, recommendation)
