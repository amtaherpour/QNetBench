# QNetBench Codex Execution Control Plan v0.1

_Machine-readable Markdown/text extraction from `QNetBench_Codex_Execution_Control_Plan_v0_1(1).pdf`._

_Use this file for Codex if PDF reading is unavailable. The original PDF remains the human visual source._



---

## Page 1


QNetBench Codex Execution Control Plan  |  v0.1
Page 1
QNetBench
Codex Execution Control Plan
Finite checkpoint instructions for Checkpoints 0 through 11
Version 0.1
Prepared July 10, 2026
Target: QNetBench 0.1.0a1 after Checkpoint 11
Use with the QNetBench Improved AI Handoff Manual v0.2. Codex executes one checkpoint, reports, and stops.
This document is planning and control guidance. It contains no implementation code.



---

## Page 2


QNetBench Codex Execution Control Plan  |  v0.1
Page 2
Contents
This contents list is intentionally page-number free so it remains stable across renderers.
1. How to use this plan
2. Global execution controls
3. Checkpoint map
4. Detailed checkpoint instructions 0-11
5. Proposed checkpoint report template
6. Proposed blocker report template
7. Proposed AGENTS.md
8. Proposed PROJECT_STATE.md template
9. Assumptions that must not be silently changed
10. Exact first Codex prompt for Checkpoint 0



---

## Page 3


QNetBench Codex Execution Control Plan  |  v0.1
Page 3
1. How to use this plan
This is a control document, not a backlog. Only one checkpoint is active at a time. Codex receives a checkpoint 
prompt, inspects the current repository, implements only the listed scope, runs every required command, updates the 
handoff state, reports, and stops.
1.  Read AGENTS.md, PROJECT_STATE.md, the improved manual, the active checkpoint section, latest report, 
relevant contracts, ADRs, and blockers.
2.  Inspect git status before editing and preserve unrelated human changes.
3.  Confirm that all prerequisites from the prior checkpoint are actually present and passing.
4.  Implement the smallest change set that meets the active definition of done.
5.  Add required tests and run every command exactly. Do not summarize a command that was not run.
6.  Update PROJECT_STATE.md, write the checkpoint or blocker report, commit if authorized, and stop.
No chained checkpoints
A successful checkpoint does not authorize the next one. The next checkpoint begins only after a new human or 
controller prompt.
2. Global execution controls
2.1 Toolchain decisions for the alpha
- Python baseline: 3.12.
- Packaging: PEP 621 pyproject.toml with setuptools build backend and pip-based developer commands.
- Runtime libraries: Pydantic v2, PyYAML, and Typer. Matplotlib is introduced only for the plot extra at Checkpoint 
8. The SeQUeNCe dependency is introduced only after the verified research checkpoint.
- Quality tools: pytest and Ruff. Mypy, pre-commit, tox/nox, and coverage thresholds are not required for 0.1.0a1.
- License: BSD-3-Clause unless the human owner changes it before Checkpoint 0 is approved.
- Version progression: 0.0.0.dev0 through Checkpoint 10; 0.1.0a1 at Checkpoint 11.
2.2 Common commands
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
2.3 Common stop conditions
- A required command fails and cannot be corrected within checkpoint scope.
- The repository state conflicts with the current checkpoint assumptions.
- Completing the task requires a frozen-contract change, new dependency, or future-checkpoint feature.
- An external simulator API, installation step, license, or version cannot be verified.
- Unrelated human changes would be overwritten or require a merge decision.
- Tests pass only after weakening or deleting an existing requirement.
2.4 Commit policy
Each completed checkpoint should be one focused commit when repository permissions and author identity are 
already configured. Codex must not force-push, rewrite history, or publish. If committing is unavailable, the report 
must say so and provide the exact dirty working tree state.
3. Checkpoint map
CP
Name
Release gate
0
Repository control plane and minimal 
package skeleton
Control plane



---

## Page 4


QNetBench Codex Execution Control Plan  |  v0.1
Page 4
CP
Name
Release gate
1
Freeze the v0.1 contracts
Contracts frozen
2
Benchmark loading, normalization, and 
hashing
Spec runtime
3
Canonical result models and artifact bundle 
I/O
Canonical bundle
4
Adapter interface, registry, and 
deterministic mock adapter
Mock adapter
5
Backend-independent metric engine
Metrics
6
Single-run orchestration and CLI through 
the mock backend
Mock single-run E2E
7
Frozen benchmark catalog and user-facing 
mock documentation
Four benchmarks
8
Finite sweep, aggregate analysis, plots, and 
mock-pipeline release gate
Mock pipeline ready
9
Verified SeQUeNCe research spike - no 
production adapter
SeQUeNCe verified
10
Narrow SeQUeNCe adapter MVP and 
integration validation
SeQUeNCe MVP
11
Alpha hardening, release validation, and 
0.1.0a1 candidate
0.1.0a1 candidate
SeQUeNCe gate
Checkpoint 9 may begin only after Checkpoint 8 records mock_pipeline_ready: true. Production sequence.py is 
forbidden until Checkpoint 10.
4. Detailed checkpoint instructions 0-11
Every checkpoint below contains the seven controls requested for Codex: goal, files, tests, commands, definition of 
done, what must not be done yet, and the expected stop/report format.



---

## Page 5


QNetBench Codex Execution Control Plan  |  v0.1
Page 5
Checkpoint 0: Repository control plane and minimal package 
skeleton
Goal
Create a clean, installable repository with governance files, one importable package, default CI, and no product behavior. 
Establish the checkpoint control system before contracts or adapters are implemented.
Files to create or edit
- AGENTS.md
- PROJECT_STATE.md
- pyproject.toml
- README.md
- LICENSE
- CHANGELOG.md
- .gitignore
- Makefile
- .github/workflows/ci.yml
- qnetbench/__init__.py
- tests/test_import.py
- docs/ai_handoff/checkpoint_00_report.md
Tests required
- Package imports as qnetbench in an editable install.
- qnetbench.__version__ exists and equals 0.0.0.dev0.
- No CLI, schema, adapter, metric, or runner behavior is tested or implemented.
Commands required
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
Definition of done
- All required files exist and use the approved project assumptions.
- The default CI workflow runs the same lint and test commands on Python 3.12.
- README clearly says the project is pre-contract and at Checkpoint 0.
- PROJECT_STATE.md identifies Checkpoint 1 as the only next allowed work.
- The checkpoint report records the exact repository state and command outputs.
What Codex must not do yet
Stop boundary
- Do not create the benchmark/result schemas.
- Do not add a console entry point or implement CLI commands.
- Do not add adapters, simulator dependencies, metrics, runners, benchmark files, or plots.
- Do not choose a SeQUeNCe version or create sequence.py.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- State whether the repository was new or pre-existing and list preserved pre-existing files.
- Report the selected build backend and dependency declarations.
- Report CI file contents at a high level and the final clean/dirty git status.



