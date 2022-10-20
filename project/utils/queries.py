#!/usr/bin/env python
import operator


def run_query(to_be_checked, operator_choice, criteria):
    ops = {
        "==": operator.eq,
        "=<": operator.le,
        ">=": operator.ge,
        ">": operator.gt,
        "<": operator.lt,
    }

    return ops[operator_choice](to_be_checked, criteria)
