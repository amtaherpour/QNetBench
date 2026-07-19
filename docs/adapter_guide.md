# Adapter guide

Implement the `Adapter` interface, return a structured `SupportReport`, and emit
canonical `RequestResult` records in memory. An adapter must reject unsupported
features before execution and must not calculate metrics or write final result
bundles. Register the factory by a stable lowercase name and add deterministic,
support, failure, and architecture-boundary tests.

Real simulator integrations require a separate verified research checkpoint. Do
not infer simulator APIs or scientific mappings from the mock adapter. The mock
is synthetic and is not evidence that a corresponding real backend is supported.
