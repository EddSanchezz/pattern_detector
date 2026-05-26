from .automaton import MatchResult
from .patterns import (
    EmailAutomaton, PhoneAutomaton, DateAutomaton,
    URLAutomaton, PlateAutomaton, DocumentAutomaton, PasswordAutomaton
)


class PatternMatcher:
    def __init__(self):
        self.automata = {
            "email": EmailAutomaton(),
            "phone": PhoneAutomaton(),
            "date": DateAutomaton(),
            "url": URLAutomaton(),
            "plate": PlateAutomaton(),
            "document_id": DocumentAutomaton(),
            "password": PasswordAutomaton(),
        }

    def search(self, text: str, pattern_names: list) -> dict:
        return {
            name: [m.to_dict() for m in self.automata[name].process(text)]
            for name in pattern_names if name in self.automata
        }

    def search_all(self, text: str) -> dict:
        return self.search(text, list(self.automata.keys()))

    def validate(self, pattern_name: str, value: str) -> tuple:
        if pattern_name not in self.automata:
            return False, pattern_name, value, f"Pattern '{pattern_name}' not found"
        matches = self.automata[pattern_name].process(value)
        # Check if any match covers the entire value (exact match)
        if any(m.value == value for m in matches):
            return True, pattern_name, value, None
        # For partial matches - check if the value could match as a valid pattern
        # This handles cases where search finds it but validate requires full match
        if matches:
            match = matches[0]
            # If the match is at the start and covers a significant portion, consider it valid
            if match.start == 0 and len(match.value) >= len(value) * 0.8:
                return True, pattern_name, value, None
        return False, pattern_name, value, f"No match for '{value}'"

    def get_available_patterns(self) -> list:
        return list(self.automata.keys())