---

## Page 6


QNetBench Codex Execution Control Plan  |  v0.1
Page 6
Required final status line
STATUS: COMPLETE - Checkpoint 0 only. STOP. Next allowed checkpoint: 1.
Checkpoint 1: Freeze the v0.1 contracts
Goal
Define and test the normative BenchmarkSpec, Canonical Result Contract, metric row shape, examples, and architectural 
boundary before runtime implementation.
Files to create or edit
- docs/contracts/README.md
- docs/contracts/benchmark_spec_v0_1.md
- docs/contracts/canonical_result_v0_1.md
- docs/contracts/metric_definitions_v0_1.md
- pyproject.toml (add PyYAML and jsonschema for contract tests)
- schemas/v0_1/benchmark.schema.json
- schemas/v0_1/run_manifest.schema.json
- schemas/v0_1/request_result.schema.json
- schemas/v0_1/metric_row.schema.json
- schemas/v0_1/summary.schema.json
- schemas/v0_1/error.schema.json
- examples/contracts/minimal_benchmark.yaml
- examples/contracts/complete_run/benchmark.yaml
- examples/contracts/complete_run/run_manifest.json
- examples/contracts/complete_run/requests.jsonl
- examples/contracts/complete_run/metrics.csv
- examples/contracts/complete_run/summary.json
- examples/contracts/failed_run/run_manifest.json
- examples/contracts/failed_run/error.json
- docs/decisions/ADR-0001-contract-boundaries.md
- tests/contracts/test_contract_examples.py
- docs/ai_handoff/checkpoint_01_report.md
Tests required
- Every checked-in JSON Schema is itself valid.
- The minimal benchmark validates and rejects backend, seed, output, and sweep fields.
- The complete-run example validates against manifest, request, and metric-row schemas.
- Negative fixtures cover unknown fields, duplicate IDs, invalid units/ranges, NaN/infinity, and bad status values.
- Docs and schemas agree on required fields and enums.
Commands required
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/contracts
python -m pytest -q
git diff --check
Definition of done
- The contracts make BenchmarkSpec backend-independent and SweepSpec/RunRequest separate concerns.
- The result bundle requires one terminal request record per planned request.
- Metric availability states and stable CSV columns are fixed.
- All examples validate and all negative fixtures fail for the intended reason.
- ADR-0001 states that breaking changes require approval and versioning.
- PROJECT_STATE.md marks contract_version 0.1 as frozen for implementation.



---

## Page 7


QNetBench Codex Execution Control Plan  |  v0.1
Page 7
What Codex must not do yet
Stop boundary
- Do not implement Pydantic models, loader, hashing, adapters, metrics, or CLI behavior.
- Do not add benchmark catalog values beyond the minimal contract example.
- Do not weaken strictness for convenience.
- Do not add backend extensions to the alpha examples.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- List every normative schema and example with validation result.
- Call out any ambiguity resolved relative to the original manual.
- Include the explicit statement that no production runtime behavior was added.
Required final status line
STATUS: COMPLETE - Checkpoint 1 only. STOP. Next allowed checkpoint: 2.
Checkpoint 2: Benchmark loading, normalization, and hashing
Goal
Implement the BenchmarkSpec v0.1 runtime model exactly as frozen, with safe YAML/JSON loading, strict errors, 
deterministic normalization, and a golden SHA-256 hash.
Files to create or edit
- pyproject.toml (add Pydantic v2 and PyYAML as runtime dependencies)
- qnetbench/errors.py
- qnetbench/spec/__init__.py
- qnetbench/spec/models.py
- qnetbench/spec/loader.py
- qnetbench/spec/canonicalize.py
- tests/spec/test_models.py
- tests/spec/test_loader.py
- tests/spec/test_hashing.py
- tests/fixtures/spec/valid_equivalent.yaml
- tests/fixtures/spec/valid_equivalent.json
- tests/fixtures/spec/invalid_unknown_field.yaml
- docs/ai_handoff/checkpoint_02_report.md
Tests required
- Valid YAML and JSON load into equivalent strict models.
- Unknown fields and invalid ranges fail with useful field paths.
- Equivalent source formatting and mapping order produce the same canonical JSON and hash.
- Meaningful value or ordered-list changes produce a different hash.
- The checked-in minimal benchmark has a golden expected hash.
- Unsafe YAML constructors are not accepted.
Commands required
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/spec
python -m pytest -q
git diff --check



---

## Page 8


