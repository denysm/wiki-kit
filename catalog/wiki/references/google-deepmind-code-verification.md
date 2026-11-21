---
title: "google-deepmind/code-verification"
category: reference
kind: library
areas: [verifying-code]
repo: google-deepmind/code-verification
version: "8c8d371"
licence: "Apache-2.0 code, third-party files AGPL-3.0-only or MIT"
desk_checked: 2026-11-21
sources:
  - raw/repos/google-deepmind-code-verification-desk-check-2026-11-21.md
created: 2026-11-21
updated: 2026-11-21
tags: [catalog, card, area-verifying-code, kind-library, lean, formal-verification, machine-code, aarch64, ai-generated-proofs, trusted-base]
confidence: high
volatility: hot
verified: 2026-11-21
summary: "Lean project of AI-generated proofs that the compiled AArch64 machine code of libsignal meets security properties under a symbolic and a computational model, with a reusable arm64 verification engine, a comparator check, a tiered trusted-base audit and a reviewers' site. Read at commit 8c8d371 (no releases) from a clone, not built: a full check takes hours and up to 34 GiB of RAM. The proof libraries and audits are references for how AI-written proofs are trusted; the engine is a candidate."
---

# google-deepmind/code-verification

> A Lean project (kind `library`, licence Apache-2.0 for code by its README, third-party files AGPL-3.0-only or MIT; commit `8c8d371` read, no releases): "two AI-generated proofs of security for compiled AArch64 machine code of `libsignal`", one under the symbolic model and one under the computational model, with the `arm64-semantics` engine they rest on, a comparator check of the headline theorems and an audit of what a reviewer must read. Read from a clone, not built.

## Tasks it serves

| Task | Part | Area |
|------|------|------|
| Check how an AI-written proof about compiled code is trusted: what a person reads, what the kernel checks | Trusted base and deviations | verifying-code |
| Find a worked example of verifying machine code against a security property | `Symbolic`, `Computational` | verifying-code |
| Check that AI-written proofs prove exactly the approved statements, using only the standard axioms | `comparator` | verifying-code |
| List every definition and axiom a theorem rests on | Axiom audit scripts | verifying-code |
| Show that a specification catches real bugs by re-injecting historical fixes | `Symbolic/BugInjection` | verifying-code |
| Prove that a compiled Rust or C function meets a contract at the arm64 assembly level, with an agent writing the proof | `arm64-semantics` | verifying-code |
| Pin the exact binary a proof is about and rebuild it reproducibly | Pinned binary scripts | verifying-code |
| Read the statements of a large verification without building it | Reviewers' site, `docs/PAPER_MAP.md` | verifying-code |

## Run it here

- **Clone**: `git clone --depth 1 https://github.com/google-deepmind/code-verification $EXTERNAL/code-verification`, read-only; `git -C $EXTERNAL/code-verification log -1 --format=%h` should print `8c8d371`. Never edit the clone.
- **Version**: commit `8c8d371` of `main`, committed 2026-11-19; the repository has no releases and no tags. Compare before relying on this card: `gh api repos/google-deepmind/code-verification/commits/main --jq .sha`.
- **Read first**: `README.md`, then `Computational/docs/TRUSTED_BASE.md`, `docs/PAPER_MAP.md` and `Symbolic/README.md`; or the reviewers' site, which tiers the statements for reading.
- **Switch off**: nothing; reading sends nothing out. A build would download prebuilt Mathlib (`lake exe cache get`) and Lake packages from GitHub, clone libsignal `v0.105.4` into the home directory unless `LIBSIGNAL_SRC` points to a checkout (`LIBSIGNAL_NO_CLONE` turns cloning off), and the comparator installer fetches its tools and a Go toolchain.
- **Do not install**: the Lean (`leanprover/lean4:v4.35.0`), Rust `1.98.1`, Zig `0.16.0` or LLVM `ld.lld` `22.1.8` toolchains, and do not run `lake build`: "several hours, ~15–34 GiB peak RAM". Comparator runs "only supported on Linux". A real build waits for the user's yes.

## What's inside

