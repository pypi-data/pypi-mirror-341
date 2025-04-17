from sympy import Array, Expr, Symbol
from sympy.physics.units import convert_to, Quantity
from functools import lru_cache
from typing import Union

import sympy as sp

_sum_square = lambda array: sum(i ** 2 for i in array)

class Measurement(Symbol):
    values: Array
    uB_array: Array
    def __new__(cls, name: str, values, unit: Quantity, uB = []):
        obj = super().__new__(cls, name)
        obj.values = Array(values) * unit
        obj.uB_array = Array(uB) * unit
        return obj

    @property
    @lru_cache
    def mean(self) -> Expr:
        return sum(self.values) / len(self.values)

    @lru_cache
    def _u(self, type):
        total_u2 = 0
        length = len(self.values)
        if "A" in type and length > 1:
            total_u2 += _sum_square(
                i - self.mean for i in self.values
            ) / length / (length - 1)
        if "B" in type:
            total_u2 += _sum_square(self.uB_array)
        return sp.sqrt(total_u2)

    @property
    def u(self):
        return self._u("AB")

def _mean(expr: Expr):
    if isinstance(expr, Measurement):
        return expr.mean
    return expr.subs({
        i: i.mean for i in expr.free_symbols
        if isinstance(i, Measurement)
    })

def _u(expr: Expr, type, margs=None):
    if isinstance(expr, Measurement):
        return expr._u(type)
    measurements = {
        i for i in expr.free_symbols
        if isinstance(i, Measurement)
    }
    return sp.sqrt(_sum_square(
        sp.diff(expr, i) * i._u(type) for i in measurements
        if not margs or i in margs
    )).subs({i: i.mean for i in measurements}).simplify()

class CombinedMeasurement(Measurement):
    expr: Expr
    def __new__(cls, name: str, expr: Expr, uB = []):
        obj = super().__new__(cls, name, _mean(expr), 1, uB)
        obj.expr = expr
        return obj

    @lru_cache
    def _u(self, type):
        u = _u(self.expr, type=type)
        if "B" in type and self.uB_array:
            u = sp.sqrt(u ** 2 + _sum_square(self.uB_array))
        return u

    @property
    def sub_measurements(self):
        return {
            i for i in self.expr.free_symbols
            if isinstance(i, Measurement)
        }

def mean(expr: Expr):
    return sp.N(_mean(expr))

def u(expr: Expr,
      type: str = "AB",
      margs: Union[Measurement, set[Measurement]] = None,
      n: int = 2):
    if isinstance(margs, Measurement):
        margs = {margs}
    return sp.N(_u(expr, type=type, margs=margs), n)

def uvalue(expr: Expr, n=2, units=None):
    mean_val, uncertainty = _mean(expr), _u(expr, type="AB")
    relative_uncertainty = sp.N(sp.simplify(uncertainty / mean_val), 4)
    if units is not None:
        mean_val = convert_to(mean_val, units)
        uncertainty = convert_to(uncertainty, units)
    def _get_exp(quan):
        num = quan.replace(lambda x: isinstance(x, Quantity), lambda _: 1)
        return sp.floor(sp.log(num, 10))
    uncertainty = sp.N(uncertainty, n)
    mean_val = sp.N(mean_val, n+_get_exp(mean_val)-_get_exp(uncertainty))
    return mean_val, uncertainty, relative_uncertainty

__all__ = [
    "Measurement",
    "CombinedMeasurement",
    "mean",
    "u",
    "uvalue"
]
