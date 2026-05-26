from .automaton import MatchResult


class PatternAutomaton:
    def __init__(self, pattern_name: str):
        self.pattern_name = pattern_name
        self.states: dict[str, bool] = {}
        self.transitions: dict[str, list[tuple[str, callable]]] = {}

    def add_state(self, state_id: str, is_accept: bool = False) -> None:
        self.states[state_id] = is_accept

    def add_transition(self, from_state: str, to_state: str, condition: callable) -> None:
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append((to_state, condition))

    def get_next_state(self, current_state: str, char: str) -> str | None:
        if current_state not in self.transitions:
            return None
        for to_state, condition in self.transitions[current_state]:
            if condition(char):
                return to_state
        return None


class EmailAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("email")

    def _is_valid_local(self, s: str) -> bool:
        if not s:
            return False
        return all(c.isalnum() or c in "._%+-" for c in s)

    def _is_valid_domain(self, s: str) -> bool:
        if not s:
            return False
        return all(c.isalnum() or c == "-" for c in s)

    def _is_valid_tld(self, s: str) -> bool:
        if len(s) < 2 or len(s) > 10:
            return False
        return s.isalpha()

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        n = len(text)
        while i < n:
            # Quick check if @ exists in remaining text
            at_pos = text.find("@", i)
            if at_pos == -1:
                break  # No more @ found, exit immediately
            
            # Local part validation: from i to at_pos (must have at least 1 char)
            if at_pos - i < 1:
                i += 1
                continue
            
            local_part = text[i:at_pos]
            if not self._is_valid_local(local_part):
                i = at_pos + 1  # Skip past this @
                continue
            
            # Find dot after @
            dot_pos = text.find(".", at_pos + 1)
            if dot_pos == -1:
                i = at_pos + 1
                continue
            
            # Domain part: at_pos+1 to dot_pos (must have at least 1 alnum/hyphen char)
            domain_part = text[at_pos + 1:dot_pos]
            if not self._is_valid_domain(domain_part):
                i = dot_pos + 1
                continue
            
            # TLD: after dot, collect only alphabetic characters (stop at digit, /, space, etc.)
            tld_start = dot_pos + 1
            tld_end = tld_start
            while tld_end < n and text[tld_end].isalpha():
                tld_end += 1
            tld_part = text[tld_start:tld_end]
            if not self._is_valid_tld(tld_part):
                i = dot_pos + 1
                continue
            
            # Valid email found!
            end_pos = tld_start + len(tld_part)
            results.append(MatchResult(value=text[i:end_pos], start=i, end=end_pos, pattern=self.pattern_name))
            i = end_pos
        
        return results


class PhoneAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("phone")
        for i in range(10):
            self.add_state(f"s{i}")
        self.add_state("accept", True)
        for i in range(9):
            self.add_transition(f"s{i}", f"s{i+1}", lambda c: c.isdigit())

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            matched = False
            # Format 1: +57 3XXXXXXXXX (with space)
            if text[i:i+4] == "+57 " and i + 14 <= len(text) and text[i+4:i+14].isdigit():
                results.append(MatchResult(value=text[i:i+14], start=i, end=i+14, pattern=self.pattern_name))
                i += 14
                matched = True
            # Format 2: +573XXXXXXXXX (no space)
            elif text[i:i+3] == "+57" and i + 13 <= len(text) and text[i+3:i+13].isdigit():
                results.append(MatchResult(value=text[i:i+13], start=i, end=i+13, pattern=self.pattern_name))
                i += 13
                matched = True
            # Format 3: 3XXXXXXXXX (bare mobile)
            elif text[i] == "3" and i + 10 <= len(text) and text[i+1:i+11].isdigit():
                results.append(MatchResult(value=text[i:i+10], start=i, end=i+10, pattern=self.pattern_name))
                i += 10
                matched = True
            if not matched:
                i += 1
        return results


class DateAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("date")

    def _days_in_month(self, month: int, year: int) -> int:
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        elif month == 2:
            # Leap year check
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        return 0

    def _valid_date(self, date: str) -> bool:
        # Colombian format: DD/MM/YYYY or DD-MM-YYYY (exactly)
        if "/" in date:
            parts = date.split("/")
            sep = "/"
        elif "-" in date:
            parts = date.split("-")
            sep = "-"
        else:
            return False
        if len(parts) != 3:
            return False
        day, month, year = parts
        # Must be exactly 2 digits for day, 2 for month, 4 for year
        if not (len(day) == 2 and len(month) == 2 and len(year) == 4):
            return False
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return False
        try:
            m = int(month)
            d = int(day)
            y = int(year)
            if not (1 <= m <= 12):
                return False
            if not (1 <= d <= self._days_in_month(m, y)):
                return False
            return True
        except:
            return False

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            if text[i].isdigit():
                start = i
                j = i
                # Day: exactly 2 digits
                if j + 2 < len(text) and text[j:j+2].isdigit():
                    j += 2
                    sep = text[j] if text[j] in "/-" else None
                    if sep is None:
                        i += 1
                        continue
                    j += 1
                    # Month: exactly 2 digits
                    if j + 2 < len(text) and text[j:j+2].isdigit():
                        j += 2
                        if text[j] != sep:
                            i += 1
                            continue
                        j += 1
                        # Year: exactly 4 digits
                        if j + 4 <= len(text) and text[j:j+4].isdigit():
                            j += 4
                            candidate = text[start:j]
                            if self._valid_date(candidate):
                                results.append(MatchResult(value=candidate, start=start, end=j, pattern=self.pattern_name))
                                i = j
                                continue
                i += 1
            else:
                i += 1
        return results


