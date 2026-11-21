---
title: "Desk check: google-deepmind/code-verification 8c8d371"
source: https://github.com/google-deepmind/code-verification/tree/8c8d371f1962ac73435c8eb148678991f5c3470d
type: repos
authors: ["Swarat Chaudhuri", "Andrew Ferraiuolo", "Anton Kovsharov", "Tej Chajed", "Sam Schlesinger", "Karn Seth", "Jonathan Katz", "Charles Sutton", "Pushmeet Kohli"]
source_date: 2026-11-19
ingested: 2026-11-21
repo: google-deepmind/code-verification
kind: library
version: "8c8d371"
licence: "Apache-2.0 code, third-party files AGPL-3.0-only or MIT"
tags: [catalog, desk-check, kind-library, lean, formal-verification, machine-code, aarch64, ai-generated-proofs, trusted-base]
summary: "google-deepmind/code-verification read at commit 8c8d371 (default branch, no releases) from a read-only clone: a Lean project of AI-generated proofs about the compiled AArch64 machine code of libsignal under a symbolic and a computational model, the shared binary proofs, the arm64-semantics verification engine, the comparator check, the trusted-base and axiom audit, the scripts and the reviewers' site; the licence as the files state it; the toolchains, memory, hours and downloads a full check needs. Every part is a reference, except the engine, which is a candidate."
---

# Desk check: google-deepmind/code-verification 8c8d371

Read from a shallow clone of the default branch `main` at commit `8c8d371f1962ac73435c8eb148678991f5c3470d` (committed 2026-11-19T23:57:30Z, message "Export from internal repository (#5)"), at `$EXTERNAL/code-verification`. The repository has no releases and no tags, so the version is the short commit sha `8c8d371`. The clone was not modified; nothing was installed, built or run. Checked 2026-11-21. Version read by this desk check: 8c8d371.

## Repository facts

- GitHub description: "Verifying Signal's security at the machine-code level". Homepage: the reviewers' site, https://google-deepmind.github.io/code-verification/.
- README: "We present two AI-generated proofs of security for compiled AArch64 machine code of `libsignal` (the official Rust implementation of the Signal protocol) in a CLI harness". The two proofs give "independent arguments for security, one under the symbolic model and one under the computational model."
- The paper on the reviewers' site, "AlphaProof Code: Verifying Signal's Security at the Machine-Code Level" (dated 2026-11-10; authors from Google DeepMind and Google), describes AlphaProof Code as "a multi-agent AI framework for formal software specification and verification": a human-guided agent writes Lean specifications, a formal semantics of AArch64 machine code gives the code its meaning, and autonomous prover agents write proofs that are "accepted only if Lean's kernel checks them against the approved specification." Abstract: "our agents generated about 6.3 million lines of machine-checked Lean proof code, resting on about 27,000 lines of trusted specifications and AArch64 semantics." The proofs cover the PQXDH handshake and the Triple Ratchet (forward secrecy, authentication, post-compromise security, handshake secrecy).
- What is verified: `libsignal` tag `v0.105.4` plus `spqr` v1.6.0 (README tree), compiled to one SHA-256-pinned AArch64 ELF of a CLI harness, including linked cryptographic primitives, formatting and I/O.
- The README's own caveats, retold: 18 Rust panic entry points are mapped to `SIGABRT`; the binary correctness theorem excuses out-of-memory; runs where one rejection-sampling loop in the ML-KEM code never ends are excused from termination and add an unbounded probability term to the computational bound; the computational main theorem rests on named idealization hypotheses (a noise idealization for Kyber-1024, a random-oracle gap for HKDF). Every deviation from the papers it follows has an ID in `Computational/docs/DEVIATIONS.md` (3736 lines).
- Kind: `library`. The repository is a Lake package of Lean libraries (`lakefile.lean` declares `lean_lib` targets such as `LibsignalBinary`, `Symbolic`, `Computational`, `CliElfLib`, `ComparatorChallenge`, `ComparatorSolution`) plus build and audit scripts; `arm64-semantics` can be used on its own "in a downstream repository that consumes it as a submodule/Lake dependency". No one would import the libsignal proofs into other work, so those parts are kept as references: a worked example of how AI-written proofs about compiled code are checked and trusted.
- Size, counted with `find` and `wc` in the clone: `Symbolic/` 1,598 `.lean` files (595,180 lines), `Computational/` 1,389 (1,347,827 lines), `LibsignalBinary/` 7,703 (4,397,707 lines), `arm64-semantics/` 790 (473,796 lines).
- Top-level folders: `Computational/`, `Symbolic/`, `LibsignalBinary/`, `arm64-semantics/`, `comparator/`, `scripts/`, `third_party/`, `docs/`.
- `CONTRIBUTING.md`: contributions need the Google Contributor License Agreement; all submissions are reviewed through GitHub pull requests.

