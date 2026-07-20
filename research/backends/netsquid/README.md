# NetSquid optional BYO integration boundary

NetSquid is not a dependency of QNetBench core and is not installed by public
default CI. Access requires user registration, acceptance of applicable terms,
and user-specific credentials for the private package index.

A future optional distribution named `qnetbench-netsquid` must:

1. declare its own NetSquid-compatible Python and package versions;
2. receive credentials only through an authorized private secret store;
3. explicitly register its adapter after import;
4. pass the common conformance cases and canonical bundle tests;
5. keep all NetSquid imports outside QNetBench core; and
6. label generated paper artifacts as an optional credentialed reproduction lane.

The template `private_ci_template.yml.example` is intentionally inactive. It does
not contain credentials and must not be copied into an active workflow until the
user has independently obtained access and authorized that private lane.
