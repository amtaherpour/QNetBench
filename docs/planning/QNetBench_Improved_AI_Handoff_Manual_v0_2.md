# QNetBench Improved AI Handoff Manual v0.2

_Machine-readable Markdown/text extraction from `QNetBench_Improved_AI_Handoff_Manual_v0_2(1).pdf`._

_Use this file for Codex if PDF reading is unavailable. The original PDF remains the human visual source._



---

## Page 1


QNetBench Improved AI Handoff Manual  |  v0.2
Page 1
QNetBench
Improved AI Handoff Manual
Contract-first guidance for a reusable quantum-network benchmark suite
Version 0.2
Prepared July 10, 2026
Scope locked: Checkpoints 0 through 11, ending at QNetBench 0.1.0a1
This manual supersedes the v0.1 planning guide where the two documents differ. The companion Codex Execution 
Control Plan contains the checkpoint instructions.
This document is planning and control guidance. It contains no implementation code.



---

## Page 2


QNetBench Improved AI Handoff Manual  |  v0.2
Page 2
Contents
This contents list is intentionally page-number free so it remains stable across renderers.
1. Audit of the original handoff manual
2. Authority, read order, and interpretation
3. Product definition and v0.1-alpha release boundary
4. Non-negotiable architecture rules
5. Contract-first system architecture
6. Benchmark specification contract v0.1
7. Execution request and sweep contract
8. Canonical result and artifact contract v0.1
9. Standard metric definitions v0.1
10. Backend adapter contract
11. Mock backend contract and mock-pipeline gate
12. Frozen alpha benchmark catalog
13. Testing, validation, and quality gates
14. Checkpoint and handoff discipline
15. SeQUeNCe research and adapter boundary
16. Definition of QNetBench 0.1.0a1
17. Change control and post-v0.1 work
18. Final handoff checklist



---

## Page 3


QNetBench Improved AI Handoff Manual  |  v0.2
Page 3
1. Audit of the original handoff manual
The original v0.1 manual is a strong planning document. Its central architectural instincts are correct. The main 
improvement needed is not a larger feature list; it is a more explicit contract boundary, a narrower alpha release, and 
acceptance criteria that leave less room for an AI to improvise.
1.1 What is strong
- It correctly positions QNetBench as a benchmark and reproducibility layer above existing simulators, not as a new 
simulator.
- It makes the benchmark specification and canonical result format the architectural center of the project.
- It isolates simulator-specific logic in adapters and prohibits metrics from depending on backend-specific logs.
- It requires a deterministic mock backend before any SeQUeNCe adapter work.
- It uses ordered checkpoints, tests, Git commits, PROJECT_STATE.md, checkpoint reports, and blocker reports to 
make AI work resumable.
- It explicitly warns against invented simulator APIs and recommends a research spike before production adapter 
code.
- It gives a sensible first real-backend boundary: two-node link generation and a three-node repeater chain.
1.2 What is unclear
- The example benchmark file mixes the benchmark definition with backend selection, backend version constraints, 
seeds, and sweep orchestration. That weakens the idea of one benchmark being reusable across backends.
- The canonical source of truth is ambiguous. events.jsonl, summary.json, metrics.csv, and an in-memory 
CanonicalResult are all described, but their authority and derivation order are not fully specified.
- Metric populations and denominators are not defined precisely. For example, latency might mean successful 
requests only or all terminal requests; throughput needs an exact measurement window; attempts per success 
needs a coverage rule.
- The alpha support boundary is inconsistent: four benchmark scenarios are listed, but the SeQUeNCe MVP 
supports only two; the release definition does not state which combinations are mandatory.
- Schema evolution, canonicalization, run identity, failed-run artifacts, and explicit support-rejection behavior need 
stronger rules.
- The original file tree is presented as a likely implementation rather than as a dependency boundary. An AI could 
optimize for matching file count instead of satisfying contracts.
- The example project-state baseline of Python 3.11 is no longer safe for the planned real backend: the official 
SeQUeNCe README checked for this revision requires Python 3.12 or later. The alpha baseline is therefore 3.12 
and must be re-verified at the research checkpoint.
1.3 What is over-scoped
- Random routing, multiple protocol variants, reusable topology/workload generators, general resource-usage 
metrics, multiple plot types, paper figures, Zenodo publication, and future adapters are too much for the first 
alpha.
- A 3x3 grid and five-node chain are useful catalog cases, but they need not be supported by SeQUeNCe in the 
alpha.
- A citation and paper strategy is valuable, but a DOI, paper-figure pipeline, and cross-simulator scientific claims 
should not block the software alpha.
- Targeting a specific total number of Python files is not a product requirement and can encourage unnecessary 
abstraction.
1.4 What is missing
- A distinction between normative contracts and informative examples.
- A contract-freeze checkpoint before runtime implementation.
- A required per-request terminal record that gives metrics a stable, backend-independent input population.
- A metric availability model for values a backend cannot expose, without silently dropping rows or emitting NaN.
- A structured backend support report with unsupported field paths and reasons.
- Atomic artifact writing, failed-run bundles, duplicate request detection, and result-bundle validation.
- Architecture tests that detect forbidden imports, especially adapters imported by metrics or SeQUeNCe imported 
outside its adapter.
- A precise, finite release gate for 0.1.0a1.