QNetBench Codex Execution Control Plan  |  v0.1
Page 8
Definition of done
- Runtime models conform to the Checkpoint 1 schemas without extra fields.
- load_benchmark returns one typed BenchmarkSpec or a typed ConfigError.
- canonical JSON and benchmark_hash are deterministic and golden-tested.
- No backend or result code is imported by qnetbench.spec.
What Codex must not do yet
Stop boundary
- Do not implement result artifacts, adapters, metrics, runners, or CLI commands.
- Do not change the frozen schemas to make implementation easier.
- Do not add arbitrary CLI overrides or defaults that alter scientific values.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the golden benchmark hash and the two equivalent source files used to prove it.
- List validation error examples and confirm the field paths are human-readable.
Required final status line
STATUS: COMPLETE - Checkpoint 2 only. STOP. Next allowed checkpoint: 3.
Checkpoint 3: Canonical result models and artifact bundle I/O
Goal
Implement the frozen canonical run/result models, invariant validation, safe readers, and atomic bundle writer 
independently of any backend or metric calculation.
Files to create or edit
- qnetbench/results/__init__.py
- qnetbench/results/models.py
- qnetbench/results/validate.py
- qnetbench/artifacts/__init__.py
- qnetbench/artifacts/reader.py
- qnetbench/artifacts/writer.py
- tests/results/test_request_invariants.py
- tests/artifacts/test_bundle_roundtrip.py
- tests/artifacts/test_bundle_failures.py
- tests/fixtures/results/complete_run/
- tests/fixtures/results/failed_run/
- docs/ai_handoff/checkpoint_03_report.md
Tests required
- Complete and failed bundle fixtures validate under different required-file rules.
- Round-trip write/read preserves normalized benchmark, manifest, request records, metric rows, and summary.
- Duplicate/missing request IDs, count mismatches, invalid time relations, and non-finite values fail.
- Writer refuses an existing destination unless overwrite is explicit.
- A failed write does not leave a directory that validates as complete.
- raw/ and optional events.jsonl are ignored by metric-independent validation.
Commands required
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/results tests/artifacts
python -m pytest -q



---

## Page 9


QNetBench Codex Execution Control Plan  |  v0.1
Page 9
git diff --check
Definition of done
- Canonical models exactly implement Contract v0.1.
- The writer uses a temporary sibling and validates before finalization.
- The reader rejects malformed JSONL with file and line context.
- No adapter or metric module is required for bundle round trips.
What Codex must not do yet
Stop boundary
- Do not implement an adapter, mock simulation, standard metric computation, CLI, or sweep.
- Do not make events.jsonl mandatory.
- Do not let raw/ influence validation of scientific fields.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the exact complete and failed fixture layouts.
- Report the atomic-write strategy and any platform limitation observed.
- Include one demonstrated invariant failure and its error message.
Required final status line
STATUS: COMPLETE - Checkpoint 3 only. STOP. Next allowed checkpoint: 4.
Checkpoint 4: Adapter interface, registry, and deterministic mock 
adapter
Goal
Implement the backend boundary and a synthetic deterministic mock adapter that returns canonical records in memory 
and supports the full alpha feature subset.
Files to create or edit
- qnetbench/adapters/__init__.py
- qnetbench/adapters/base.py
- qnetbench/adapters/registry.py
- qnetbench/adapters/mock.py
- tests/adapters/test_support_report.py
- tests/adapters/test_mock_determinism.py
- tests/adapters/test_mock_records.py
- tests/fixtures/mock/golden_seed_1.jsonl
- docs/ai_handoff/checkpoint_04_report.md
Tests required
- SupportReport exposes supported, reasons, unsupported_paths, warnings, and backend identity.
- Same benchmark/hash, seed, and mock algorithm version produce byte-stable canonical request records.
- A tested alternate seed changes at least one stochastic outcome reproducibly.
- Mock records satisfy all canonical invariants and match the planned request count.
- Unsupported protocol or extension paths are rejected before run.
- Mock metadata labels the result synthetic and records mock algorithm version.



---

## Page 10


QNetBench Codex Execution Control Plan  |  v0.1
Page 10
Commands required
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/adapters
python -m pytest -q
git diff --check
Definition of done
- The adapter interface does not know about CLI, plotting, or final bundle layout.
- Mock supports the alpha contract subset used by the future four catalog cases.
- Golden records are intentional, documented, and deterministic.
- No real simulator dependency is present.
What Codex must not do yet
Stop boundary
- Do not compute metrics or write run bundles from the adapter.
- Do not add qnetbench/adapters/sequence.py or any SeQUeNCe dependency.
- Do not claim mock values are physically meaningful.
- Do not implement random routing, purification, or dynamic arrivals.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the mock algorithm version and deterministic seed construction.
- Show support-report output for one supported and one unsupported fixture.
- State explicitly that the mock is synthetic, not a physics baseline.
Required final status line
STATUS: COMPLETE - Checkpoint 4 only. STOP. Next allowed checkpoint: 5.
Checkpoint 5: Backend-independent metric engine
Goal
Implement the exact v0.1 metrics as pure calculations over a validated run manifest and canonical request records, 
including explicit unavailable states and coverage counts.
Files to create or edit
- qnetbench/metrics/__init__.py
- qnetbench/metrics/models.py
- qnetbench/metrics/definitions.py
- qnetbench/metrics/compute.py
- tests/metrics/test_success.py
- tests/metrics/test_latency.py
- tests/metrics/test_fidelity.py
- tests/metrics/test_throughput.py
- tests/metrics/test_attempts.py
- tests/metrics/test_architecture_boundary.py
- docs/ai_handoff/checkpoint_05_report.md
Tests required
- Hand-calculated synthetic fixtures match all metric values exactly or within declared floating tolerance.
- Zero-success runs emit unavailable latency/fidelity/attempt rows, not zero or NaN.
- p95 uses the nearest-rank rule from the contract.



---

## Page 11


QNetBench Codex Execution Control Plan  |  v0.1
Page 11
- Fidelity and attempt coverage_count behavior is tested for complete, partial, and absent data; partial fidelity coverage is 
unavailable.
- Throughput rejects zero/negative measurement windows.
- Static architecture test proves qnetbench.metrics does not import qnetbench.adapters or simulator modules.
Commands required
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/metrics
python -m pytest -q
git diff --check
Definition of done
- All standard metric IDs, units, populations, and edge cases match the frozen contract.
- Metric rows always have stable status/value/unit/population_count/coverage_count fields.
- No metric reads summary.json, events.jsonl, raw/, or an adapter object.
What Codex must not do yet
Stop boundary
- Do not add plots, sweep aggregation, CLI, or backend-specific metrics.
- Do not add generalized resource metrics beyond attempts_per_success.
- Do not modify canonical request fields to simplify a metric.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Include a compact table of each metric fixture, expected value, status, population, and coverage.
- Report the architecture-boundary test method.
Required final status line
STATUS: COMPLETE - Checkpoint 5 only. STOP. Next allowed checkpoint: 6.
Checkpoint 6: Single-run orchestration and CLI through the mock 
backend
Goal
Connect validation, support checking, adapter execution, metric computation, and artifact writing into one single-run 
pipeline and expose the minimal CLI.
Files to create or edit
- qnetbench/runners/__init__.py
- qnetbench/runners/single.py
- qnetbench/cli.py
- pyproject.toml (add qnetbench console script)
- tests/runners/test_single_run.py
- tests/cli/test_validate.py
- tests/cli/test_run.py
- tests/cli/test_summarize.py
- tests/cli/test_validate_result.py
- docs/ai_handoff/checkpoint_06_report.md



