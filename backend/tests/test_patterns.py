import pytest
from automata import PatternMatcher


class TestPatterns:
    def setup_method(self):
        self.matcher = PatternMatcher()

    def test_email_valid(self):
        valid, name, val, error = self.matcher.validate("email", "edwar5020@gmail.com")
        assert valid == True
        assert error is None

    def test_email_invalid(self):
        valid, name, val, error = self.matcher.validate("email", "invalid")
        assert valid == False

    def test_phone_valid(self):
        valid, name, val, error = self.matcher.validate("phone", "3217539293")
        assert valid == True

    def test_phone_invalid(self):
        valid, name, val, error = self.matcher.validate("phone", "abc")
        assert valid == False

    def test_date_valid(self):
        valid, name, val, error = self.matcher.validate("date", "25/12/2024")
        assert valid == True

    def test_url_valid(self):
        valid, name, val, error = self.matcher.validate("url", "http://google.com")
        assert valid == True

    def test_plate_valid(self):
        valid, name, val, error = self.matcher.validate("plate", "ABC-123")
        assert valid == True

    def test_document_id_valid(self):
        valid, name, val, error = self.matcher.validate("document_id", "CC123456")
        assert valid == True


class TestSearchPatterns:
    def setup_method(self):
        self.matcher = PatternMatcher()

    def test_search_email_only(self):
        text = "edwar5020@gmail.com"
        results = self.matcher.search(text, ["email"])
        assert "email" in results
        assert len(results["email"]) > 0

    def test_search_phone_only(self):
        text = "3217539293"
        results = self.matcher.search(text, ["phone"])
        assert "phone" in results
        assert len(results["phone"]) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])