---

## Page 4


QNetBench Improved AI Handoff Manual  |  v0.2
Page 4
1.5 What should be simplified
- Keep benchmark files static in v0.1-alpha. Do not build scenario or workload generator modules until repetition 
justifies them.
- Use one deterministic shortest-path rule and one fixed sequential-swapping baseline. Defer random routing and 
purification.
- Separate BenchmarkSpec, RunRequest, and SweepSpec rather than placing all concerns in one YAML file.
- Require one small sweep and one standard plot family, not a general analysis framework.
- Treat attempts per success as the alpha resource proxy. Defer generalized memory, queue, and device-utilization 
metrics.
- Prepare citation metadata at release, but do not make publication, DOI minting, or paper figures part of the Codex 
checkpoint path.
1.6 What should remain unchanged
Core idea to preserve
QNetBench is a benchmark layer, not a new simulator. The benchmark specification and canonical result format are 
central. Metrics use canonical outputs only. Backend-specific code stays inside adapters. SeQUeNCe work starts only 
after the complete mock pipeline passes. Work remains finite, checkpoint-based, and stops after every checkpoint.
2. Authority, read order, and interpretation
Future AI assistants and collaborators must treat this manual as a project contract, not as brainstorming. The 
companion execution plan turns the contract into checkpoint tasks.
2.1 Required read order
1.  The current human instruction or approved checkpoint issue.
2.  AGENTS.md.
3.  PROJECT_STATE.md.
4.  The versioned contract documents under docs/contracts/ and schemas/.
5.  This Improved AI Handoff Manual.
6.  The Codex Execution Control Plan.
7.  The latest completed checkpoint report, open blocker reports, relevant ADRs, and CI logs.
2.2 Precedence and conflicts
- A current explicit human instruction outranks repository planning text.
- Versioned technical contracts outrank examples and README prose.
- PROJECT_STATE.md states current progress; it does not silently alter contracts.
- An approved ADR may clarify a contract, but a breaking contract change requires explicit human approval and a 
versioning decision.
- When two authoritative sources conflict, stop and file a blocker. Do not choose the convenient interpretation 
silently.
2.3 Normative language
MUST and MUST NOT are hard requirements. SHOULD is the default unless a checkpoint report records a justified 
deviation. MAY is optional. Examples are informative unless they are explicitly named as golden fixtures.
3. Product definition and v0.1-alpha release boundary
3.1 Product definition
QNetBench is a Python package and command-line benchmark layer for reproducible quantum-network 
entanglement-distribution experiments. It validates backend-independent benchmark specifications, executes them 
through adapters, normalizes each run into a canonical result bundle, computes standard metrics from canonical 
records, and runs finite parameter sweeps.



---

## Page 5