---

## Page 12


QNetBench Codex Execution Control Plan  |  v0.1
Page 12
Tests required
- validate succeeds for the minimal benchmark and fails with nonzero exit and field paths for invalid input.
- run --backend mock writes one complete, valid bundle with exact seed/hash/version provenance.
- summarize reads the saved bundle rather than rerunning or reading raw output.
- validate-result detects a deliberately corrupted bundle.
- Existing output directory fails unless --overwrite is explicit.
- A simulated adapter failure creates a valid failed-run bundle and nonzero exit.
Commands required
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/runners tests/cli
qnetbench validate examples/contracts/minimal_benchmark.yaml
qnetbench run examples/contracts/minimal_benchmark.yaml --backend mock --seed 1 --out .tmp/cp06-run
qnetbench validate-result .tmp/cp06-run
qnetbench summarize .tmp/cp06-run
python -m pytest -q
git diff --check
Definition of done
- The single-run pipeline is adapter-neutral and writes only after canonical validation and metric calculation.
- The CLI exposes exactly validate, run, summarize, and validate-result at this checkpoint.
- The demonstrated mock run bundle validates and its metrics recompute identically.
- Temporary smoke artifacts are removed or documented as ignored output.
What Codex must not do yet
Stop boundary
- Do not add the benchmark catalog, list command, sweeps, plots, or SeQUeNCe.
- Do not bypass support checks.
- Do not make summary.json the metric source.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the exact run directory tree and key manifest identifiers.
- Paste the CLI exit codes and concise outputs for validate, run, validate-result, and summarize.
- Report the failed-run bundle test evidence.
Required final status line
STATUS: COMPLETE - Checkpoint 6 only. STOP. Next allowed checkpoint: 7.
Checkpoint 7: Frozen benchmark catalog and user-facing mock 
documentation
Goal
Create the four static alpha benchmarks, catalog discovery/listing, support matrix, and documentation needed for a new 
user to run each case with the mock adapter.
Files to create or edit
- benchmarks/v0_1/link_2_batch.yaml
- benchmarks/v0_1/chain_3_batch.yaml
- benchmarks/v0_1/chain_5_batch.yaml



---

## Page 13


QNetBench Codex Execution Control Plan  |  v0.1
Page 13
- benchmarks/v0_1/grid_3x3_batch.yaml
- benchmarks/v0_1/README.md
- qnetbench/catalog.py
- qnetbench/cli.py (add list command)
- docs/quickstart.md
- docs/adapter_guide.md
- docs/reproducibility.md
- docs/support_matrix.md
- tests/catalog/test_catalog.py
- tests/catalog/test_catalog_mock_runs.py
- tests/cli/test_list.py
- docs/ai_handoff/checkpoint_07_report.md
Tests required
- All four benchmark IDs are unique, match filenames/README, have empty extensions, and validate.
- All four complete through the mock single-run pipeline with deterministic artifacts.
- Grid shortest-path tie-break and sequential swapping choices are documented and tested.
- Catalog listing is stable and does not import or instantiate simulator packages.
- Documentation commands are executed as doctest-style smoke checks or equivalent integration tests.
Commands required
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/catalog tests/cli/test_list.py
qnetbench list
qnetbench run benchmarks/v0_1/link_2_batch.yaml --backend mock --seed 1 --out .tmp/cp07-link
qnetbench run benchmarks/v0_1/chain_3_batch.yaml --backend mock --seed 1 --out .tmp/cp07-chain3
qnetbench run benchmarks/v0_1/chain_5_batch.yaml --backend mock --seed 1 --out .tmp/cp07-chain5
qnetbench run benchmarks/v0_1/grid_3x3_batch.yaml --backend mock --seed 1 --out .tmp/cp07-grid
python -m pytest -q
git diff --check
Definition of done
- The four benchmark values are frozen and their hashes are recorded in benchmarks/v0_1/README.md.
- All four mock bundles validate and complete within the documented smoke budget.
- Docs accurately describe only implemented behavior.
- Support matrix marks SeQUeNCe as not started and does not imply support.
What Codex must not do yet
Stop boundary
- Do not add topology/workload generator APIs.
- Do not add random routing, purification, dynamic arrivals, or more benchmark files.
- Do not start sweep implementation or SeQUeNCe research.
- Do not alter the frozen contract fields.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report all four benchmark IDs, hashes, request counts, and mock run durations.
- Report the deterministic grid tie-break rule.
- Confirm no backend-specific extension appears in any frozen benchmark.
Required final status line
STATUS: COMPLETE - Checkpoint 7 only. STOP. Next allowed checkpoint: 8.



---

## Page 14


