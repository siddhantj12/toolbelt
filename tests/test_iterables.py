import pytest

from toolbelt.iterables import batched, chunk_by, dedupe, first


class TestBatched:
    def test_splits_into_even_batches(self):
        assert list(batched([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    def test_final_batch_is_short(self):
        assert list(batched([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    def test_empty_input_yields_nothing(self):
        assert list(batched([], 3)) == []

    def test_consumes_a_generator_lazily(self):
        assert list(batched((n for n in range(5)), 2)) == [[0, 1], [2, 3], [4]]

    def test_size_below_one_raises(self):
        with pytest.raises(ValueError):
            list(batched([1, 2], 0))


class TestDedupe:
    def test_removes_duplicates_preserving_order(self):
        assert list(dedupe([3, 1, 3, 2, 1])) == [3, 1, 2]

    def test_keeps_first_occurrence(self):
        pairs = [("a", 1), ("a", 2), ("b", 3)]
        assert list(dedupe(pairs, key=lambda p: p[0])) == [("a", 1), ("b", 3)]

    def test_empty_input_yields_nothing(self):
        assert list(dedupe([])) == []


class TestFirst:
    def test_returns_first_item(self):
        assert first([3, 1, 2]) == 3

    def test_empty_input_returns_none_by_default(self):
        assert first([]) is None

    def test_empty_input_returns_given_default(self):
        assert first([], default="none") == "none"

    def test_only_consumes_one_item_from_a_generator(self):
        seen = []

        def gen():
            for n in range(5):
                seen.append(n)
                yield n

        assert first(gen()) == 0
        assert seen == [0]


class TestChunkBy:
    def test_groups_consecutive_matches(self):
        words = ["ant", "ape", "bee", "cow", "cat"]
        assert list(chunk_by(words, key=lambda w: w[0])) == [
            ["ant", "ape"],
            ["bee"],
            ["cow", "cat"],
        ]

    def test_non_adjacent_matches_form_separate_groups(self):
        assert list(chunk_by([1, 1, 2, 1], key=lambda n: n)) == [[1, 1], [2], [1]]

    def test_empty_input_yields_nothing(self):
        assert list(chunk_by([], key=lambda x: x)) == []

    def test_falsy_first_item_still_starts_a_group(self):
        assert list(chunk_by([0, 0, 1], key=lambda n: n)) == [[0, 0], [1]]