QNetBench Improved AI Handoff Manual  |  v0.2
Page 5
3.2 The alpha must deliver
- A strict BenchmarkSpec v0.1 with stable normalization and SHA-256 benchmark hashing.
- A Canonical Result Contract v0.1 with validated run manifests and one terminal canonical record per workload 
request.
- A deterministic mock adapter that supports all four frozen alpha benchmark files.
- Backend-independent metrics with exact definitions and explicit unavailable/not-applicable states.
- A single-run CLI, a finite cartesian-product sweep runner, aggregate CSV output, and a minimal plot command.
- A narrow SeQUeNCe adapter for exactly the two-node link and three-node repeater-chain benchmark cases.
- Default CI that does not require SeQUeNCe, plus documented optional SeQUeNCe integration tests.
- User and contributor documentation, a clean package build, CHANGELOG.md, LICENSE, and CITATION.cff.
3.3 Non-goals for 0.1.0a1
- Building a simulator, quantum-hardware interface, scheduler, network service, or web application.
- Supporting every physical model, protocol, workload, simulator, or topology.
- Random routing, purification, adaptive control, dynamic arrivals, distributed sweeps, parallel execution, or 
resume/retry orchestration.
- Generalized resource-utilization benchmarking beyond canonical attempt counts.
- Numerical equivalence claims between the mock adapter and SeQUeNCe, or between different real simulators.
- Publishing a paper, minting a DOI, or adding a second real simulator adapter.
Finite boundary
Checkpoint 11 ends the plan. The release target is 0.1.0a1. Any feature not named in the alpha definition is out of scope 
unless a human explicitly replaces the checkpoint plan.
Current compatibility correction
The official SeQUeNCe repository checked July 10, 2026 states Python 3.12 or later. QNetBench therefore uses Python 
3.12 as its single alpha baseline. Checkpoint 9 must re-verify this before the optional dependency is pinned.
4. Non-negotiable architecture rules
1.  QNetBench MUST remain a benchmark layer and MUST NOT implement a general discrete-event quantum-
network simulator.
2.  Benchmark files MUST be backend-independent. Backend name, seed, output path, and sweep axes are execution 
concerns, not benchmark-definition fields.
3.  The BenchmarkSpec and Canonical Result Contract are the only cross-module data contracts. Their v0.1 forms are 
frozen at Checkpoint 1.
4.  Metrics MUST read only canonical request records and the canonical run manifest. They MUST NOT read raw 
backend logs, adapter objects, simulator events, or backend-specific metadata.
5.  All imports and calls to a simulator package MUST remain in that simulator adapter or a clearly separated research 
tool.
6.  Adapters MUST report unsupported fields explicitly and MUST NOT coerce, ignore, or approximate an 
unsupported benchmark silently.
7.  The mock adapter MUST be complete end to end before production SeQUeNCe adapter work begins.
8.  The mock adapter MUST be labeled synthetic and MUST NOT be presented as a physics reference.
9.  Every run MUST be reproducible or explain why it is not, using hashes, seeds, versions, and a saved resolved 
benchmark.
10.  Every checkpoint MUST finish with passing required commands, an updated PROJECT_STATE.md, and a 
checkpoint or blocker report, then stop.
11.  A failed checkpoint MUST NOT be bypassed by deleting tests, weakening assertions, inventing data, or 
expanding scope elsewhere.
12.  No release, push, tag, package publication, DOI action, or external claim is performed without explicit human 
authorization.



---

## Page 6


QNetBench Improved AI Handoff Manual  |  v0.2
Page 6
5. Contract-first system architecture
The architecture has three inputs and one canonical output boundary. The benchmark describes what is measured. A 
run request chooses how one execution is performed. A sweep specification expands into a finite list of run requests.
BenchmarkSpec v0.1
    -> validate -> normalize -> benchmark_hash
RunRequest(benchmark, backend, seed, output)
    -> adapter support check
    -> backend execution
    -> canonical request records + run provenance
    -> metric engine
    -> validated canonical result bundle
SweepSpec(base benchmark, finite parameter axes, seeds)
    -> bounded run plan
    -> repeated single-run pipeline
    -> aggregate_metrics.csv + approved plots
Optional raw backend output -> raw/ only; never a metric input.
5.1 Module dependency direction
Area
May depend on
Must not depend on
spec
standard library, validation library
adapters, metrics, runners, simulator 
packages
results/artifacts
spec, standard models
simulator packages
adapters
spec and result contracts
metrics and analysis
metrics
result contract only
adapters, raw/, simulator packages
runners/CLI
spec, adapters, metrics, artifacts
simulator internals
analysis
metrics tables and canonical bundles
adapter internals, raw/
5.2 Responsibility boundaries
- Adapters translate and run; they do not calculate standard metrics or own final artifact layout.
- The metric engine calculates; it does not know which backend produced the records.
- The artifact layer validates and persists; it does not infer physics or simulator state.
- The runner orchestrates one pipeline; it does not embed backend-specific branches.
- The sweep runner expands only explicit finite axes and delegates each execution to the single-run runner.
6. Benchmark specification contract v0.1
BenchmarkSpec v0.1 is the stable, backend-independent scientific input. The checked-in JSON Schema and contract 
document are normative. YAML and JSON are accepted source encodings, but both normalize to the same model.
6.1 Required conceptual sections
Section
Purpose
schema_version
Exactly "0.1" for this release line.
benchmark_id
Stable, unique, lowercase identifier for the frozen benchmark case.
title / description
Human-readable identity and scientific intent.
network
Explicit nodes and links, with stable IDs and explicit distances.
physical_profile
Only common alpha parameters, with units encoded in field 
names.