QNetBench Codex Execution Control Plan  |  v0.1
Page 14
Checkpoint 8: Finite sweep, aggregate analysis, plots, and mock-
pipeline release gate
Goal
Implement the separate SweepSpec, bounded cartesian expansion, sequential sweep runner, deterministic aggregate 
CSV, minimal plotting, and prove the full mock pipeline is ready before any SeQUeNCe work.
Files to create or edit
- qnetbench/sweeps/__init__.py
- qnetbench/sweeps/models.py
- qnetbench/runners/sweep.py
- qnetbench/analysis/__init__.py
- qnetbench/analysis/aggregate.py
- qnetbench/analysis/plots.py
- qnetbench/cli.py (add sweep and plot commands)
- sweeps/v0_1/link_loss_small.yaml
- docs/mock_pipeline_gate.md
- tests/sweeps/test_expansion.py
- tests/sweeps/test_runner.py
- tests/analysis/test_aggregate.py
- tests/analysis/test_plots.py
- tests/cli/test_sweep.py
- docs/ai_handoff/checkpoint_08_report.md
Tests required
- Sweep expansion order is deterministic and the one checked-in sweep expands to at most nine unique execution hashes.
- An expansion above 100 runs is rejected before execution.
- Sequential sweep writes sweep_manifest.json, child run bundles, and aggregate_metrics.csv.
- Aggregate calculations handle unavailable metrics and use n_runs/n_ok correctly.
- Plot command creates only the approved success-probability and latency plots from aggregate_metrics.csv.
- Existing sweep directory fails; resume, retry, parallelism, and implicit overwrite are absent.
- The complete mock-pipeline gate test runs all four benchmarks plus the checked-in sweep.
Commands required
python -m pip install -e ".[dev,plot]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/sweeps tests/analysis tests/cli/test_sweep.py
qnetbench sweep sweeps/v0_1/link_loss_small.yaml --backend mock --out .tmp/cp08-sweep
qnetbench plot .tmp/cp08-sweep
python -m pytest -q
git diff --check
Definition of done
- The full mock pipeline passes from clean install through contracts, four single runs, finite sweep, aggregate CSV, and 
plots.
- docs/mock_pipeline_gate.md records commands, hashes, artifact paths, and observed results.
- PROJECT_STATE.md sets mock_pipeline_ready: true only after all gate evidence passes.
- Default CI remains independent of SeQUeNCe; plotting dependency is handled by the approved extra or baseline 
decision.
What Codex must not do yet
Stop boundary
- Do not add parallelism, resume, retries, conditional axes, random search, databases, or dashboards.
- Do not create or edit qnetbench/adapters/sequence.py.
- Do not begin SeQUeNCe research unless this checkpoint is complete and reported.



---

## Page 15


QNetBench Codex Execution Control Plan  |  v0.1
Page 15
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the exact sweep expansion table and total run count.
- List aggregate CSV columns and plot filenames.
- Provide the explicit mock-pipeline-ready evidence and PROJECT_STATE flag.
Required final status line
STATUS: COMPLETE - Checkpoint 8 only. STOP. Next allowed checkpoint: 9.
Checkpoint 9: Verified SeQUeNCe research spike - no production 
adapter
Goal
Verify the current SeQUeNCe source, installation, executable minimal example, seed control, API symbols, output 
extraction, and field mapping for the two alpha cases. Produce an implementation-ready research record without 
production adapter code.
Files to create or edit
- docs/research/sequence_notes.md
- docs/research/sequence_field_mapping.md
- docs/research/sequence_support_matrix.md
- docs/decisions/ADR-0002-sequence-alpha-integration.md
- tools/research/sequence_smoke.py (standalone research tool only, if needed)
- PROJECT_STATE.md
- docs/ai_handoff/checkpoint_09_report.md or docs/blockers/<date>-sequence-research.md
Tests required
- All existing default tests remain green.
- A repository check proves qnetbench/adapters/sequence.py does not exist.
- The research smoke example is executed in an isolated environment and its exact command/output is recorded.
- Required API observations are cited to upstream docs/source/example locations and are not inferred from memory.
- The mapping marks every common alpha field supported, fixed, approximated with approval, or unsupported; silent gaps 
are forbidden.
Commands required
python3.12 -m venv .venv-sequence
. .venv-sequence/bin/activate
python -m pip install --upgrade pip
python -m pip install sequence  # current official command; re-verify and record exact version
<run the exact verified upstream minimal example command>
python tools/research/sequence_smoke.py  # only if the research tool is created
deactivate
python -m pytest -q
test ! -e qnetbench/adapters/sequence.py
git diff --check
Definition of done
- The exact upstream revision, license, Python compatibility, install command, and dependency constraints are recorded.
- A minimal upstream or standalone example runs successfully outside production QNetBench code.
- The notes identify verified methods for timeline execution, topology/channel setup, memory setup, request submission, 
success detection, timing, fidelity, attempts if available, and seed control.
- ADR-0002 fixes the narrow support and normalization strategy for Checkpoint 10.
- If any required point remains unknown, the checkpoint is BLOCKED and no adapter work begins.



---

## Page 16


QNetBench Codex Execution Control Plan  |  v0.1
Page 16
What Codex must not do yet
Stop boundary
- Do not create qnetbench/adapters/sequence.py.
- Do not change the common contracts to mirror SeQUeNCe internals.
- Do not claim cross-backend numerical agreement.
- Do not expand support beyond link-2 and chain-3.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the exact verified install and smoke commands, upstream revision, and environment.
- List every API symbol used with source location.
- State a go/no-go decision for Checkpoint 10 and unresolved risks.
Required final status line
STATUS: COMPLETE - Checkpoint 9 only. STOP. Next allowed checkpoint: 10.
Checkpoint 10: Narrow SeQUeNCe adapter MVP and integration 
validation
Goal
Implement the verified adapter for exactly the two-node link and three-node chain, normalize real outputs to the 
canonical contract, reject all other alpha cases before execution, and validate the integration honestly.
Files to create or edit
- qnetbench/adapters/sequence.py
- qnetbench/adapters/registry.py
- pyproject.toml (verified sequence optional extra and pytest marker)
- docs/support_matrix.md
- docs/adapter_guide.md
- tests/adapters/test_sequence_support.py
- tests/integration/test_sequence_link_2.py
- tests/integration/test_sequence_chain_3.py
- tests/integration/test_sequence_rejections.py
- .github/workflows/sequence.yml (manual/optional, only if feasible)
- docs/ai_handoff/checkpoint_10_report.md
Tests required
- Without the optional dependency, importing qnetbench and running default tests still succeeds with a clear unavailable 
backend report.
- Support checks accept only link_2_batch and chain_3_batch within the frozen field subset.
- chain_5_batch, grid_3x3_batch, extensions, purification, and unsupported fields reject before simulator creation.
- Both supported cases run with explicit seed and create complete canonical bundles.
- Manifest captures exact SeQUeNCe version/revision and adapter version.
- Request count, IDs, time monotonicity, status/fidelity ranges, and metric recomputation validate.
- Repeated fixed-seed runs are reproducible to the extent verified; any nondeterminism is documented, not hidden.
Commands required
python -m pip install -e ".[dev,sequence]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q -m "not sequence"
python -m pytest -q -m sequence
qnetbench run benchmarks/v0_1/link_2_batch.yaml --backend sequence --seed 1 --out .tmp/cp10-seq-link



