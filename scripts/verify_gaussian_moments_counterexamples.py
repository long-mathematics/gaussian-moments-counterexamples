#!/usr/bin/env python3
"""Exact symbolic checks for the GMC paper and the conservative JC -> GMC(158) bound.

Requires SymPy.  The finite moment checks are diagnostics; the paper's displayed
coefficient identities are the all-m proofs.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from math import factorial

import sympy as sp


def complex_gaussian_expectation(poly: sp.Expr, pairs: list[tuple[sp.Symbol, sp.Symbol]],
                                 real_vars: list[sp.Symbol] | None = None) -> sp.Expr:
    """Apply E(W^a Z^b)=delta_ab a! and standard-real Gaussian moments."""
    real_vars = real_vars or []
    variables = [u for pair in pairs for u in pair] + real_vars
    result = sp.Integer(0)
    for monom, coeff in sp.Poly(sp.expand(poly), *variables).terms():
        exps = dict(zip(variables, monom))
        moment = sp.Integer(1)
        for w, z in pairs:
            if exps[w] != exps[z]:
                moment = 0
                break
            moment *= factorial(exps[w])
        if moment == 0:
            continue
        for t in real_vars:
            e = exps[t]
            if e % 2:
                moment = 0
                break
            moment *= sp.factorial2(e - 1) if e else 1
        result += coeff * moment
    return sp.simplify(result)


def check_gmc_examples(max_m: int = 7) -> None:
    w1, z1, w2, z2 = sp.symbols("w1 z1 w2 z2")
    p4 = (1 + z2) * (w1 * (1 - z1) + w2)
    q4 = z2
    for m in range(1, max_m + 1):
        assert complex_gaussian_expectation(p4**m, [(w1, z1), (w2, z2)]) == 0
        assert complex_gaussian_expectation(q4 * p4**m, [(w1, z1), (w2, z2)]) == factorial(m)
        for a in range(4):
            lhs = complex_gaussian_expectation(z2**a * p4**m, [(w1, z1), (w2, z2)])
            rhs = factorial(m) * sp.expand(z2**a * (1 + z2) ** (m - 1)).coeff(z2, m)
            assert sp.simplify(lhs - rhs) == 0

    w, z, t = sp.symbols("w z t")
    p3 = (1 + z) * (w - sp.Rational(1, 2) * (2 + z) * t**2)
    q3 = z
    assert sp.expand(p3) == w + w*z - t**2 - sp.Rational(3, 2)*z*t**2 - sp.Rational(1, 2)*z**2*t**2
    for m in range(1, max_m + 1):
        assert complex_gaussian_expectation(p3**m, [(w, z)], [t]) == 0
        assert complex_gaussian_expectation(q3 * p3**m, [(w, z)], [t]) == factorial(m)
        for a in range(4):
            lhs = complex_gaussian_expectation(z**a * p3**m, [(w, z)], [t])
            rhs = factorial(m) * sp.expand(z**a * (1 + z) ** (m - 1)).coeff(z, m)
            assert sp.simplify(lhs - rhs) == 0


def announced_map_checks() -> Counter[int]:
    x, y, z = sp.symbols("x y z")
    f1 = (1 + 2*x*y)**3*z + 4*y**2*(1 + 2*x*y)*(2 + 3*x*y)
    f2 = y + 3*x*(1 + 2*x*y)**2*z + 12*x*y**2*(2 + 3*x*y)
    f3 = -x + 3*x**2*y + x**3*z
    F = sp.Matrix([f1, f2, f3])
    assert sp.factor(F.jacobian([x, y, z]).det()) == 1

    a = {x: 1, y: -sp.Rational(3, 4), z: sp.Rational(13, 4)}
    b = {x: -1, y: sp.Rational(3, 4), z: sp.Rational(13, 4)}
    assert F.subs(a) == F.subs(b)

    # Target normalization (u,v,w) -> (-w,v,u), whose determinant is 1.
    G = [sp.expand(-f3), sp.expand(f2), sp.expand(f1)]
    assert sp.Matrix(G).jacobian([x, y, z]).subs({x: 0, y: 0, z: 0}) == sp.eye(3)
    counts: Counter[int] = Counter()
    for g in G:
        for monom, coeff in sp.Poly(g, x, y, z).terms():
            d = sum(monom)
            if d >= 4 and coeff != 0:
                counts[d] += 1
    assert counts == Counter({4: 3, 5: 2, 6: 2, 7: 1})
    return counts


@lru_cache(None)
def c(d: int) -> int:
    """Balanced BCW monomial-reduction upper bounds used in the audit."""
    if d <= 3:
        return 0
    p = d // 2
    q = d - p
    # For d=5 this is 2+3; for d=7 it is 3+4.
    return 1 + c(p + 1) + c(q + 1) + c(p) + c(q)


def check_dimension_bound(counts: Counter[int]) -> tuple[int, int, int, int]:
    assert [c(d) for d in range(4, 8)] == [1, 2, 3, 5]
    steps = sum(counts[d] * c(d) for d in counts)
    degree_three_dimension = 3 + 2 * steps
    cubic_nilpotent_dimension = 2 * degree_three_dimension
    cubic_homogeneous_dimension = cubic_nilpotent_dimension + 1
    gmc_dimension = 2 * cubic_homogeneous_dimension
    assert (steps, degree_three_dimension, cubic_homogeneous_dimension, gmc_dimension) == (18, 39, 79, 158)
    return steps, degree_three_dimension, cubic_homogeneous_dimension, gmc_dimension


def main() -> None:
    check_gmc_examples()
    counts = announced_map_checks()
    steps, s, r, n = check_dimension_bound(counts)
    print("Exact finite moment checks passed for both GMC examples.")
    print("Announced map: det(JF)=1 and the stated collision is exact.")
    print(f"High-degree support counts: {dict(sorted(counts.items()))}")
    print(f"BCW degree-lowering steps <= {steps}; degree <= 3 dimension s = {s}.")
    print(f"Cubic-homogeneous dimension r = {r}; fixed-dimensional DVEZ/Zhao gives not GMC({n}).")


if __name__ == "__main__":
    main()