---

## Page 7


QNetBench Improved AI Handoff Manual  |  v0.2
Page 7
Section
Purpose
workload
Finite source-destination entanglement requests and request 
count.
protocol
Deterministic routing and fixed swapping policy; no purification in 
alpha.
requested_metrics
Metric IDs requested from the standard v0.1 registry.
extensions
Namespaced escape hatch; empty in all frozen alpha benchmarks.
6.1.1 Minimal alpha field set
- network contains explicit node IDs and undirected quantum links with link IDs, endpoints, and length_km. Alpha 
classical connectivity mirrors the quantum-link graph.
- physical_profile is limited to memory_count_per_node, memory_coherence_time_s, memory_frequency_hz, 
memory_efficiency, detector_efficiency, fiber_attenuation_db_per_km, quantum_propagation_speed_km_per_s, 
classical_propagation_speed_km_per_s, link_fidelity, swap_success_probability, and swap_fidelity_factor.
- workload is limited to one source, one destination, request_count, batch_start_s, and deadline_s. Each logical 
request asks for one entangled pair.
- protocol is limited to routing=shortest_path, shortest_path_tiebreak=lexical, swapping=sequential when needed, 
and purification=none.
- requested_metrics is limited to the standard v0.1 metric IDs in Section 9.
6.2 Strictness and units
- Unknown fields are rejected. Missing required fields are rejected with field-path errors.
- Unit-bearing values use explicit suffixes such as _s, _km, _hz, and _db_per_km. Hidden unit conventions are 
prohibited.
- NaN, positive infinity, and negative infinity are invalid.
- Node, link, request, and benchmark IDs must be deterministic and unique within their scope.
- Lists whose order has scientific meaning preserve order. Mapping key order has no meaning.
- The alpha benchmark catalog must not use extensions. An extension makes a run backend-specialized and 
ineligible for a cross-backend equivalence statement.
6.3 Prohibited benchmark fields
- backend name or backend version
- seed
- output directory
- sweep axes or seed lists
- wall-clock timeout or CI behavior
- simulator class names, object paths, or raw simulator settings outside an explicitly approved extension namespace
6.4 Normalization and hashing
- Load with safe YAML or JSON parsing into strict typed models.
- Normalize model values, including equivalent numeric representations accepted by the schema.
- Serialize to UTF-8 canonical JSON with sorted mapping keys, compact separators, and non-finite floats forbidden.
- Compute benchmark_hash as lowercase SHA-256 hex over the canonical JSON bytes.
- Comments, whitespace, YAML key order, and source filename do not affect benchmark_hash.
- Changing any scientific value, ordered list, benchmark_id, or schema_version changes benchmark_hash.
- A checked-in golden hash fixture protects the algorithm from accidental drift.
Contract freeze rule
After Checkpoint 1, a breaking BenchmarkSpec or result-contract change requires an approved ADR, human approval, 
updated fixtures, and either a new schema version or an explicit pre-release migration. Codex must not make such a 
change as incidental refactoring.



---

## Page 8