### Licence, as the files state it

- GitHub reports the licence as `NOASSERTION` ("Other").
- `LICENSE` (9 lines) holds only third-party terms: files under `third_party/hashbrown-0.17.1` are MIT; `arm64-semantics/CaseStudies/Hashbrown/Implementation/hashbrown_cli.elf` contains compiled code from hashbrown 0.17.1, the Rust standard library 1.98.1 and musl 1.2.5, under MIT; "The files located at third_party/libsignal that contain code copied from libsignal are licensed under the following terms: https://opensource.org/license/agpl-v3"; three assembly files under `third_party/libsignal/libsignal-session/cli-elf/` contain Rust standard library code (MIT); files under `.../cli-elf/string-include` contain musl 1.2.5 code (MIT). The file does not contain the Apache License text.
- README, first "License" section: "All code is licensed under the Apache License, Version 2.0". README, "License and disclaimer": "Unless a file states otherwise, the software in this repository is licensed under the license described in [`LICENSE`](LICENSE). Third-party material, including code copied from Signal's `libsignal` (AGPL-3.0-only), keeps its own license." and "This is not an official Google product."
- Source file headers read (`lakefile.lean`, `scripts/cli-elf`, `scripts/cli-elf-stock`, `scripts/trusted-closure.sh`, `comparator/install-tools.sh`) repeat "All code is licensed under the Apache License, Version 2.0".
- `arm64-semantics/LICENSE` is the full Apache License, Version 2.0 text. `third_party/libsignal/LICENSE` is the upstream AGPL text; `third_party/libsignal/README.md`: "`AGPL-3.0-only`; full text in [`LICENSE`](LICENSE), copied from the upstream `LICENSE` at that commit".
- Code versus other material: the README speaks of "code" and "software" only. No statement was found for non-code material (the Markdown documents, the paper, the reviewers' site); a search for "Creative Commons" and "CC-BY" found nothing. So: code Apache-2.0 by the README and file headers; third-party files AGPL-3.0-only or MIT as listed; documents and site not stated.

## Freshness (checked 2026-11-21 through `gh api`)

- `gh api repos/google-deepmind/code-verification`: `pushed_at` 2026-11-20T00:08:57Z; licence `NOASSERTION`; default branch `main`; not archived; created 2026-10-26T16:27:08Z.
- `gh api .../releases/latest`: 404, no releases. `gh api .../tags`: no tags.
- `gh api .../commits/main`: `8c8d371f1962ac73435c8eb148678991f5c3470d`, 2026-11-19T23:57:30Z, the commit read. The push of 2026-11-20 is the `gh-pages` branch: commit `c633c62`, 2026-11-20T00:08:47Z, "Reviewers' site (v7) for code-verification 8c8d371f1962".
- Branches: `main`, `gh-pages`, and two `copybara/export-*` branches (exports from an internal repository).

## How to run here

- **Clone**: `git clone --depth 1 https://github.com/google-deepmind/code-verification $EXTERNAL/code-verification`, read-only; check that `git -C $EXTERNAL/code-verification log -1 --format=%h` prints `8c8d371`.
- **Read first**: `README.md`, then `Computational/docs/TRUSTED_BASE.md` (what a reviewer reads and what Lean checks), `docs/PAPER_MAP.md`, `Symbolic/README.md`. The reviewers' site shows the same statements tiered for reading, without building anything.
- **Telemetry**: none; reading the files sends nothing. Nothing needs switching off for reading.
- **What a build would download** (not run here):
  - `lake exe cache get` fetches prebuilt Mathlib (README step 1).
  - Lake packages from GitHub, pinned in `lake-manifest.json`: mathlib (`v4.35.0`), VCVio, dylean, PolyFun, cslib, batteries, aesop, ProofWidgets4, plausible, LeanSearchClient, import-graph, quote4, lean4-cli.
  - The build clones `https://github.com/signalapp/libsignal` at tag `v0.105.4` into a `sw/libsignal` folder in the home directory unless `LIBSIGNAL_SRC` points to a checkout; `LIBSIGNAL_NO_CLONE` turns cloning off (`third_party/libsignal/libsignal-session/translation.toml`, `rust-obj2lean`). Cargo builds run with `--locked`.
  - `comparator/install-tools.sh` fetches and builds `leanprover/comparator`, `leanprover/lean4export` and `Zouuup/landrun` from GitHub and downloads a Go toolchain from go.dev.
- **Needs for a full check** (README "Prerequisites" and "Build and Kernel-Check All Proofs"):
  - Lean 4 through `elan`; `lean-toolchain` pins `leanprover/lean4:v4.35.0`.
  - Rust `1.98.1`, pinned in `rust-toolchain.toml`, with the `aarch64-unknown-linux-gnu` and `aarch64-unknown-linux-musl` targets, `rust-src` and `llvm-tools-preview`; "do not override the pin", because the generated Lean depends on the exact `rustc` output.
  - `protoc`, LLVM `ld.lld` `22.1.8` and Zig `0.16.0` on `PATH`.
  - Time and memory: `lake build` checks all default proofs in "several hours, ~15–34 GiB peak RAM", with `LEAN_NUM_THREADS` at "about 1 thread per 4 GiB of free RAM". The binary-level theorems need a second step: build and pin-check the ELF (`scripts/cli-elf-stock`), then `lake build CliElfLib`.
  - Comparator: "only supported on Linux", because `landrun` uses the Linux Landlock LSM.
- **Do not install** the Lean, Rust, Zig or LLVM toolchains for this desk check, and do not run `lake build`: the hours and memory above are the cost. A real build waits for the user's yes.

## Parts

### `Symbolic` (Lean library, `Symbolic/`)

- The Dolev-Yao (DyLean) symbolic development for `libsignal v0.105.4`: symbolic models of PQXDH and the Triple Ratchet, "ten protocol security properties (secrecy, authentication, forward secrecy, post-compromise security, KCI resistance, session independence, and HNDL resistance)", trace refinement from the SHA-256-pinned AArch64 binary, security preservation across refinement, and the bug-injection suite.
- Layout: `Specifications/` (trusted: models, concrete byte-level mirrors, refinement statement, security statements), `Theorems/` (audited headline statements), `Tests/` (non-vacuity and guard modules), `Proofs/` (untrusted), `DYBridge/`, `BugInjection/`, `scripts/` (dependency and machine-freeness checks).
- Headline theorems: forward secrecy, post-compromise security and 8 handshake properties in `Theorems/ModelSecurity.lean` and refinement preservation (default `lake build`); `comp_refines_cli` and `signal_session_secure` with their real-primitive variants (`lake build CliElfLib`).
- Needs: the full build above. Status `reference`.

### `Symbolic/BugInjection`

- "Each bug in this directory is a Rust patch against `libsignal`: either a reversed upstream fix commit ... or a forward regression patch against `v0.105.4`." For each, a witness proves that the patched binary breaks a security predicate, showing that the specification catches the bug. The README notes that retargeting the suite from the retired placed predicate to the current ELF-direct headline "is pending".
- Needs: the full build. Status `reference`.

### `Computational` (Lean library, `Computational/`)

- The game-based security proof of the one-to-one session, following ACD19 (Alwen, Coretti, Dodis, the Double Ratchet security paper) and, for PQXDH, FG24, BJKS24 and Signal's PQXDH specification. `Theorems/Lemmas.lean`: Lemmas 1 to 3 and a Kyber-1024 decapsulation-failure bound; `Theorems/Main.lean`: Lemma 4 (the binary refines the model) and the Main Theorem, in library `CliElfLib`. `Specifications/` holds games, assumptions, reductions; `Proofs/` is checked by Lean and "not part of the trusted base"; `Tests/` holds non-vacuity, sanity and known-answer tests.
- Docs: `READING_THE_THEOREMS.md`, `TRUSTED_BASE.md`, `DEVIATIONS.md`, `GLOSSARY.md`, `REDUCTION_DSL_TUTORIAL.md`, `PQXDH.md`.
- Needs: the full build. Status `reference`.

### Trusted base and deviations (`Computational/docs/TRUSTED_BASE.md`, `DEVIATIONS.md`)

- `TRUSTED_BASE.md` (1073 lines): "To trust a theorem, you read its **statement** and the **definitions** the statement uses, and you trust the shared foundations and tools. You never need to read a proof." Three tiers: Tier 1, the statement files, read in full; Tier 2, definitions from this repository that the statements use, read as definitions only; Tier 3, shared foundations (the `arm64-semantics` machine model, Lean core, Mathlib, VCVio) and the three standard axioms, not read.
- Numbers for the model-run theorem `libsignalCliPqSecure_holds`: Tier 1, 19 statement files, 3,431 code lines; Tier 2, 74 files, 9,510 code lines; everything else, "1,561 repository files" and 1,383,725 lines, "No: Lean checks them". Numbers "computed from the compiled `.olean` artifacts" with `scripts/trusted-closure.sh`, on `arm64-semantics` `v0.56.1`, commit `b62b68b0`.
- Section 4, "What Lean does not check, so you check it by reading": for example, that the reduction programs' cost bounds assign honest costs, which needs reading the `ReductionDsl` specification.
- `DEVIATIONS.md`: every place where the Lean differs from the papers, one entry per ID.
- Needs: nothing to read. Status `reference`.

### `LibsignalBinary` (Lean library, `LibsignalBinary/`)

- Specifications and proofs about the compiled AArch64 session code that both the symbolic and the computational proofs use: hook models, layouts and session programs, the `SignalMessage` wire format, per-function contracts of the binary with machine-code proofs (Triple Ratchet entry points, AES-CBC, HMAC, linked crates), the Rust heap vocabulary and a `musl` allocator instance, the SPQR V1 model.
- Needs: the full build. Status `reference`.

### `arm64-semantics` (Lean engine, `arm64-semantics/`)

- "This is a system for specifying and verifying Rust and C at the arm64 assembly level." "you bring code and a specification ..., an agent comes up with a proof, and you can have confidence that the compiled assembly of your code actually meets your specification." Trusted code (`Arm64/Trusted/`: instruction decoding and semantics, ELF loading, Linux syscalls, the specification forms) is kept apart from untrusted proof tooling (`ProofLib/`: proof rules, tactics, a symbolic block executor) so that only the trusted part needs review. Also `VerifiedLibraries/` (musl, mallocng, Rust std foundations), `CaseStudies/Hashbrown`, and `tools/rust-obj2lean`, a Rust CLI that compiles Rust crates or C units to AArch64 objects and turns them into Lean.
- Limits stated: Linux ELF only, static linking only; single-threaded memory model; generic Rust code cannot be verified until instantiated.
- Needs: Lean through `elan` (`leanprover/lean4:v4.35.0`); Rust `1.98.1` with AArch64 targets for the generated modules ("The core libraries (`Arm64`, `ProofLib`) do not need Rust."); `ld.lld`. Hardware: "A full build ... takes about 35–40 minutes on 12 cores and peaks at about 25 GiB of memory." "Use at least 16 GB of RAM ..., 32 GB or more for 12-way parallelism, and about 6 GB of free disk." "Building only the core libraries (`lake build`) takes about 13–15 minutes and stays under 6 GB."
- Status `candidate`: it is the one part meant to be reused on other code.

### `comparator` (`comparator/`)

- Sets up `leanprover/comparator`, "the Lean FRO's proof judge", for every headline theorem. It checks that the proved theorem "has the exact statement of the challenge" with every referenced constant identical, that "its proof depends only on the standard Lean axioms `propext`, `Quot.sound`, and `Classical.choice`", and that the whole solution, exported by `lean4export`, "replays in a fresh Lean kernel". `ComparatorChallenge` holds trusted reference statements proved with `sorry` and importing only specification modules; `ComparatorSolution` re-exports the proved theorems; `computational.json` and `symbolic.json` list the theorems; `install-tools.sh` and `run.sh` run it.
- Needs: Linux (Landlock), the full build, the downloads above. Status `reference`.

### Scripts: axiom audit (`scripts/trusted-closure.sh`, `scripts/TrustedClosure.lean`)

- After a build, computes the transitive declaration closure of each headline theorem (`trusted_closure.csv`, `trusted_closure.md`, `trusted_banners.csv`), enforces that no proof-tree definition is unfolded in a headline's statement closure, and reports each headline's kernel axioms. Runs over the default lemmas, the 8 headlines in `scripts/trust_banner_headlines.txt`, or the 14 symbolic headlines.
- Needs: a finished build. Status `reference`.

### Scripts: pinned binary build (`scripts/cli-elf-stock`, `scripts/cli-elf`, `scripts/stock-pin/`, `scripts/stock_elf_prep/`)

- `cli-elf-stock`: "Reproducible stock-`ld.lld` CLI ELF builder & fail-closed verifier": builds the ELF from pinned lock inputs, enforces structural, symbol, relocation and environment invariants, and checks the SHA-256 pin; "Python checks here are defense-in-depth build/preflight guards only; they never replace in-Lean kernel checks". `cli-elf` is the legacy builder kept for bug-injection mutants. `scripts/lake-facets/` and `LakeInputFacet.lean` hook generated modules into Lake.
- Needs: the Rust toolchain, `ld.lld`, Zig. Status `reference`.

### `third_party/`

- The libsignal crates that wrap `libsignal` `v0.105.4` (commit `b2a5c30f3245c1bcad04b27b1e752a38321c793d`) for compilation, bug-injection patches, test vectors, and hashbrown 0.17.1. "No upstream checkout and no compiler output is committed in this repository"; they are regenerated by `lake build`.
- Needs: nothing to read. Status `reference`, read for what is copied from libsignal and under which licence.

### `docs/PAPER_MAP.md`

- Maps each section, figure, theorem and lemma of the paper to the Lean declarations, each with a status: "proved" (only the three standard axioms, enforced by `comparator/run.sh`), "conditional" (under a named hypothesis not discharged), or "open" (stated with `sorry`; "only the 17 non-default synthetic mutation stubs"). `docs/Symbolic/PAPER_DIFFERENCES.md` lists where the symbolic Lean differs from the paper.
- Needs: nothing. Status `reference`.

### Reviewers' site (`gh-pages` branch, https://google-deepmind.github.io/code-verification/)

- Not in the clone; read through `gh api` (tree) and the public page. Holds the paper and the statements in three folders, `Tier-1___-statements`, `Tier-2___-definitions` and `Tier-3___-trusted___-not-read`, with search and cross-references; built for commit `8c8d371f1962` ("Reviewers' site (v7)").
- Needs: a browser. Status `reference`.

## Reasons for reference status

- The libsignal proof libraries (`Symbolic`, `Computational`, `LibsignalBinary`), the bug-injection suite, the comparator setup, the scripts, `third_party/`, the paper map and the reviewers' site are specific to one verified binary. They are read for how a large AI-written proof about compiled code is made trustworthy (tiers of what a person reads, a fixed set of axioms, statements compared with an approved challenge, a pinned binary, re-injected historical bugs), not run. A full check also costs hours and tens of GiB of memory, and the comparator step runs only on Linux.
- `arm64-semantics` is the exception: it is built to be reused on other Rust or C code, so it stays a `candidate`.

## Cost of this desk check

Written in one agent run together with the other 1 desk check, the cards and the use records of the same batch: 81 model calls on opus, $5.80 at list prices (`claude_usage.py agents`). The cost of this desk check alone was not measured.
