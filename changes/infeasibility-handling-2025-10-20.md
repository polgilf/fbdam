# Implementation Instructions for LLM Agent: FBDAM Infeasibility Handling

## Mission Overview

You are tasked with modifying an optimization pipeline (FBDAM - Food Basket Design and Allocation Model) to gracefully handle infeasible solutions. Currently, the system crashes or behaves unpredictably when the solver cannot find a feasible solution. Your goal is to ensure the system captures all diagnostic information, provides clear user feedback, and continues execution even when models are infeasible.

## Project Context

**Technology Stack:**

* Python 3.12+
* Pyomo (optimization modeling)
* HiGHS solver (via APPSI interface or classic wrapper)
* Typer (CLI framework)
* Rich (terminal formatting)

**Current Architecture:**

```
User → CLI (run.py) → IO (io.py) → Model Builder (model.py) → Solver (solver.py) → Reporting (reporting.py) → Artifacts
```

**Key Files to Modify:**

1. `src/fbdam/engine/solver.py` (primary changes)
2. `src/fbdam/engine/run.py` (CLI feedback)
3. `src/fbdam/engine/reporting.py` (report generation)
4. `src/fbdam/engine/kpis.py` (KPI computation)

---

## PART 1: Solver Module Changes (`solver.py`)

### Objective

Enhance the solver interface to detect and report infeasibility without raising exceptions.

### Current Behavior

The `solve_model()` function:

* Accepts a Pyomo model and solver options
* Invokes the solver (APPSI HiGHS or classic HiGHS)
* Extracts results (termination condition, status, objective value, variable values)
* Returns a dictionary with solver metadata

**Problem:** When the solver returns "infeasible", the system either crashes or produces incomplete/invalid results.

### Required Changes

#### Change 1.1: Add Feasibility Detection

Add a new boolean field `is_feasible` to the results dictionary returned by `solve_model()`.

**Logic:**

* Examine the termination condition string (case-insensitive)
* If it contains "infeasible" → set `is_feasible = False`
* If it contains "unbounded" → set `is_feasible = False`
* If it contains "optimal" → set `is_feasible = True`
* If it contains "feasible" (but not "infeasible") → set `is_feasible = True`
* Otherwise (unknown/error) → set `is_feasible = False` (safe default)

**Implementation Notes:**

* Handle both APPSI interface (where results have direct attributes like `results.termination_condition`)
* Handle classic interface (where results have nested attributes like `results.solver.termination_condition`)
* The termination condition is an enum or object that needs `.to_string()` or `str()` conversion

#### Change 1.2: Create Status Normalization Helper

Create a new helper function `_determine_status()` that maps verbose termination conditions to simple status strings.

**Mapping:**

* "optimal" → "ok"
* "infeasible" → "infeasible"
* "unbounded" → "unbounded"
* "limit" or "timeout" → "time_limit"
* anything else → return the raw string

**Purpose:** Provide a consistent, simple status field for users and downstream code.

#### Change 1.3: Create Feasibility Check Helper

Create a new helper function `_check_feasibility()` that takes termination and status strings and returns a boolean.

**Logic:**

* Return False if either string contains "infeasible" or "unbounded"
* Return True if either string contains "optimal" or status is "ok"
* Return True if termination contains "feasible" (partial success)
* Return False by default (conservative approach)

#### Change 1.4: Add Exception Handling

Wrap the solver invocation in a try-except block.

**If an exception occurs:**

* Capture the exception message
* Create an error report dictionary with:
  * `solver`: the solver name
  * `elapsed_sec`: time elapsed before error
  * `termination`: "error"
  * `status`: "error"
  * `is_feasible`: False
  * `error_message`: the exception message as a string
  * `objective_value`: None
  * `variables`: empty dict
  * `gap`: None
  * `best_bound`: None
* Return this error report instead of raising the exception

**Create a helper function `_build_error_report()` for this purpose.**

#### Change 1.5: Update Result Dictionary Structure

Modify the results dictionary structure to always include:

```
{
    "solver": str,              # "appsi_highs" or "highs"
    "elapsed_sec": float,       # rounded to 4 decimals
    "termination": str,         # raw termination condition
    "status": str,              # normalized status (ok/infeasible/etc)
    "is_feasible": bool,        # NEW: feasibility flag
    "objective_value": float | None,
    "best_feasible_objective": float | None,  # if available
    "best_objective_bound": float | None,     # if available
    "gap": float | None,
    "variables": dict,          # var_name -> value mapping
    "error_message": str | None  # NEW: only present if exception
}
```