QNetBench Improved AI Handoff Manual  |  v0.2
Page 8
7. Execution request and sweep contract
7.1 RunRequest
A RunRequest is orchestration data, not part of the benchmark file. It contains the benchmark path or resolved 
benchmark object, backend name, integer seed, output directory, and explicit overwrite policy. The runner records the 
resolved request in the run manifest.
- No default seed is implied for a scientific run; the CLI requires one.
- The output directory must not exist unless the user explicitly requests overwrite. Silent merging and implicit 
resume are out of scope.
- The runner computes execution_hash from the normalized benchmark, backend identity, seed, and adapter 
execution options. Timestamps and output path are excluded.
- A run_id combines the benchmark ID, backend, seed, and a short execution-hash suffix. It is human-readable but 
not itself the source of truth.
7.2 SweepSpec
SweepSpec is a separate versioned YAML/JSON document. It references one base benchmark, lists finite parameter 
paths and values, lists seeds, and declares an output root. It expands deterministically into cartesian-product 
RunRequests.
- Only scalar replacement at contract-approved field paths is supported in alpha.
- The expansion order is deterministic: parameter paths sorted lexically, values in source order, then seeds in source 
order.
- The total expanded run count must be computed before execution and must not exceed 100 in alpha.
- Parallel execution, adaptive sweeps, conditional axes, random search, resume, distributed workers, and retry 
policies are deferred.
- The one checked-in alpha sweep must contain no more than nine runs so smoke execution remains finite.
8. Canonical result and artifact contract v0.1
The canonical result bundle is the boundary that makes QNetBench reusable. Adapters emit canonical records; all 
metrics and analysis operate above that boundary. A complete run directory has the following layout.
<run_dir>/
  benchmark.yaml          normalized benchmark actually executed
  run_manifest.json       identity, provenance, timing, hashes, status
  requests.jsonl          one terminal canonical record per request
  metrics.csv             standard metric rows derived from canonical records
  summary.json            derived convenience summary; never a metric source
  events.jsonl            optional canonical trace; not used by v0.1 metrics
  raw/                    optional backend-specific output; never a metric source
  error.json              present only for failed runs
8.1 Run manifest requirements
- result_schema_version, run_id, benchmark_id, benchmark_hash, and execution_hash
- qnetbench version, adapter name/version, backend package name/version or verified source revision
- seed and backend name
- run status: complete or failed in alpha; partial scientific results are not accepted
- UTC start/end timestamps for provenance, plus simulation measurement_start_s and measurement_end_s for 
metrics
- expected request count and written request count
- Python version and platform summary
- warnings and support-report digest
8.2 Canonical request record
requests.jsonl is required for every complete run. Each line is one terminal outcome for exactly one workload request. 
The required conceptual fields are:



---

## Page 9


QNetBench Improved AI Handoff Manual  |  v0.2
Page 9
Field
Rule
request_id
Unique and stable within the run.
source / destination
Must refer to benchmark node IDs.
submitted_at_s
Finite and non-negative.
terminal_at_s
Finite, not earlier than submitted_at_s.
status
success, failed, timed_out, or rejected.
latency_s
terminal_at_s - submitted_at_s within tolerance.
fidelity
0 to 1 for successful requests when exposed; otherwise null.
attempts
Non-negative integer when exposed; otherwise null.
path
Ordered node IDs when exposed; otherwise null.
failure_reason
Required for non-success when a reason is known.
metadata
Small canonical, backend-independent annotations only.
8.3 Bundle invariants
- A complete run contains exactly one request record for every planned request; duplicate or missing request IDs 
invalidate the bundle.
- Successful records have a valid terminal time and latency. Fidelity may be unavailable, but an unavailable value 
must be null, never guessed.
- No record contains NaN or infinity.
- The saved benchmark re-hashes to benchmark_hash.
- The request count in the manifest matches the JSONL record count.
- metrics.csv and summary.json can be regenerated from run_manifest.json and requests.jsonl.
- events.jsonl and raw/ may be absent. Their absence cannot make a standard metric unavailable if the required 
request fields exist.
8.4 Metric rows and availability
metrics.csv has the stable columns metric_id, status, value, unit, population_count, and coverage_count. status is ok, 
unavailable, or not_applicable. value is blank for non-ok rows. NaN and infinity are forbidden.
8.5 Writing and failure behavior
- Write to a temporary sibling directory, validate the complete bundle, then rename atomically when the platform 
permits.
- Do not leave a directory that looks complete after a failed write.
- A failed run writes a failed run_manifest.json and error.json with exception type, message, stage, and sanitized 
traceback. It does not produce standard metrics.
- Never overwrite an existing run directory without an explicit CLI flag.
- Raw simulator output is optional, size-bounded by the adapter, and excluded from bundle validation beyond path 
safety.
9. Standard metric definitions v0.1
The v0.1 metric registry is deliberately small. Every metric is a pure calculation over the canonical run manifest and 
canonical request records. Metric IDs and units are stable within the 0.1 release line.
Metric ID
Definition
Unit
Population
request_success_probability
success_count / 
planned_request_count
1
All planned requests.
latency_mean_s
Arithmetic mean latency_s
s
Successful requests only.
latency_median_s
Median latency_s
s
Successful requests only.
latency_p95_s
Nearest-rank 95th percentile
s
Successful requests only.