class URLAutomaton(PatternAutomaton):
    MAX_URL_LENGTH = 500

    def __init__(self):
        super().__init__("url")

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            lower = text[i:].lower()
            if lower.startswith("http://") or lower.startswith("https://") or lower.startswith("www."):
                start = i
                j = i
                # Limit URL length to prevent infinite loops on text without whitespace
                max_end = min(len(text), i + self.MAX_URL_LENGTH)
                while j < max_end and text[j] not in " \t\n":
                    j += 1
                results.append(MatchResult(value=text[start:j], start=start, end=j, pattern=self.pattern_name))
                i = j
            else:
                i += 1
        return results


class PlateAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("plate")

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            # Colombian plates: must start with 3 uppercase letters
            # Old format: ABC-123 (3 letters + hyphen + 3 digits)
            # New format: ABC-12D (3 letters + hyphen + 2 digits + 1 letter)
            # New format: HLQ-75E (3 letters + hyphen + 2 digits + 1 letter)
            if text[i].isupper() and text[i].isalpha() and i + 3 < len(text):
                # Check first 3 chars are letters
                first3 = text[i:i+3]
                if not all(c.isalpha() and c.isupper() for c in first3):
                    i += 1
                    continue
                # Next char must be hyphen
                j = i + 3
                if j >= len(text) or text[j] != "-":
                    i += 1
                    continue
                # Skip the hyphen
                j += 1
                # Collect digits after hyphen
                digits = 0
                while j < len(text) and text[j].isdigit() and digits < 4:
                    digits += 1
                    j += 1
                # Check for new format with trailing letter (2 digits + 1 letter)
                has_trailing_letter = False
                if digits == 2 and j < len(text) and text[j].isalpha():
                    has_trailing_letter = True
                    j += 1
                # Valid plate requires:
                # - 3 letters (already verified)
                # - hyphen (already verified)
                # - 3 digits OR 2 digits + 1 letter
                is_valid = False
                if has_trailing_letter:
                    # New format: 3 letters + hyphen + 2 digits + 1 letter
                    is_valid = True
                elif digits == 3:
                    # Old format: 3 letters + hyphen + 3 digits
                    is_valid = True
                if is_valid:
                    plate = text[i:j]
                    results.append(MatchResult(value=plate, start=i, end=j, pattern=self.pattern_name))
                    i = j
                else:
                    i += 1
            else:
                i += 1
        return results


class PasswordAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("password")

    def _is_valid_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        return has_upper and has_lower and has_digit and has_special

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            start = i
            j = i
            while j < len(text) and text[j] not in " \t\n":
                j += 1
            candidate = text[start:j]
            if len(candidate) >= 8 and self._is_valid_password(candidate):
                results.append(MatchResult(value=candidate, start=start, end=j, pattern=self.pattern_name))
                i = j
            else:
                i += 1
        return results


class DocumentAutomaton(PatternAutomaton):
    def __init__(self):
        super().__init__("document_id")
        self.types = ["CC", "NIT", "TI", "RC", "PEP"]

    def process(self, text: str) -> list[MatchResult]:
        results = []
        i = 0
        while i < len(text):
            matched = False
            # Try prefixed documents first (CC, NIT, TI, RC, PEP + 6+ digits)
            for t in self.types:
                if text[i:].upper().startswith(t) and i + len(t) + 6 <= len(text):
                    suffix = text[i+len(t):i+len(t)+10]
                    if suffix.isdigit() and len(suffix) >= 6:
                        doc = t + suffix[:max(6, len(suffix))]
                        results.append(MatchResult(value=doc, start=i, end=i+len(doc), pattern=self.pattern_name))
                        i += len(doc)
                        matched = True
                        break
            # If no prefix matched, try bare document (6-10 consecutive digits)
            # But NOT if it looks like a phone (starts with 3 and 10 digits)
            if not matched:
                if text[i].isdigit():
                    start = i
                    j = i
                    while j < len(text) and text[j].isdigit() and j - i < 10:
                        j += 1
                    doc_num = text[start:j]
                    doc_len = len(doc_num)
                    # Check if it's a phone number (starts with 3 and exactly 10 digits)
                    is_phone = doc_len == 10 and doc_num.startswith("3")
                    if 6 <= doc_len <= 10 and not is_phone:
                        results.append(MatchResult(value=doc_num, start=start, end=j, pattern=self.pattern_name))
                        i = j
                        matched = True
            if not matched:
                i += 1
        return results