| Part | What it does | Status | Needs | Check when |
|------|--------------|--------|-------|------------|
| `Symbolic` | Dolev-Yao models of PQXDH and the Triple Ratchet, ten protocol security properties, trace refinement from the pinned binary to the model, security preserved across refinement. | reference | The full build (Lean, Rust, hours, up to 34 GiB of RAM). | Consult when a protocol-level property has to be tied to compiled code. |
| `Symbolic/BugInjection` | Reversed upstream fixes and synthetic regressions applied to libsignal; a witness proves each patched binary breaks security. Retargeting to the current headline "is pending". | reference | The full build. | Consult when showing that a specification would have caught known bugs. |
| `Computational` | Game-based proof of the session following the Double Ratchet and PQXDH papers: three lemmas, a Kyber-1024 bound, Lemma 4 (the binary refines the model) and the Main Theorem, under named idealization hypotheses. | reference | The full build. | Consult when a computational security bound has to reach machine code. |
| Trusted base and deviations | `TRUSTED_BASE.md`: "You never need to read a proof"; three tiers (statements read in full, definitions they use, shared foundations not read) with exact counts; what Lean does not check. `DEVIATIONS.md`: every departure from the papers by ID. | reference | Nothing to read. | Consult when deciding what a reviewer must read before trusting an AI-written proof. |
| `LibsignalBinary` | Specifications and machine-code proofs of the binary shared by both proofs: session entry points, AES-CBC, HMAC, wire format, heap. | reference | The full build. | Consult for how per-function contracts of a binary are stated. |
| `arm64-semantics` | Engine "for specifying and verifying Rust and C at the arm64 assembly level": trusted instruction, ELF and syscall semantics kept apart from untrusted proof tooling; verified libc and allocator foundations; a hashbrown case study; `rust-obj2lean`, which turns compiled objects into Lean. Linux, static linking, single thread. | candidate | Lean `leanprover/lean4:v4.35.0`; Rust `1.98.1` for generated modules; core libraries alone "about 13–15 minutes and stays under 6 GB"; full build "about 35–40 minutes on 12 cores", "about 25 GiB of memory". | Try it on one small Rust or C function whose compiled code must meet a contract, on a machine with 32 GB of RAM. |
| `comparator` | Runs Lean's proof judge on every headline theorem: same statement as the trusted challenge, only `propext`, `Quot.sound` and `Classical.choice`, replay in a fresh kernel. | reference | Linux (Landlock), the full build, tools fetched from GitHub. | Consult when accepting proofs from an agent against statements a person approved. |
| Axiom audit scripts | `scripts/trusted-closure.sh` and `TrustedClosure.lean`: the transitive declarations and kernel axioms of each headline theorem. | reference | A finished build. | Consult when a trust report per theorem is needed. |
| Pinned binary scripts | `scripts/cli-elf-stock`: builds the ELF from pinned inputs with stock `ld.lld` and checks its SHA-256 pin; Python checks are only guards, never a replacement for kernel checks. | reference | Rust, `ld.lld`, Zig. | Consult when a proof must name the exact binary it covers. |
| `third_party/` | The libsignal crates at `v0.105.4`, bug patches, test vectors, hashbrown; no upstream checkout committed. | reference | Nothing to read. | Consult for what is copied from libsignal and under which licence. |
| `docs/PAPER_MAP.md` | Paper sections and theorems mapped to Lean names, each "proved", "conditional" or "open". | reference | Nothing. | Consult when checking a claim of the paper against the code. |
| Reviewers' site | The paper and the statements in three tiers, with search; on the `gh-pages` branch, not in the clone. | reference | A browser. | Consult first, before opening any Lean file. |

## Tried

None yet: nothing here has been built or run; every part was read from the clone or the public site.

## Verdict

A reference rather than a tool to run: the libsignal proofs, the comparator setup, the audits and the site show how a very large AI-written proof about compiled code is made trustworthy (a person reads only statements and their definitions, proofs are accepted only with the standard axioms against approved statements, the binary is pinned, historical bugs are re-injected). The `arm64-semantics` engine is the one part built for reuse and is a candidate for a small Rust or C function, on a machine with enough memory. Revisit when the repository gets a release or a new commit on `main`, when the bug-injection suite is retargeted, or when a task needs a machine-checked contract for compiled code.

## See Also

- [[area-verifying-code|Verifying code]] ([Verifying code](../topics/area-verifying-code.md)): area page; machine-checked proofs about code and how AI-written proofs are trusted

## Sources

- [Desk check: google-deepmind/code-verification 8c8d371](../../raw/repos/google-deepmind-code-verification-desk-check-2026-11-21.md): every part read from the clone, the licence as the files state it, what a full check needs and downloads, the reviewers' site, freshness through the GitHub API.
