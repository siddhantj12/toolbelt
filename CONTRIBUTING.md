# Contributing

The bar for any change, human or agent:

1. **One concern per pull request.** A utility, its tests, and its docs — nothing else.
2. **No dependencies.** The standard library only. This is the point of the package.
3. **Tests are not optional.** Cover the happy path, the empty input, and the error case.
4. **Docstrings explain behaviour, not mechanics.** Say what a caller can rely on,
   including edge cases; a worked example beats a paragraph.
5. **No churn.** No reformatting, no renames, no comment padding, no whitespace-only diffs.
6. **Green before merge.** `pytest` and `ruff check .` both pass.

If nothing on the roadmap is worth doing well today, do nothing. An empty day is
a valid outcome; a filler commit is not.
