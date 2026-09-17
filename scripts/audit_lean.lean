import GaussianMomentsCounterexamples
import Lean.Util.CollectAxioms

/-! Audit declaration origins, rather than public names, so private, generated,
and differently namespaced constants cannot escape the transitive check. -/
open Lean in
run_cmd do
  let env ← getEnv
  let allowed := #[``propext, ``Classical.choice, ``Quot.sound]
  let mut declarations : Nat := 0
  let mut theorems : Nat := 0
  let mut modules : Nat := 0
  for moduleName in env.header.moduleNames do
    if (`GaussianMomentsCounterexamples).isPrefixOf moduleName then
      modules := modules + 1
  unless modules > 1 do
    throwError "No mathematical project modules imported"
  for (name, info) in env.constants.toList do
    let owned := match env.getModuleIdxFor? name with
      | some idx => (`GaussianMomentsCounterexamples).isPrefixOf env.header.moduleNames[idx.toNat]!
      | none => false
    if owned then
      declarations := declarations + 1
      if info.isTheorem then theorems := theorems + 1
      match info with
      | .axiomInfo _ => throwError "Project-added foundational declaration: {name}"
      | _ => pure ()
      for ax in ← collectAxioms name do
        unless allowed.contains ax do
          throwError "Unapproved dependency {ax} in {name}"
  unless declarations > 0 ∧ theorems > 0 do
    throwError "Empty declaration audit"
  logInfo m!"Axiom audit passed: {modules} modules, {declarations} declarations, {theorems} theorem constants."
  logInfo "All transitive dependencies lie in {propext, Classical.choice, Quot.sound}."