---

## Page 17


QNetBench Codex Execution Control Plan  |  v0.1
Page 17
qnetbench validate-result .tmp/cp10-seq-link
qnetbench run benchmarks/v0_1/chain_3_batch.yaml --backend sequence --seed 1 --out .tmp/cp10-seq-chain3
qnetbench validate-result .tmp/cp10-seq-chain3
python -m pytest -q
git diff --check
Definition of done
- Both required SeQUeNCe runs complete using only verified APIs and produce valid bundles/metrics.
- Unsupported catalog cases fail clearly and early.
- Default installation and CI still work without SeQUeNCe.
- Docs state the exact supported revision and limitations.
- No real-backend result is substituted, patched, or generated by the mock adapter.
What Codex must not do yet
Stop boundary
- Do not support chain-5 or grid even if experiments appear promising.
- Do not add another backend, purification, random routing, or dynamic workload behavior.
- Do not change common metrics or contracts to fit backend output.
- Do not make SeQUeNCe mandatory in default CI.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report exact SeQUeNCe revision, install command, run commands, durations, hashes, and artifact paths.
- Include support/rejection evidence for all four frozen benchmarks.
- Separate simulator observations from QNetBench validation conclusions.
Required final status line
STATUS: COMPLETE - Checkpoint 10 only. STOP. Next allowed checkpoint: 11.
Checkpoint 11: Alpha hardening, release validation, and 0.1.0a1 
candidate
Goal
Complete sanity and architecture validation, clean packaging and documentation, update release metadata, prove clean-
environment installation, and stop with a release candidate ready for human authorization.
Files to create or edit
- qnetbench/validation/__init__.py
- qnetbench/validation/sanity.py
- tests/validation/test_sanity.py
- tests/validation/test_architecture_boundaries.py
- tests/release/test_mock_release_smoke.py
- tests/release/test_contract_artifacts.py
- docs/release/v0_1_alpha_checklist.md
- README.md
- CHANGELOG.md
- CITATION.cff
- pyproject.toml
- .github/workflows/ci.yml
- PROJECT_STATE.md
- docs/ai_handoff/checkpoint_11_report.md



---

## Page 18


QNetBench Codex Execution Control Plan  |  v0.1
Page 18
Tests required
- No-loss/high-success and extreme-loss/low-success synthetic sanity cases have directionally correct outcomes without 
asserting exact physics.
- Architecture tests prove simulator imports are isolated to the SeQUeNCe adapter/research tool and metrics do not 
import adapters.
- All four mock catalog runs and the small sweep pass as release smoke tests.
- Both SeQUeNCe integration cases pass in the verified environment and unsupported cases reject.
- Wheel and source distribution build, wheel installs in a clean Python 3.12 environment, CLI version is 0.1.0a1, and a 
mock run succeeds.
- Documentation commands and artifact examples match actual output.
Commands required
python -m pip install -e ".[dev,plot]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python -m build
mkdir -p .tmp
cp benchmarks/v0_1/link_2_batch.yaml .tmp/release-link.yaml
python3.12 -m venv .tmp/release-venv
. .tmp/release-venv/bin/activate
python -m pip install dist/qnetbench-0.1.0a1-*.whl
qnetbench --version
qnetbench run .tmp/release-link.yaml --backend mock --seed 1 --out .tmp/release-smoke
qnetbench validate-result .tmp/release-smoke
deactivate
. .venv-sequence/bin/activate
python -m pip install -e ".[dev,sequence]"
python -m pytest -q -m sequence
deactivate
git diff --check
git status --short
Definition of done
- Every item in docs/release/v0_1_alpha_checklist.md is checked with evidence or explicitly marked human-only.
- Package metadata, README, CHANGELOG, CITATION.cff, CLI version, and built artifact version agree on 0.1.0a1.
- There are no known failing required tests, invalid example bundles, or release-blocking blockers.
- PROJECT_STATE.md states release_candidate_ready: true and next_action: await human release authorization.
- Checkpoint 11 report includes artifact names and hashes for the built distributions.
What Codex must not do yet
Stop boundary
- Do not create a Git tag, push branches, open a release, publish to PyPI, mint a DOI, or submit a paper without explicit 
authorization.
- Do not add last-minute features or second adapters.
- Do not relax tests or contracts to make the release pass.
Expected stop/report format
Use the standard checkpoint report template in Section 5 and include these checkpoint-specific items:
- Report the final version, full command matrix, test counts/skips, build artifact filenames and SHA-256 hashes.
- Report mock and SeQUeNCe release-smoke evidence separately.
- End with exactly: STOP - 0.1.0a1 release candidate ready; awaiting human authorization.
Required final status line
STATUS: COMPLETE - Checkpoint 11 only. STOP. Next allowed checkpoint: none; await human release authorization.



---

## Page 19


