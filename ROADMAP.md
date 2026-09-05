# Roadmap

A queue of small, self-contained utilities worth adding. Each entry is roughly
one day's work: implementation, tests, and a docstring with a worked example.

Take the topmost unchecked item unless a better idea presents itself. Tick the
box in the same pull request that lands the work.

## Planned

### `toolbelt.iterables`
- [ ] `windowed(iterable, size)` — sliding windows of `size` consecutive items.
- [ ] `partition(iterable, predicate)` — split into matching and non-matching, one pass.
- [ ] `flatten(nested, depth=1)` — flatten nested iterables, strings treated as atoms.

### `toolbelt.text`
- [ ] `word_wrap(text, width)` — wrap preserving existing paragraph breaks.
- [ ] `common_prefix(strings)` — longest shared leading substring.
- [ ] `strip_ansi(text)` — remove ANSI escape sequences from terminal output.

### `toolbelt.mapping` (new module)
- [ ] `deep_merge(a, b)` — recursively merge nested dicts, `b` winning on conflicts.
- [ ] `get_path(mapping, "a.b.c", default=None)` — safe nested lookup.
- [ ] `invert(mapping)` — swap keys and values, with a documented collision rule.

### `toolbelt.timing` (new module)
- [ ] `Timer` context manager — wall-clock elapsed time with a readable `repr`.
- [ ] `retry(attempts, backoff)` — decorator with exponential backoff.

## Infrastructure
- [ ] Add `py.typed` marker so type checkers see the inline annotations.
- [ ] Add mypy to CI once the public surface stabilises.
- [ ] Property-based tests for `slugify` idempotence via Hypothesis.

## Done
- [x] `slugify`, `truncate` (`toolbelt.text`)
- [x] `batched`, `dedupe`, `chunk_by`, `first` (`toolbelt.iterables`)