---

## Page 10


QNetBench Improved AI Handoff Manual  |  v0.2
Page 10
Metric ID
Definition
Unit
Population
fidelity_mean
Arithmetic mean fidelity
1
All successful requests; complete 
fidelity coverage required.
fidelity_median
Median fidelity
1
All successful requests; complete 
fidelity coverage required.
throughput_success_per_s
success_count / measurement 
duration
success/s
All successes in the manifest 
window.
attempts_per_success
sum known attempts / 
success_count
attempt/success
Requires complete attempt 
coverage.
9.1 Exact edge-case rules
- planned_request_count is the benchmark workload count, not the number of records an adapter happened to 
emit.
- If no request succeeds, latency and fidelity metrics are unavailable. They are not zero.
- Nearest-rank p95 uses sorted successful latencies and index ceil(0.95 * n) - 1.
- Fidelity coverage_count is the number of successful records with non-null fidelity; population_count is the number 
of successful records. Partial fidelity coverage makes the metric unavailable rather than selectively averaging a 
subset.
- Throughput requires measurement_end_s greater than measurement_start_s. Otherwise it is unavailable.
- attempts_per_success is ok only when attempts are present for every planned request record and success_count is 
greater than zero.
- Metrics never inspect summary.json, events.jsonl, raw/, adapter metadata, or simulator objects.
9.2 Sweep aggregates
For each parameter combination and metric ID, the alpha aggregate table reports n_runs, n_ok, mean, sample standard 
deviation when n_ok is at least two, minimum, and maximum. Confidence intervals, hypothesis tests, and interpolation 
are post-alpha work.
10. Backend adapter contract
10.1 Required responsibilities
- Declare a stable adapter name and adapter version.
- Inspect a validated BenchmarkSpec and return a structured SupportReport before execution.
- Translate the supported common specification into backend objects without modifying the benchmark model.
- Run with the explicit seed and return canonical request records plus canonical provenance and measurement-
window data.
- Map backend failures to typed QNetBench errors without hiding original diagnostic context.
- Document supported and unsupported benchmark fields and cases.
10.2 SupportReport
SupportReport contains supported, reasons, unsupported_paths, warnings, and backend_identity. A false report is 
normal behavior, not an internal crash. The CLI must show the field paths and reasons before any simulation starts.
10.3 Adapter prohibitions
- Do not compute standard metrics.
- Do not write the final artifact bundle directly.
- Do not import plotting, sweep, or CLI modules.
- Do not silently drop unsupported physical fields or protocol options.
- Do not fall back to the mock adapter under a real backend name.
- Do not place simulator package imports outside the adapter module and approved research tools.
11. Mock backend contract and mock-pipeline gate
The mock backend is a deterministic synthetic oracle for contracts, orchestration, tests, and examples. It is not a 
physical model and must say so in its metadata and documentation.



---

## Page 11