QNetBench Codex Execution Control Plan  |  v0.1
Page 19
5. Proposed checkpoint report template
Save as docs/ai_handoff/checkpoint_XX_report.md. Replace every placeholder. Do not omit failed or skipped 
commands.
# Checkpoint XX Report: <name>
Status: COMPLETE | BLOCKED
Date (UTC): YYYY-MM-DD
Branch: <branch>
Commit: <SHA or "not committed">
Previous good commit: <SHA>
Active contract versions: benchmark 0.1; result 0.1; metrics 0.1
## Scope completed
- <one factual outcome per line>
## Files created
- <path>
## Files edited
- <path>
## Tests added or changed
- <test path>: <behavior proved>
## Commands run
| Command | Exit | Result |
|---|---:|---|
| `<exact command>` | 0 | <concise observed output> |
## Artifact evidence
- <path, run_id, benchmark_hash, execution_hash, or N/A>
## Contract and architecture checks
- BenchmarkSpec changed: no | approved change reference
- Canonical result contract changed: no | approved change reference
- Metrics read canonical outputs only: yes | N/A
- Backend-specific imports isolated: yes | N/A
## Assumptions and decisions
- <assumption used; cite ADR when applicable>
## Deviations from checkpoint plan
- None | <exact deviation and approval>
## Open issues and risks
- None | <issue>
## PROJECT_STATE.md update
- Current checkpoint/result: <value>
- Last passing command: <value>
- Next allowed action: <value>
## Final status
STATUS: COMPLETE - Checkpoint XX only. STOP.
Next allowed checkpoint: <N or await human authorization>.
6. Proposed blocker report template
Save as docs/blockers/YYYY-MM-DD-short-title.md and update PROJECT_STATE.md to BLOCKED. A blocker report 
replaces, rather than accompanies, a false completion claim.
# Blocker: <short title>
Date (UTC): YYYY-MM-DD
Checkpoint: <number and name>
Branch: <branch>
Last good commit: <SHA>
Current commit/worktree: <SHA or dirty>
Severity: release-blocking | checkpoint-blocking
## Required outcome that cannot be met
<quote the checkpoint definition of done item>
## Exact command that fails
```bash



---

## Page 20


QNetBench Codex Execution Control Plan  |  v0.1
Page 20
<command>
```
## Relevant output
```text
<full relevant traceback/log; do not paraphrase away the cause>
```
## Minimal reproduction
1. <clean checkout/environment step>
2. <install step>
3. <failing command>
## What was tried
- <attempt and result>
## Evidence gathered
- <version, file, upstream source, log, or artifact>
## Current hypotheses
1. <hypothesis, evidence for/against>
## Scope-safe next steps
- <next diagnostic that stays inside this checkpoint>
## Actions explicitly not taken
- No tests deleted or weakened.
- No contract changed.
- No mock data substituted for real backend data.
- No future checkpoint started.
## Decision requested from human/controller
<specific question, approval, or missing input>
STATUS: BLOCKED - Checkpoint <N>. STOP.
7. Proposed AGENTS.md
# AGENTS.md - QNetBench
## Mission
QNetBench is a benchmark and reproducibility layer above quantum-network
simulators. It is not a simulator.
## Read before editing
1. PROJECT_STATE.md
2. docs/contracts/ and schemas/v0_1/
3. QNetBench Improved AI Handoff Manual v0.2
4. QNetBench Codex Execution Control Plan v0.1
5. Latest docs/ai_handoff/checkpoint_*_report.md
6. Open docs/blockers/ and relevant docs/decisions/ ADRs
## Work control
- Work on exactly one active checkpoint.
- Preserve unrelated human changes.
- Run all commands required by the checkpoint.
- Update PROJECT_STATE.md and write a checkpoint or blocker report.
- Stop after reporting. Do not start the next checkpoint.
## Architectural invariants
- BenchmarkSpec is backend-independent. Backend, seed, output, and sweeps are
  execution concerns.
- Canonical result records and the run manifest are the only metric inputs.
- Metrics must never import adapters or read raw backend output.
- Simulator-specific imports and API calls stay in qnetbench/adapters/<name>.py
  or an approved tools/research/ script.
- Adapters report unsupported fields explicitly; no silent coercion or fallback.
- The mock adapter is synthetic and must complete end to end before SeQUeNCe.
- Do not create qnetbench/adapters/sequence.py before Checkpoint 10.
- Do not change frozen contracts, hashes, benchmark values, or metric semantics
  without explicit approval and an ADR/version decision.
## Alpha scope
Target release: 0.1.0a1 after Checkpoint 11.
Required backends: mock; SeQUeNCe for link-2 and chain-3 only.
Required catalog: link-2, chain-3, chain-5, grid-3x3.
Out of scope: new simulators, purification, random/adaptive routing, dynamic
arrivals, generalized resource metrics, parallel/resumable sweeps, dashboards,
paper publication, DOI creation, and additional adapters.
## Standard commands



---

## Page 21


QNetBench Codex Execution Control Plan  |  v0.1
Page 21
```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
```
Use the checkpoint section for additional commands.
## Test and evidence rules
- Never delete or weaken a test to advance a checkpoint.
- Never claim a command ran unless it ran in the current environment.
- Never fabricate artifacts or substitute mock output for a real backend.
- Record exact commands, exit codes, hashes, versions, and artifact paths.
- Default CI must not require SeQUeNCe.
## Blockers
Stop and write docs/blockers/YYYY-MM-DD-short-title.md when:
- a required command cannot pass within scope;
- authoritative instructions conflict;
- a frozen assumption must change;
- a simulator API/install/license cannot be verified; or
- unrelated changes would be overwritten.
## Publishing
Do not push, force-push, tag, publish packages, create a GitHub release, mint a
DOI, or make external scientific claims without explicit human authorization.
8. Proposed PROJECT_STATE.md template
# QNetBench Project State
Last updated (UTC): YYYY-MM-DD HH:MM
Status: NOT_STARTED | IN_PROGRESS | COMPLETE | BLOCKED
Active checkpoint: <number and name>
Last completed checkpoint: <number and name or none>
Branch: <branch>
Last good commit: <SHA>
Working tree: clean | dirty (<summary>)
## Release target
- Target version: 0.1.0a1
- Current package version: <version>
- Benchmark contract: 0.1 <draft|frozen>
- Result contract: 0.1 <draft|frozen>
- Metrics contract: 0.1 <draft|frozen>
- mock_pipeline_ready: false | true
- sequence_research_verified: false | true
- release_candidate_ready: false | true
## Environment last verified
- Python: <version>
- Platform: <value>
- Install command: <command>
- SeQUeNCe revision/environment: <N/A or exact value>
## Last passing commands
- `<command>` - <date/commit>
## What works now
- <capability with evidence path>
## What is intentionally not implemented
- <future checkpoint or out-of-scope item>
## Open blockers
- None | <link to docs/blockers/...>
## Frozen assumptions in force
- <short reference to Section 9 of the execution plan>
## Latest checkpoint evidence
- Report: docs/ai_handoff/checkpoint_XX_report.md
- Representative artifacts: <path or N/A>
- Golden hashes: <path or N/A>
## Next allowed action
<one checkpoint-sized action only>
## Notes for the next agent
- <specific warning; no narrative history>



---

## Page 22


