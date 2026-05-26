import pytest
from automata import PatternMatcher


class TestPatterns:
    def setup_method(self):
        self.matcher = PatternMatcher()

    def test_email_valid(self):
        valid, name, val, error = self.matcher.validate("email", "edwar5020@gmail.com")
        assert valid == True
        assert error is None

    def test_email_invalid_no_at(self):
        valid, name, val, error = self.matcher.validate("email", "invalidemail")
        assert valid == False

    def test_email_invalid_no_domain(self):
        valid, name, val, error = self.matcher.validate("email", "test@")
        assert valid == False

    def test_email_invalid_no_tld(self):
        valid, name, val, error = self.matcher.validate("email", "test@example")
        assert valid == False

    def test_phone_valid_mobile(self):
        valid, name, val, error = self.matcher.validate("phone", "3217539293")
        assert valid == True

    def test_phone_valid_international(self):
        valid, name, val, error = self.matcher.validate("phone", "+57 3001234567")
        assert valid == True

    def test_phone_invalid_too_short(self):
        valid, name, val, error = self.matcher.validate("phone", "123")
        assert valid == False

    def test_phone_invalid_letters(self):
        valid, name, val, error = self.matcher.validate("phone", "abc")
        assert valid == False

    def test_date_valid_slash(self):
        valid, name, val, error = self.matcher.validate("date", "25/12/2024")
        assert valid == True

    def test_date_valid_dash(self):
        valid, name, val, error = self.matcher.validate("date", "25-12-2024")
        assert valid == True

    def test_date_invalid_month(self):
        valid, name, val, error = self.matcher.validate("date", "32/12/2024")
        assert valid == False

    def test_date_invalid_format(self):
        valid, name, val, error = self.matcher.validate("date", "2024-12-25")
        assert valid == False

    def test_url_valid_https(self):
        valid, name, val, error = self.matcher.validate("url", "https://google.com")
        assert valid == True

    def test_url_valid_http(self):
        valid, name, val, error = self.matcher.validate("url", "http://test.org/path")
        assert valid == True

    def test_url_valid_www(self):
        valid, name, val, error = self.matcher.validate("url", "www.example.com")
        assert valid == True

    def test_plate_valid_old_format(self):
        valid, name, val, error = self.matcher.validate("plate", "ABC-123")
        assert valid == True

    def test_plate_valid_new_format(self):
        valid, name, val, error = self.matcher.validate("plate", "ABC-12D")
        assert valid == True

    def test_plate_invalid_lowercase(self):
        valid, name, val, error = self.matcher.validate("plate", "abc-123")
        assert valid == False

    def test_plate_invalid_no_hyphen(self):
        valid, name, val, error = self.matcher.validate("plate", "ABC123")
        assert valid == False

    def test_document_id_valid_cc(self):
        valid, name, val, error = self.matcher.validate("document_id", "CC123456789")
        assert valid == True

    def test_document_id_valid_nit(self):
        valid, name, val, error = self.matcher.validate("document_id", "NIT9876543")
        assert valid == True

    def test_document_id_valid_bare(self):
        valid, name, val, error = self.matcher.validate("document_id", "12345678")
        assert valid == True

    def test_password_valid(self):
        valid, name, val, error = self.matcher.validate("password", "Password123!")
        assert valid == True

    def test_password_invalid_too_short(self):
        valid, name, val, error = self.matcher.validate("password", "Pass1!")
        assert valid == False

    def test_password_invalid_no_uppercase(self):
        valid, name, val, error = self.matcher.validate("password", "password123!")
        assert valid == False

    def test_password_invalid_no_lowercase(self):
        valid, name, val, error = self.matcher.validate("password", "PASSWORD123!")
        assert valid == False

    def test_password_invalid_no_digit(self):
        valid, name, val, error = self.matcher.validate("password", "PasswordABC!")
        assert valid == False

    def test_password_invalid_no_special(self):
        valid, name, val, error = self.matcher.validate("password", "Password123")
        assert valid == False

    def test_password_valid_complex(self):
        valid, name, val, error = self.matcher.validate("password", "MyP@ssw0rd!2024")
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

    def test_search_multiple_patterns(self):
        text = "Contact: test@example.com, Phone: 3217539293"
        results = self.matcher.search(text, ["email", "phone"])
        assert "email" in results
        assert "phone" in results

    def test_search_password_in_text(self):
        text = "La clave es: SecurePass123!"
        results = self.matcher.search(text, ["password"])
        assert "password" in results

    def test_search_no_matches(self):
        text = "No patterns here"
        results = self.matcher.search(text, ["email", "phone", "password"])
        assert results["email"] == []
        assert results["phone"] == []


class TestEdgeCases:
    def setup_method(self):
        self.matcher = PatternMatcher()

    def test_empty_value(self):
        valid, _, _, _ = self.matcher.validate("email", "")
        assert valid == False

    def test_whitespace_only(self):
        valid, _, _, _ = self.matcher.validate("email", "   ")
        assert valid == False

    def test_nonexistent_pattern(self):
        valid, name, val, error = self.matcher.validate("nonexistent", "value")
        assert valid == False

    def test_search_empty_text(self):
        results = self.matcher.search("", ["email"])
        assert results["email"] == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])