import GaussianMomentsCounterexamples.Coordinates
import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

noncomputable section
set_option maxHeartbeats 2000000
open MvPolynomial
open scoped BigOperators
namespace GaussianMomentsCounterexamples

/-- The announced polynomial map in the manuscript's normalization. -/
def announcedMap : Fin 3 → MvPolynomial (Fin 3) ℂ :=
  ![(1 + 2 * X 0 * X 1)^3 * X 2 + 4 * X 1^2 * (1 + 2 * X 0 * X 1) * (2 + 3 * X 0 * X 1),
    X 1 + 3 * X 0 * (1 + 2 * X 0 * X 1)^2 * X 2 + 12 * X 0 * X 1^2 * (2 + 3 * X 0 * X 1),
    -X 0 + 3 * X 0^2 * X 1 + X 0^3 * X 2]

/-- The polynomial Jacobian matrix, with output indexing rows. -/
def polynomialJacobian (F : Fin 3 → MvPolynomial (Fin 3) ℂ) :
    Matrix (Fin 3) (Fin 3) (MvPolynomial (Fin 3) ℂ) := fun i j => pderiv j (F i)

set_option maxRecDepth 10000 in
set_option maxHeartbeats 2000000 in
theorem announcedMap_jacobian_det : (polynomialJacobian announcedMap).det = 1 := by
  have h2 (i : Fin 3) : pderiv i (2 : MvPolynomial (Fin 3) ℂ) = 0 := pderiv_C
  have h3 (i : Fin 3) : pderiv i (3 : MvPolynomial (Fin 3) ℂ) = 0 := pderiv_C
  have h4 (i : Fin 3) : pderiv i (4 : MvPolynomial (Fin 3) ℂ) = 0 := pderiv_C
  have h12 (i : Fin 3) : pderiv i (12 : MvPolynomial (Fin 3) ℂ) = 0 := pderiv_C
  rw [Matrix.det_fin_three]
  simp [polynomialJacobian, announcedMap, h2, h3, h4, h12]
  ring

/-- Evaluate all components of a polynomial map. -/
def evalPolynomialMap (F : Fin 3 → MvPolynomial (Fin 3) ℂ) (v : Fin 3 → ℂ) : Fin 3 → ℂ :=
  fun i => eval v (F i)

def collisionPoint₁ : Fin 3 → ℂ := ![1, -3/4, 13/4]
def collisionPoint₂ : Fin 3 → ℂ := ![-1, 3/4, 13/4]

theorem collisionPoints_distinct : collisionPoint₁ ≠ collisionPoint₂ := by
  intro h
  have hh := congrFun h 0
  norm_num [collisionPoint₁, collisionPoint₂] at hh

theorem announcedMap_collision₁ : evalPolynomialMap announcedMap collisionPoint₁ = ![-1/8, 0, 0] := by
  ext i
  fin_cases i <;> norm_num [evalPolynomialMap, announcedMap, collisionPoint₁]

theorem announcedMap_collision₂ : evalPolynomialMap announcedMap collisionPoint₂ = ![-1/8, 0, 0] := by
  ext i
  fin_cases i <;> norm_num [evalPolynomialMap, announcedMap, collisionPoint₂]

theorem announcedMap_not_injective : ¬ Function.Injective (evalPolynomialMap announcedMap) := by
  intro h
  exact collisionPoints_distinct (h (announcedMap_collision₁.trans announcedMap_collision₂.symm))

/-- In fact this polynomial map has no left inverse even as a set-theoretic function. -/
theorem announcedMap_no_leftInverse :
    ¬ ∃ H : (Fin 3 → ℂ) → (Fin 3 → ℂ), Function.LeftInverse H (evalPolynomialMap announcedMap) := by
  rintro ⟨H, hH⟩
  exact announcedMap_not_injective hH.injective

/-- Target-normalized map, in sparse monomial form. -/
def normalizedAnnouncedMap : Fin 3 → MvPolynomial (Fin 3) ℂ :=
  ![monomial (exp3 1 0 0) 1 + monomial (exp3 2 1 0) (-3) + monomial (exp3 3 0 1) (-1),
    monomial (exp3 0 1 0) 1 + monomial (exp3 1 0 1) 3 + monomial (exp3 1 2 0) 24 +
      monomial (exp3 2 1 1) 12 + monomial (exp3 2 3 0) 36 + monomial (exp3 3 2 1) 12,
    monomial (exp3 0 0 1) 1 + monomial (exp3 0 2 0) 8 + monomial (exp3 1 1 1) 6 +
      monomial (exp3 1 3 0) 28 + monomial (exp3 2 2 1) 12 +
      monomial (exp3 2 4 0) 24 + monomial (exp3 3 3 1) 8]

lemma monomial_exp3_eq (a b c : ℕ) (r : ℂ) :
    monomial (exp3 a b c) r = C r * X 0 ^ a * X 1 ^ b * X 2 ^ c := by
  simp [exp3, X_pow_eq_monomial, C_mul_monomial, monomial_mul_monomial]

/-- The displayed normalized map is exactly the target composition (-F₃,F₂,F₁). -/
theorem normalizedAnnouncedMap_eq_target :
    normalizedAnnouncedMap = ![-announcedMap 2, announcedMap 1, announcedMap 0] := by
  funext i
  fin_cases i <;> norm_num [normalizedAnnouncedMap, announcedMap, monomial_exp3_eq, map_ofNat] <;> ring

