import pytest

from toolbelt.iterables import (
    batched,
    chunk_by,
    dedupe,
    first,
    flatten,
    group_by,
    partition,
    windowed,
)


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


class TestPartition:
    def test_splits_matches_from_non_matches(self):
        assert partition([1, 2, 3, 4, 5], lambda n: n % 2 == 0) == (
            [2, 4],
            [1, 3, 5],
        )

    def test_preserves_order_within_each_list(self):
        assert partition([5, 3, 4, 1, 2], lambda n: n % 2 == 0) == (
            [4, 2],
            [5, 3, 1],
        )

    def test_empty_input_returns_two_empty_lists(self):
        assert partition([], lambda n: True) == ([], [])

    def test_predicate_error_propagates(self):
        def blows_up(n):
            if n == 2:
                raise ValueError("boom")
            return True

        with pytest.raises(ValueError):
            partition([1, 2, 3], blows_up)


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


class TestGroupBy:
    def test_groups_non_adjacent_matches_together(self):
        words = ["ant", "bee", "ape", "cow"]
        assert group_by(words, key=lambda w: w[0]) == {
            "a": ["ant", "ape"],
            "b": ["bee"],
            "c": ["cow"],
        }

    def test_keys_appear_in_first_seen_order(self):
        assert list(group_by([3, 1, 3, 2, 1], key=lambda n: n)) == [3, 1, 2]

    def test_empty_input_returns_empty_dict(self):
        assert group_by([], key=lambda x: x) == {}

    def test_key_error_propagates(self):
        def blows_up(n):
            if n == 2:
                raise ValueError("boom")
            return n

        with pytest.raises(ValueError):
            group_by([1, 2, 3], key=blows_up)


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


class TestWindowed:
    def test_slides_by_one(self):
        assert list(windowed([1, 2, 3, 4], 2)) == [[1, 2], [2, 3], [3, 4]]

    def test_size_one_yields_singletons(self):
        assert list(windowed([1, 2, 3], 1)) == [[1], [2], [3]]

    def test_size_equal_to_length_yields_one_window(self):
        assert list(windowed([1, 2, 3], 3)) == [[1, 2, 3]]

    def test_empty_input_yields_nothing(self):
        assert list(windowed([], 2)) == []

    def test_too_few_items_yields_nothing(self):
        assert list(windowed([1, 2], 3)) == []

    def test_consumes_a_generator_lazily(self):
        assert list(windowed((n for n in range(4)), 2)) == [[0, 1], [1, 2], [2, 3]]

    def test_size_below_one_raises(self):
        with pytest.raises(ValueError):
            list(windowed([1, 2], 0))


class TestFlatten:
    def test_default_depth_flattens_one_level(self):
        nested = [1, [2, 3], [4, [5, 6]]]
        assert list(flatten(nested)) == [1, 2, 3, 4, [5, 6]]

    def test_depth_two_flattens_two_levels(self):
        nested = [1, [2, [3, 4]]]
        assert list(flatten(nested, depth=2)) == [1, 2, 3, 4]

    def test_depth_zero_yields_items_unchanged(self):
        nested = [1, [2, 3]]
        assert list(flatten(nested, depth=0)) == [1, [2, 3]]

    def test_strings_are_treated_as_atoms(self):
        assert list(flatten(["ab", ["cd", "ef"]])) == ["ab", "cd", "ef"]

    def test_empty_input_yields_nothing(self):
        assert list(flatten([])) == []

    def test_negative_depth_raises(self):
        with pytest.raises(ValueError):
            list(flatten([1, 2], depth=-1))