QNetBench Improved AI Handoff Manual  |  v0.2
Page 11
11.1 Mock requirements
- Support all four frozen alpha benchmark files and only the v0.1 feature subset.
- Produce identical canonical records for the same normalized benchmark, seed, and mock algorithm version.
- Produce a reproducible difference for at least one tested alternate seed.
- Never use wall-clock time, global random state, process ID, file order, or output path as randomness inputs.
- Expose a mock algorithm version so golden fixtures can change intentionally.
- Run the full default test suite and all four catalog cases quickly enough for default CI.
11.2 Mock-pipeline gate before SeQUeNCe
- All four catalog benchmarks validate and complete through the CLI with --backend mock.
- Every produced bundle passes result validation and re-computed metrics match metrics.csv.
- The checked-in small sweep completes, aggregates deterministically, and produces the approved plots.
- Default lint and test commands pass from a clean editable install.
- README quickstart, benchmark contract, result contract, metrics, adapter guide, and reproducibility 
documentation are current.
- PROJECT_STATE.md explicitly records mock_pipeline_ready: true and names the evidence commands.
Hard gate
No production qnetbench/adapters/sequence.py may be created or edited before the Checkpoint 8 report proves the 
mock-pipeline gate. Research notes may begin only at Checkpoint 9.
12. Frozen alpha benchmark catalog
The alpha catalog contains four static benchmark files. Their exact parameter values are frozen at Checkpoint 7. 
Changing a scientific value after freeze requires a new benchmark ID or an explicit pre-release migration approved by 
the human owner.
Benchmark ID
Case
Mock
SeQUeNCe alpha
qnb-v0.1-link-2-batch
Two nodes, one link, finite 
batch requests
Required
Required
qnb-v0.1-chain-3-batch
Three-node path, sequential 
swap
Required
Required
qnb-v0.1-chain-5-batch
Five-node path, sequential 
swaps
Required
Not supported
qnb-v0.1-grid-3x3-batch
Nine-node grid, corner-to-
corner shortest path
Required
Not supported
12.1 Shared alpha choices
- Workload type: finite batch of source-destination entanglement requests.
- Routing: deterministic shortest path with a documented lexical tie-break.
- Swapping: fixed sequential policy when intermediate repeaters exist.
- Purification: none.
- Extensions: empty.
- Benchmark files are explicit and static; no topology/workload generator API is part of alpha.
13. Testing, validation, and quality gates
13.1 Required test layers
- Contract tests: normative examples validate against checked-in schemas.
- Specification tests: strict validation, YAML/JSON equivalence, stable normalization, and golden hash.
- Result tests: record invariants, bundle round trip, atomic write behavior, failed-run behavior, and malformed 
JSONL rejection.
- Mock tests: deterministic outputs, support reports, request count, seed behavior, and golden fixtures.
- Metric tests: small synthetic request sets with hand-calculated expected values and edge cases.



---

## Page 12


QNetBench Improved AI Handoff Manual  |  v0.2
Page 12
- CLI integration tests: validate, run, summarize, validate-result, list, sweep, and plot.
- Architecture tests: forbidden imports and simulator-package isolation.
- SeQUeNCe integration tests: optional marker, only after the research checkpoint, with explicit skip reasons when 
the dependency is absent.
- Release smoke tests: build wheel/sdist, install the wheel in a clean environment, and run a mock benchmark.
13.2 CI policy
- Default CI uses Python 3.12, installs the development extra, runs Ruff and pytest, and does not require 
SeQUeNCe.
- Default CI should complete in about one minute on an ordinary hosted runner; long real simulations do not belong 
there.
- An optional or manually triggered SeQUeNCe job may be added after Checkpoint 10.
- No failing test is skipped, deleted, or weakened merely to advance a checkpoint.
- There is no alpha coverage-percentage target. Critical contracts and edge cases matter more than a gameable line 
number.
14. Checkpoint and handoff discipline
14.1 One checkpoint at a time
- Codex implements only the active checkpoint named in PROJECT_STATE.md or the current human prompt.
- It may inspect future files for context but may not create future-checkpoint implementation.
- Every checkpoint has an explicit file list, required tests, commands, definition of done, and must-not-do-yet list.
- At completion, Codex updates PROJECT_STATE.md, writes the checkpoint report, commits if authorized, reports, 
and stops.
- A human or controlling agent starts the next checkpoint with a new prompt.
14.2 Blocker behavior
- Create a blocker report when a required command fails after reasonable diagnosis, an external dependency cannot 
be installed, an authoritative instruction conflicts, or completing the task would require changing a frozen 
assumption.
- Include exact commands, full relevant error text, minimal reproduction, attempted fixes, hypotheses, and the 
safest next step.
- Do not work around a blocker by fabricating success, substituting mock output, changing the contract, or 
continuing to the next checkpoint.
14.3 PROJECT_STATE.md
PROJECT_STATE.md is a compact current-state record, not a diary. It must identify the active checkpoint, last good 
commit, last passing commands, contract versions, completed capabilities, open blockers, immutable assumptions, and 
the next allowed action.
15. SeQUeNCe research and adapter boundary
SeQUeNCe is the only real backend in the alpha. Because its API and install process can change, no production 
adapter API call may be inferred from memory or from this planning document.
15.1 Research checkpoint requirements
- Identify and record the exact upstream repository, version tag or commit, license, supported Python version, and 
verified installation command.
- Run an upstream minimal example in an isolated environment before touching production adapter code.
- Document exact symbols and examples for timeline/simulation control, nodes, quantum and classical channels, 
memory configuration, request submission, entanglement completion, fidelity extraction, timing extraction, 
attempts if available, and random seed control.
- Create a field-by-field mapping from the common v0.1 specification to SeQUeNCe and mark unsupported paths.
- Write an ADR defining the supported subset and extraction strategy.
- If any required value for the two alpha cases cannot be obtained honestly, stop with a blocker rather than 
redesigning the common contract silently.