/-- Every linear coefficient is the corresponding identity matrix entry. -/
theorem normalizedAnnouncedMap_linear_coeff (i j : Fin 3) :
    (normalizedAnnouncedMap i).coeff (Finsupp.single j 1) = if i = j then 1 else 0 := by
  fin_cases i <;> fin_cases j <;>
    norm_num [normalizedAnnouncedMap, exp3, coeff_monomial, Finsupp.ext_iff, Fin.forall_fin_succ]

/-- The normalized map also has zero constant term. -/
theorem normalizedAnnouncedMap_constant (i : Fin 3) :
    (normalizedAnnouncedMap i).coeff 0 = 0 := by
  fin_cases i <;>
    norm_num [normalizedAnnouncedMap, exp3, coeff_monomial, Finsupp.ext_iff, Fin.forall_fin_succ]


theorem normalizedAnnouncedMap_support_0 :
    (normalizedAnnouncedMap 0).support = {exp3 1 0 0, exp3 2 1 0, exp3 3 0 1} := by
  classical
  ext d
  by_cases h0 : d = exp3 1 0 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h1 : d = exp3 2 1 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h2 : d = exp3 3 0 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  simp [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, h0, h1, h2, Ne.symm h0, Ne.symm h1, Ne.symm h2]

theorem normalizedAnnouncedMap_support_1 :
    (normalizedAnnouncedMap 1).support = {exp3 0 1 0, exp3 1 0 1, exp3 1 2 0, exp3 2 1 1, exp3 2 3 0, exp3 3 2 1} := by
  classical
  ext d
  by_cases h0 : d = exp3 0 1 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h1 : d = exp3 1 0 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h2 : d = exp3 1 2 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h3 : d = exp3 2 1 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h4 : d = exp3 2 3 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h5 : d = exp3 3 2 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  simp [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, h0, h1, h2, h3, h4, h5, Ne.symm h0, Ne.symm h1, Ne.symm h2, Ne.symm h3, Ne.symm h4, Ne.symm h5]

theorem normalizedAnnouncedMap_support_2 :
    (normalizedAnnouncedMap 2).support = {exp3 0 0 1, exp3 0 2 0, exp3 1 1 1, exp3 1 3 0, exp3 2 2 1, exp3 2 4 0, exp3 3 3 1} := by
  classical
  ext d
  by_cases h0 : d = exp3 0 0 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h1 : d = exp3 0 2 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h2 : d = exp3 1 1 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h3 : d = exp3 1 3 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h4 : d = exp3 2 2 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h5 : d = exp3 2 4 0
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  by_cases h6 : d = exp3 3 3 1
  · subst d
    norm_num [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, exp3,
      Finsupp.ext_iff, Fin.forall_fin_succ]
  simp [mem_support_iff, normalizedAnnouncedMap, coeff_monomial, h0, h1, h2, h3, h4, h5, h6, Ne.symm h0, Ne.symm h1, Ne.symm h2, Ne.symm h3, Ne.symm h4, Ne.symm h5, Ne.symm h6]

/-- Number of nonzero component monomials of a given total degree. -/
def normalizedAnnouncedDegreeCount (d : ℕ) : ℕ :=
  ∑ i : Fin 3, ((normalizedAnnouncedMap i).support.filter
    (fun e => e.sum (fun _ k => k) = d)).card

theorem normalizedAnnouncedDegreeCounts :
    normalizedAnnouncedDegreeCount 4 = 3 ∧ normalizedAnnouncedDegreeCount 5 = 2 ∧
    normalizedAnnouncedDegreeCount 6 = 2 ∧ normalizedAnnouncedDegreeCount 7 = 1 := by
  norm_num [normalizedAnnouncedDegreeCount, Fin.sum_univ_succ,
    normalizedAnnouncedMap_support_0, normalizedAnnouncedMap_support_1,
    normalizedAnnouncedMap_support_2, exp3, Finsupp.sum_add_index, Finsupp.sum_single_index,
    Finsupp.ext_iff, Fin.forall_fin_succ, Finset.filter_insert, Finset.filter_singleton]

/-- The target change (u,v,w) ↦ (-w,v,u) is a complex linear automorphism. -/
def targetNormalization : (Fin 3 → ℂ) ≃ₗ[ℂ] (Fin 3 → ℂ) where
  toFun v := ![-v 2, v 1, v 0]
  invFun v := ![v 2, v 1, -v 0]
  left_inv v := by ext i; fin_cases i <;> simp
  right_inv v := by ext i; fin_cases i <;> simp
  map_add' v w := by ext i; fin_cases i <;> simp [add_comm]
  map_smul' c v := by ext i; fin_cases i <;> simp

theorem normalizedAnnouncedMap_eval (v : Fin 3 → ℂ) :
    evalPolynomialMap normalizedAnnouncedMap v = targetNormalization (evalPolynomialMap announcedMap v) := by
  rw [normalizedAnnouncedMap_eq_target]
  funext i
  fin_cases i
  · change eval v (-announcedMap 2) = -eval v (announcedMap 2)
    exact map_neg _ _
  · rfl
  · rfl

end GaussianMomentsCounterexamples
