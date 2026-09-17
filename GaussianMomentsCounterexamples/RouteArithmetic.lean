import Mathlib.Data.Nat.Basic
import Mathlib.Tactic.NormNum

/-! Numerical bounds from the manuscript's proposed reduction route.
These theorems establish the arithmetic implications of the displayed recurrence;
they do not construct Bass–Connell–Wright reductions or prove their preservation properties. -/

namespace GaussianMomentsCounterexamples

/-- The balanced degree splittings give the four stated upper bounds. -/
theorem balanced_recurrence_bounds (c : ℕ → ℕ)
    (h2 : c 2 = 0) (h3 : c 3 = 0)
    (h4 : c 4 ≤ 1 + c 3 + c 3 + c 2 + c 2)
    (h5 : c 5 ≤ 1 + c 3 + c 4 + c 2 + c 3)
    (h6 : c 6 ≤ 1 + c 4 + c 4 + c 3 + c 3)
    (h7 : c 7 ≤ 1 + c 4 + c 5 + c 3 + c 4) :
    c 4 ≤ 1 ∧ c 5 ≤ 2 ∧ c 6 ≤ 3 ∧ c 7 ≤ 5 := by omega

/-- The support multiplicities yield at most eighteen steps, assuming the step bounds. -/
theorem route_step_bound (c : ℕ → ℕ)
    (h4 : c 4 ≤ 1) (h5 : c 5 ≤ 2) (h6 : c 6 ≤ 3) (h7 : c 7 ≤ 5) :
    3 * c 4 + 2 * c 5 + 2 * c 6 + c 7 ≤ 18 := by omega

/-- This is only the arithmetic of the proposed dimension counts. -/
theorem route_dimension_counts :
    3 + 2 * 18 = (39 : ℕ) ∧ 2 * 39 + 1 = (79 : ℕ) ∧ 2 * 79 = (158 : ℕ) := by decide

/-- The purely numerical balanced-splitting recurrence; no reduction semantics are assumed. -/
def balancedCost (d : ℕ) : ℕ :=
  if h : d ≤ 3 then 0
  else 1 + balancedCost (d / 2 + 1) + balancedCost (d - d / 2 + 1) +
    balancedCost (d / 2) + balancedCost (d - d / 2)
termination_by d
decreasing_by all_goals omega

theorem balancedCost_values :
    balancedCost 4 = 1 ∧ balancedCost 5 = 2 ∧ balancedCost 6 = 3 ∧ balancedCost 7 = 5 := by
  norm_num [balancedCost]

theorem balancedCost_weighted :
    3 * balancedCost 4 + 2 * balancedCost 5 + 2 * balancedCost 6 + balancedCost 7 = 18 := by
  rcases balancedCost_values with ⟨h4, h5, h6, h7⟩
  omega

end GaussianMomentsCounterexamples
