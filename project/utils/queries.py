#!/usr/bin/env python
import operator


def runQuery(toBeChecked, operatorChoice, criteria):
    ops = {
        "==": operator.eq,
        "=<": operator.le,
        ">=": operator.ge,
        ">": operator.gt,
        "<": operator.lt,
    }

    return ops[operatorChoice](toBeChecked, criteria)
