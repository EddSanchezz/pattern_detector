from dataclasses import dataclass


@dataclass
class MatchResult:
    value: str
    start: int
    end: int
    pattern: str

    def to_dict(self) -> dict:
        return {"value": self.value, "start": self.start, "end": self.end, "pattern": self.pattern}


@dataclass
class State:
    id: str
    is_accept: bool = False


class Automaton:
    def __init__(self, pattern_name: str):
        self.pattern_name = pattern_name
        self.states: dict[str, State] = {}
        self.transitions: dict[str, list[tuple[str, callable]]] = {}
        self.initial_state: str = ""

    def add_state(self, state_id: str, is_accept: bool = False) -> None:
        self.states[state_id] = State(id=state_id, is_accept=is_accept)

    def add_transition(self, from_state: str, to_state: str, condition: callable) -> None:
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append((to_state, condition))