---

## Page 13


QNetBench Improved AI Handoff Manual  |  v0.2
Page 13
15.2 Adapter alpha boundary
- Required: qnb-v0.1-link-2-batch and qnb-v0.1-chain-3-batch.
- Explicitly unsupported: qnb-v0.1-chain-5-batch and qnb-v0.1-grid-3x3-batch, even if partial experimentation 
suggests they might run.
- No purification, random routing, dynamic arrivals, or backend extensions.
- Real outputs are normalized into the same request records used by the mock adapter.
- Validation checks physical sanity and artifact correctness, not equality to mock values.
16. Definition of QNetBench 0.1.0a1
Checkpoint 11 may declare the alpha complete only when every item below is true.
- Package version is 0.1.0a1 and a wheel and source distribution build successfully.
- The wheel installs in a clean Python 3.12 environment and the qnetbench CLI reports its version.
- All default lint and tests pass with no unexplained warnings or hidden skips.
- BenchmarkSpec v0.1, Canonical Result Contract v0.1, metric definitions, and golden hashes are frozen and 
documented.
- All four frozen benchmarks complete with the mock adapter and produce valid bundles.
- The checked-in small sweep completes and its aggregate CSV and plots are reproducible.
- The two required SeQUeNCe cases complete in the verified integration environment and produce valid bundles; 
unsupported cases reject before execution.
- Architecture-boundary tests pass: metrics do not import adapters; simulator imports are isolated.
- README, contracts, metrics, adapter guide, reproducibility guide, support matrix, and release checklist match 
actual behavior.
- LICENSE, CITATION.cff, and CHANGELOG.md are present and internally consistent.
- PROJECT_STATE.md has no open release-blocking issue and links to the Checkpoint 11 report.
Publication boundary
Checkpoint 11 prepares a release candidate. Codex must not push, create a Git tag, publish to a package index, create a 
GitHub release, or mint a DOI without a separate human authorization.
17. Change control and post-v0.1 work
17.1 Changes that require explicit approval
- Changing benchmark or result schema fields after Checkpoint 1.
- Changing the hash algorithm or a frozen benchmark value after its golden fixture is accepted.
- Adding runtime dependencies not named in the plan.
- Adding another backend, a new protocol family, a new metric population, or generalized resource metrics.
- Increasing the sweep cap, adding parallelism/resume, or expanding SeQUeNCe support beyond the two cases.
- Changing the target release, Python baseline, license, package name, or checkpoint count.
17.2 Post-v0.1 ideas - not part of the execution plan
- Additional adapters such as QuNetSim, QuISP, or NetSquid/SquidASM after separate research and licensing 
review.
- Purification, random/adaptive routing, dynamic workloads, application-layer benchmarks, and richer physical 
profiles.
- Memory occupancy, queueing, energy, and detailed resource-utilization metrics with a stronger common contract.
- Parallel/distributed sweeps, resumable execution, result databases, dashboards, and web interfaces.
- Cross-simulator validation studies, paper figures, software-paper submission, and DOI publication.
18. Final handoff checklist
1.  Read AGENTS.md and PROJECT_STATE.md before changing files.
2.  Confirm the active checkpoint and its exact stop boundary.
3.  Read the relevant v0.1 contract documents and ADRs.
4.  Inspect git status and preserve unrelated human changes.



---

## Page 14


QNetBench Improved AI Handoff Manual  |  v0.2
Page 14
5.  Implement only the named files and behavior for the checkpoint.
6.  Add the required tests before claiming completion.
7.  Run every required command and record exit status and evidence.
8.  Update PROJECT_STATE.md and write the checkpoint or blocker report.
9.  Commit only if authorized and report the commit SHA.
10.  Stop. Do not begin the next checkpoint in the same turn.
Final instruction to future AI
Make the smallest contract-correct increment. Prove it with tests and artifacts. Record the state. Stop at the checkpoint 
boundary.