QNetBench Codex Execution Control Plan  |  v0.1
Page 22
9. Assumptions that must not be silently changed
1.  The package and CLI name are qnetbench.
2.  The target after Checkpoint 11 is 0.1.0a1, not a stable 0.1.0 release.
3.  The checkpoint sequence is exactly 0 through 11. No additional implementation checkpoint is inserted without 
human approval.
4.  Python 3.12 is the required alpha baseline.
5.  Packaging uses pyproject.toml, setuptools, and pip-based commands. A different package manager or build 
backend requires approval.
6.  The alpha license is BSD-3-Clause unless changed by the human owner before Checkpoint 0 approval.
7.  Pydantic v2, PyYAML, and Typer are the approved core runtime libraries. Matplotlib is introduced only for 
plotting. No dependency is added merely for convenience.
8.  BenchmarkSpec v0.1 is backend-independent and excludes backend, seed, output, and sweep fields.
9.  Unknown benchmark/result fields are rejected. The alpha catalog uses no extensions.
10.  The benchmark hash is SHA-256 over the frozen canonical JSON procedure and is protected by golden fixtures.
11.  RunRequest and SweepSpec are separate from BenchmarkSpec.
12.  A sweep is a deterministic cartesian product, runs sequentially, has a hard cap of 100, and has no 
resume/parallel/retry behavior.
13.  A complete canonical bundle requires benchmark.yaml, run_manifest.json, requests.jsonl, metrics.csv, and 
summary.json. events.jsonl and raw/ are optional.
14.  There is exactly one terminal request record per planned request in a complete run.
15.  Metrics use only run_manifest.json and requests.jsonl. raw/, events.jsonl, summary.json, and adapter objects are 
never metric inputs.
16.  The standard alpha metrics are success probability; mean, median, and p95 successful latency; mean and median 
successful fidelity; throughput; and attempts per success.
17.  Generalized resource utilization, confidence intervals, and statistical tests are post-alpha.
18.  The mock adapter is synthetic, deterministic, and supports all four frozen benchmarks.
19.  The alpha benchmark catalog has exactly link-2, chain-3, chain-5, and grid-3x3 static files with batch requests, 
deterministic shortest path, sequential swapping, and no purification.
20.  SeQUeNCe research begins only after the Checkpoint 8 mock gate. Production sequence.py begins only at 
Checkpoint 10.
21.  SeQUeNCe alpha support is exactly link-2 and chain-3. Chain-5 and grid-3x3 reject even if experimental code 
could run them.
22.  Default CI does not install or require SeQUeNCe.
23.  No mock output may be labeled or stored as SeQUeNCe output.
24.  No schema, benchmark value, metric semantic, hash procedure, Python baseline, license, dependency boundary, 
or backend support boundary changes without explicit approval.
25.  Codex does not push, tag, publish, create releases, mint a DOI, or make scientific claims without human 
authorization.
10. Exact first Codex prompt for Checkpoint 0
Copy the prompt below exactly, attach or place both planning documents in the repository, and give Codex access to 
the repository. Replace only the repository-specific note in angle brackets when necessary.
You are Codex acting as the implementation agent for QNetBench.
Execute Checkpoint 0 only: Repository control plane and minimal package skeleton.
Do not implement any later checkpoint.
Authoritative inputs:
1. QNetBench Improved AI Handoff Manual v0.2
2. QNetBench Codex Execution Control Plan v0.1
3. The current repository and any explicit human instruction in this prompt
First inspect, without editing:
- pwd



---

## Page 23


QNetBench Codex Execution Control Plan  |  v0.1
Page 23
- git status --short --branch
- find . -maxdepth 3 -type f | sort
- any existing AGENTS.md, PROJECT_STATE.md, README.md, pyproject.toml, CI files,
  and checkpoint reports
Preserve all unrelated human work. If the existing repository materially
conflicts with Checkpoint 0, stop and create a blocker report rather than
rewriting it.
Checkpoint 0 goal:
Create a clean, installable repository control plane with one importable
qnetbench package, governance files, default CI, and no product behavior.
Create or edit only these files unless an existing repository requires a
scope-safe equivalent:
- AGENTS.md
- PROJECT_STATE.md
- pyproject.toml
- README.md
- LICENSE
- CHANGELOG.md
- .gitignore
- Makefile
- .github/workflows/ci.yml
- qnetbench/__init__.py
- tests/test_import.py
- docs/ai_handoff/checkpoint_00_report.md
Use these fixed decisions:
- Python baseline: 3.12
- Package name: qnetbench
- Version: 0.0.0.dev0
- Build backend: setuptools
- Developer workflow: pip, pytest, Ruff
- License: BSD-3-Clause
- No CLI entry point yet
- No schema, result model, adapter, metric, runner, benchmark, sweep, plot, or
  SeQUeNCe dependency yet
pyproject.toml must use PEP 621 metadata and define a development extra with
pytest, Ruff, and build. Do not declare runtime dependencies yet; they are added
only by the checkpoints that use them. Do not add mypy, pre-commit, tox/nox,
coverage gates, a lockfile, or unrelated frameworks.
README.md must state that QNetBench is a benchmark layer, not a simulator, and
that the repository is at Checkpoint 0 with contracts not yet implemented.
AGENTS.md and PROJECT_STATE.md must follow the proposed templates in the
execution plan, adapted only for the current state.
Required tests:
- editable install imports qnetbench
- qnetbench.__version__ exists and equals 0.0.0.dev0
Run exactly:
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
If all commands pass:
- update PROJECT_STATE.md so Checkpoint 0 is complete and Checkpoint 1 is the
  only next allowed action;
- write docs/ai_handoff/checkpoint_00_report.md using the report template;
- commit the checkpoint only if git author identity and repository permissions
  are already configured; otherwise report the uncommitted state;
- stop.
Do not start Checkpoint 1. Do not create contract schemas or implementation
stubs for future modules.
Your final response must use this order:
1. STATUS: COMPLETE or BLOCKED
2. Checkpoint and commit SHA
3. Files created/edited
4. Tests added
5. Commands run with exit codes and concise observed results
6. Assumptions/deviations
7. PROJECT_STATE.md result
8. Next allowed action
9. Final line exactly:
   STATUS: COMPLETE - Checkpoint 0 only. STOP. Next allowed checkpoint: 1.
   (Use the blocker status line instead if blocked.)
