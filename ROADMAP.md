# Roadmap

A queue of small, self-contained utilities worth adding. Each entry is roughly
one day's work: implementation, tests, and a docstring with a worked example.

Take the topmost unchecked item unless a better idea presents itself. Tick the
box in the same pull request that lands the work.

## Planned

### Next batch (added 2026-09-24)

`toolbelt.iterables`
- [ ] `group_by(iterable, key)` — dict of lists, first-seen key order, no pre-sorting needed.
- [ ] `count_by(iterable, key)` — dict of counts per key, first-seen key order.
- [ ] `interleave(*iterables)` — round-robin across inputs until all are exhausted.
- [ ] `unique_justseen(iterable, key=None)` — drop consecutive duplicates only.
- [ ] `split_at(iterable, predicate)` — split into lists at items matching `predicate`, dropping them.
- [ ] `nth(iterable, n, default=None)` — item at index `n` of any iterable without raising.
- [ ] `peekable(iterable)` — iterator wrapper with `.peek(default)` that doesn't consume.

`toolbelt.text`
- [ ] `snake_case(text)` — from camelCase, PascalCase, kebab and spaced input, acronyms kept together.
- [ ] `camel_case(text)` — the inverse, with a documented rule for acronyms.
- [ ] `ordinal(n)` — `1st`, `22nd`, `113th`, including the 11–13 exceptions.
- [ ] `pluralize(count, singular, plural=None)` — `"1 file"`, `"3 files"`.
- [ ] `human_bytes(n, *, binary=True)` — `"1.5 MiB"` / `"1.6 MB"`.
- [ ] `mask(value, visible=4, char="*")` — hide all but the last `visible` characters.

`toolbelt.mapping`
- [ ] `pick(mapping, keys)` and `omit(mapping, keys)` — key subsetting as new dicts.
- [ ] `set_path(mapping, "a.b.c", value)` — new dict with a nested value set, intermediates created.
- [ ] `flatten_dict(mapping, sep=".")` — nested dict to dotted keys.
- [ ] `unflatten_dict(mapping, sep=".")` — the inverse, raising on key collisions.

`toolbelt.timing`
- [ ] `human_duration(seconds)` — `"1h 2m 3s"`, with sub-second handling documented.
- [ ] `parse_duration(text)` — `"1h30m"` to seconds, the inverse of `human_duration`.

`toolbelt.functional` (new module)
- [ ] `once(func)` — call at most once, return the cached result after.
- [ ] `compose(*funcs)` — right-to-left function composition.

`toolbelt.files` (new module)
- [ ] `atomic_write(path, text)` — write via a temp file in the same directory and `os.replace`.
- [ ] `read_lines(path, *, strip=True, skip_blank=True)` — lines of a text file as a list.

### `toolbelt.iterables`
- [ ] `partition(iterable, predicate)` — split into matching and non-matching, one pass.


- [ ] `windowed(iterable, size)` — sliding windows of `size` consecutive items.
- [ ] `first(iterable, default=None)` — first item without raising on empty input.


- [ ] `flatten(nested, depth=1)` — flatten nested iterables, strings treated as atoms.



### `toolbelt.text`
- [ ] `common_prefix(strings)` — longest shared leading substring.


- [ ] `word_wrap(text, width)` — wrap preserving existing paragraph breaks.
- [ ] `strip_ansi(text)` — remove ANSI escape sequences from terminal output.



### `toolbelt.mapping` (new module)
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
- [x] `slugify`, `truncate`, `word_wrap`, `common_prefix`, `strip_ansi` (`toolbelt.text`)
- [x] `batched`, `dedupe`, `chunk_by`, `windowed`, `partition`, `first`, `flatten` (`toolbelt.iterables`)
- [x] `deep_merge` (`toolbelt.mapping`)