#### Change 1.6: Safe Variable Extraction

Ensure the `_extract_variable_values()` helper function uses `pyo.value(var, exception=False)` to prevent crashes when variables are uninitialized (common in infeasible solutions).

**Behavior:**

* If a variable has no value, store `None` instead of raising an exception
* This allows inspection of partial solutions or solver state even when fully infeasible

---

## PART 2: CLI Module Changes (`run.py`)

### Objective

Provide clear, differentiated feedback to users based on whether the solution is feasible or infeasible.

### Current Behavior

The CLI command `fbdam run` currently:

* Loads scenario configuration
* Builds the Pyomo model
* Solves the model
* Generates reports and artifacts
* Displays a success message with artifact locations

**Problem:** The success message appears even when the model is infeasible, which is misleading.

### Required Changes

#### Change 2.1: Extract Feasibility Status

After calling `solve_model()`, extract the `is_feasible` field from the results dictionary:

```
is_feasible = results.get("is_feasible", True)
```

**Note:** Default to `True` for backward compatibility with older solver results that don't have this field.

#### Change 2.2: Conditional Success/Warning Display

Replace the single "Pipeline finished successfully" panel with conditional logic:

**If `is_feasible` is True:**

* Display a GREEN-bordered panel (using Rich's `border_style="green"`)
* Title: "Pipeline finished successfully"
* Content:
  * Run ID (bold)
  * Artifacts directory path
  * Number of manifest entries
  * Manifest file path

**If `is_feasible` is False:**

* Display a YELLOW-bordered panel (using Rich's `border_style="yellow"`)
* Title: "Model is INFEASIBLE" (bold yellow)
* Content:
  * Termination condition from results
  * Status from results
  * Empty line for spacing
  * Section header: "Diagnostic artifacts saved:" (dimmed)
  * Run ID (bold)
  * Artifacts directory path
  * Solver log path (from solver options or "N/A")
  * Model MPS path (if export_mps is True, else "N/A")
  * Manifest file path

#### Change 2.3: Maintain Non-Breaking Behavior

Ensure the CLI does NOT raise an exit code or exception for infeasible solutions. The pipeline should complete normally and return exit code 0.

**Rationale:** Users need artifacts for diagnosis. A crash would prevent artifact generation.

---

## PART 3: Reporting Module Changes (`reporting.py`)

### Objective

Enhance reports to clearly communicate infeasibility and provide actionable troubleshooting guidance.

### Current Behavior

The `write_markdown_summary()` function:

* Creates a human-readable Markdown report
* Includes solver summary section
* Includes KPIs section (if provided)
* Includes model statistics section

**Problem:** The report treats infeasible solutions identically to feasible ones, providing no diagnostic guidance.

### Required Changes

#### Change 3.1: Detect Infeasibility in Report Generation

At the start of `write_markdown_summary()`, check the feasibility status:

```
solver_section = solver_report.get("solver", {})
is_feasible = solver_section.get("is_feasible", True)
```

#### Change 3.2: Add Infeasibility Warning Section

If `is_feasible` is False, immediately after the Run ID section, insert:

```markdown
⚠️ **WARNING: MODEL IS INFEASIBLE** ⚠️

The solver could not find a feasible solution. Review the constraints and dials.
```

**Formatting requirements:**

* Use emoji warning symbol (⚠️)
* Bold text using Markdown double asterisks
* Blank line before and after for visibility

#### Change 3.3: Modify Solver Summary Section

Add the error message field to the solver summary if present:

**Current keys displayed:**

* name, status, termination, elapsed_sec, objective_value, gap, best_bound

**Add after the existing keys:**

* If `error_message` exists in solver_section, display it as:
  ```markdown
  **Error:** {error_message}
  ```

#### Change 3.4: Conditional KPI Section

Modify the KPI section generation:

**If `is_feasible` is True:**

* Display KPIs normally in a table format

**If `is_feasible` is False:**

* Display the "## KPIs" header
* Display: " *KPIs not available for infeasible solutions.* " (italicized)
* Do NOT attempt to display the KPI table (it will contain None values)

#### Change 3.5: Add Troubleshooting Section

If `is_feasible` is False, append a new section at the end of the report:

```markdown
## Troubleshooting suggestions
- Check the solver log for detailed infeasibility analysis
- Review constraint dial values (alpha, beta, gamma, kappa, rho, omega)
- Verify that requirements are achievable with available stock + budget
- Consider relaxing adequacy floors or equity caps
- Enable epsilon slack with a small lambda penalty
```

**Format as a bullet list with actionable items.**

#### Change 3.6: Maintain All Artifact Generation

Ensure that ALL artifacts (variables.csv, model.mps, config_snapshot.json, etc.) are still generated even when infeasible.

**Critical:** Do NOT skip artifact generation based on feasibility status. Users need these files for diagnosis.

---

## PART 4: KPI Module Changes (`kpis.py`)

### Objective

Prevent crashes when computing KPIs for infeasible solutions where model expressions may not evaluate.

### Current Behavior

The `compute_kpis()` function:

* Takes a Pyomo model, domain index, and solver report
* Computes various metrics by evaluating Pyomo expressions
* Returns a nested dictionary with categorized KPIs

**Problem:** When a model is infeasible, variables and expressions may be uninitialized, causing `pyo.value()` calls to fail.

### Required Changes

#### Change 4.1: Early Feasibility Check

At the very start of `compute_kpis()`, extract and check the feasibility status:

```
solver_section = solver_report.get("solver")
is_feasible = True
if isinstance(solver_section, Mapping):
    is_feasible = solver_section.get("is_feasible", True)
```

#### Change 4.2: Return Placeholder KPIs for Infeasible Models

If `is_feasible` is False, immediately return a minimal KPI structure:

```python
{
    "kpi": {
        "basic": {
            "items": len(domain.items) if domain else None,
            "households": len(domain.households) if domain else None,
            "nutrients": len(domain.nutrients) if domain else None,
            "objective_value": None,
            "feasibility_status": "INFEASIBLE"
        }
    }
}
```

**Key points:**

* Still include item/household/nutrient counts (safe to extract)
* Set `objective_value` to `None`
* Add a new field `feasibility_status: "INFEASIBLE"` for clarity
* Do NOT attempt to compute utility, supply, or allocation equity metrics

#### Change 4.3: Ensure Safe Evaluation for Feasible Cases

For the normal (feasible) path, ensure all `pyo.value()` calls include `exception=False`:

```python
pyo.value(model.some_expression, exception=False)
```

**Rationale:** Even "feasible" solutions may have partially undefined values (e.g., time limits, suboptimal solutions).

#### Change 4.4: Handle None Values in KPI Calculations

When computing aggregate statistics (min, max, mean), filter out `None` values before applying the operation:

**Example:**

```
# Instead of:
min(pyo.value(model.u[n, h]) for n in model.N for h in model.H)

# Use:
values = [pyo.value(model.u[n, h], exception=False) for n in model.N for h in model.H]
valid_values = [v for v in values if v is not None]
min(valid_values) if valid_values else None
```

---

## PART 5: Integration and Testing Instructions

### Testing Requirements

#### Test 5.1: Create Infeasible Scenario

Create a new test scenario YAML file with impossible constraints:

**Scenario characteristics:**

* Set `alpha` and `beta` to 0.0 (perfect allocation equity impossible with unequal households)
* Set `rho` and `kappa` to 1.0 (all households must equal global mean - contradictory)
* Set budget very low (insufficient to buy necessary items)

**Expected behavior:**

* Solver should return termination = "infeasible"
* `is_feasible` should be False
* All artifacts should still be generated
* CLI should display yellow warning panel
* Report.md should contain infeasibility warning

#### Test 5.2: Verify Artifact Generation

For the infeasible test scenario, verify these files are created:

* `solver.log` (should contain "infeasible" or similar)
* `model.mps` (should be a valid MPS file)
* `solver_report.json` (should have `"is_feasible": false`)
* `report.md` (should contain warning section and troubleshooting)
* `kpis.json` (should have placeholder KPIs with INFEASIBLE status)
* `manifest.json` (should list all artifacts with checksums)

#### Test 5.3: Verify Backward Compatibility

Run existing test scenarios (demo.yaml, demo_efficiency.yaml, demo_fairness.yaml):

* All should complete successfully
* Results should be identical to pre-modification behavior
* New `is_feasible` field should be present and True
* Reports should NOT show infeasibility warnings

#### Test 5.4: Test Exception Handling

Intentionally break the solver (e.g., provide invalid solver name or malformed model):

* System should catch the exception
* Should return an error report dictionary with `error_message`
* Should NOT crash or raise unhandled exception
* Should still generate artifacts with error information

### Integration Checklist

* [ ] All four modules modified (solver.py, run.py, reporting.py, kpis.py)
* [ ] New helper functions created and used
* [ ] `is_feasible` field added to solver results
* [ ] CLI displays conditional panels based on feasibility
* [ ] Markdown reports include infeasibility warnings when appropriate
* [ ] KPI computation handles infeasible cases without crashing
* [ ] All artifacts generated regardless of feasibility
* [ ] Exception handling prevents crashes
* [ ] Backward compatibility maintained
* [ ] No new dependencies required
* [ ] Existing tests pass
* [ ] New infeasibility test passes

---

## PART 6: Implementation Order and Dependencies

### Recommended Implementation Sequence

**Step 1: Solver Module (CRITICAL PATH)**
Start here because all other changes depend on the `is_feasible` flag.

* Implement feasibility detection helpers
* Add exception handling
* Update results dictionary structure
* Test with both feasible and infeasible scenarios

**Step 2: KPI Module (SAFETY)**
Implement this before reporting to prevent crashes during report generation.

* Add early feasibility check
* Return placeholder KPIs for infeasible cases
* Test that KPI computation doesn't crash

**Step 3: Reporting Module (USER COMMUNICATION)**
Now enhance reports with infeasibility information.

* Add infeasibility warning section
* Conditional KPI display
* Troubleshooting section
* Test report generation with infeasible solver results

**Step 4: CLI Module (POLISH)**
Finally, update user-facing feedback.

* Conditional panel display
* Test CLI output with both feasible and infeasible runs
* Verify artifact paths are correct

### Dependency Graph

```
solver.py (is_feasible flag)
    ↓
    ├─→ kpis.py (check is_feasible before computing)
    │       ↓
    └─→ reporting.py (check is_feasible for report content)
            ↓
        run.py (check is_feasible for display)
```

---

## PART 7: Edge Cases and Special Considerations

### Edge Case 7.1: Time-Limited Solutions

**Scenario:** Solver hits time limit with a partial feasible solution.

**Expected Behavior:**

* `is_feasible` should be True (solution exists, even if suboptimal)
* `termination` might be "time_limit" or "limit"
* `status` should be "time_limit"
* KPIs should compute normally
* Report should NOT show infeasibility warning
* Consider adding a note about time limit in report

### Edge Case 7.2: Unbounded Solutions

**Scenario:** Solver reports "unbounded".

**Expected Behavior:**

* `is_feasible` should be False (no finite optimal solution)
* Treat similar to infeasible
* Report should show warning
* Troubleshooting should suggest adding upper bounds

### Edge Case 7.3: Mock Solver (No Real Solver Available)

**Scenario:** Neither APPSI nor classic HiGHS is available.

**Expected Behavior:**

* Existing mock solve behavior should continue
* Mock solve sets all variables to 0.0
* `is_feasible` should default to True (or False - clarify based on context)
* Should not crash

### Edge Case 7.4: Solver Crashes Mid-Execution

**Scenario:** Solver process crashes (segfault, memory error).

**Expected Behavior:**

* Exception handling should catch this
* Error report should be generated
* `error_message` should contain exception details
* All other artifacts should still generate
* Model MPS should still export (happens before solve)

### Edge Case 7.5: Missing Solver Log File

**Scenario:** Solver log path specified but file not created.

**Expected Behavior:**

* CLI should show "N/A" or "[not created]" instead of crashing
* Manifest should not include non-existent log file
* Should not prevent other artifact generation

---

## PART 8: Validation and Quality Assurance

### Code Quality Requirements

#### Requirement 8.1: Type Hints

All new helper functions should have proper type hints:

* Parameter types
* Return types
* Use `Optional[T]` for nullable returns
* Import from `typing` module

#### Requirement 8.2: Docstrings

All new functions should have docstrings with:

* One-line summary
* Args section describing parameters
* Returns section describing return value
* Notes section for special behavior or edge cases

#### Requirement 8.3: Error Messages

User-facing error messages should be:

* Clear and non-technical
* Actionable (suggest what to do next)
* Consistent in terminology
* Free of internal implementation details

#### Requirement 8.4: Logging

Consider adding logging statements (using Python's logging module) at key decision points:

* When infeasibility is detected
* When exceptions are caught
* When artifacts are being generated despite infeasibility

**Log levels:**

* INFO: Normal feasibility detection
* WARNING: Infeasibility detected
* ERROR: Exception caught
* DEBUG: Detailed solver status parsing

### Performance Requirements

#### Requirement 8.5: No Additional Solver Calls

Do NOT add any additional solver invocations. All detection should be based on existing solver results.

#### Requirement 8.6: Minimal Overhead

Feasibility checking should add negligible time:

* Simple string comparisons
* Dictionary lookups
* No heavy computation
* Target: <1ms overhead

#### Requirement 8.7: Memory Efficiency

Do NOT create deep copies of large data structures unnecessarily:

* Reuse existing results dictionary
* Add fields in-place
* Only create new dictionaries for error reports

---

## PART 9: Documentation Requirements

### Code-Level Documentation

#### Doc 9.1: Inline Comments

Add comments explaining:

* Why infeasibility detection logic uses specific keywords
* Why certain fields default to None vs False
* Why exceptions are caught but not re-raised
* Any non-obvious design decisions

#### Doc 9.2: Module Docstrings

Update module-level docstrings for modified files:

* Mention new infeasibility handling capability
* List new functions added
* Note backward compatibility

### User Documentation Updates (if applicable)

#### Doc 9.3: README.md

If the repository has a README, add a section:

* "Handling Infeasible Solutions"
* Brief explanation of what happens
* Link to solver.log and model.mps for diagnosis

#### Doc 9.4: Example Scenarios

Consider adding commented YAML examples showing:

* Common infeasibility causes
* How to relax constraints
* How to enable slack variables

---

## PART 10: Final Implementation Checklist

### Pre-Implementation

* [ ] Understand current solver.py structure
* [ ] Identify how APPSI vs classic interface differs
* [ ] Locate where results dictionary is constructed
* [ ] Review existing exception handling patterns

### Core Implementation

* [ ] Add feasibility detection to solver.py
* [ ] Create helper functions (_check_feasibility, _determine_status, _build_error_report)
* [ ] Add exception handling around solver invocation
* [ ] Update results dictionary structure with is_feasible
* [ ] Modify kpis.py to check feasibility early
* [ ] Add placeholder KPI return for infeasible cases
* [ ] Update reporting.py to detect infeasibility
* [ ] Add infeasibility warning to Markdown reports
* [ ] Add troubleshooting section to reports
* [ ] Modify run.py to check is_feasible
* [ ] Implement conditional panel display (green vs yellow)

### Testing

* [ ] Create infeasible test scenario
* [ ] Verify solver returns is_feasible=False
* [ ] Verify all artifacts still generated
* [ ] Verify CLI shows yellow warning panel
* [ ] Verify report.md contains warning and troubleshooting
* [ ] Verify kpis.json has placeholder values
* [ ] Test backward compatibility with existing scenarios
* [ ] Test exception handling with broken solver
* [ ] Verify no crashes occur anywhere

### Quality Assurance

* [ ] Add type hints to all new functions
* [ ] Write docstrings for all new functions
* [ ] Add inline comments for complex logic
* [ ] Check for consistent error messages
* [ ] Verify performance overhead is minimal
* [ ] Check memory usage patterns

### Documentation

* [ ] Update solver.py module docstring
* [ ] Update run.py module docstring
* [ ] Update reporting.py module docstring
* [ ] Update kpis.py module docstring
* [ ] Add inline comments explaining key decisions
* [ ] Consider updating README if applicable

### Deployment

* [ ] Run full test suite
* [ ] Verify backward compatibility
* [ ] Check that no new dependencies were added
* [ ] Verify changes work with both APPSI and classic HiGHS
* [ ] Test on different platforms if applicable (Windows/Linux/Mac)
* [ ] Review all changes for production readiness

---

## Success Criteria

The implementation is successful when:

1. **Infeasible models complete without crashing**
2. **All diagnostic artifacts are saved** (logs, MPS, reports)
3. **Users receive clear feedback** distinguishing feasible from infeasible
4. **Existing functionality is preserved** (backward compatible)
5. **No new dependencies are required**
6. **Performance overhead is negligible** (<1ms)
7. **All tests pass** (existing + new infeasibility test)
8. **Code quality standards are met** (types, docs, comments)

The system should feel polished and production-ready, with infeasibility being treated as a normal, expected outcome rather than an error condition.
