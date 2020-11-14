#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


# FIXME update call signature once company match args input format clarified
def display_company_strategy(*args):
    pass


# - pay periods (semi-monthly, monthly)
# - per pay period pay
# - company match % (e.g., -m 1 .03 -m 0.5 0.02)
#   (include match approach in printed output)
# - target *annual* contribution
# - flag to optimize (false means easier of administration)
def parse_args():
    pass


def recommend_optimized():
    pass


def recommend_even():
    pass


def main(args):

    # print company match strategy and target contribution
    # FIXME update once `parse_args` is implementemed
    print(args)

    # calculate recommended contributions for every pay period
    total, recommendation = (recommend_optimized()
                             if args.optimize else recommend_even())

    # print recommendation + total company match
    # FIXME update once arg naming is settled
    print(recommendation)


if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args))
