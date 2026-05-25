import pytest
from automata import PatternMatcher


class TestExecutor:
    def test_empty_match(self):
        matcher = PatternMatcher()
        # Test that empty values don't crash
        valid, _, _, _ = matcher.validate("email", "")
        assert valid == False

    def test_find_all_simple(self):
        matcher = PatternMatcher()
        results = matcher.search("aaa", ["email"])
        # Should not crash, returns empty dict or valid result
        assert isinstance(results, dict)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])