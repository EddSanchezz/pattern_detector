from .automaton import MatchResult
from .patterns import EmailAutomaton, PhoneAutomaton, DateAutomaton, URLAutomaton, PlateAutomaton, DocumentAutomaton
from .matcher import PatternMatcher

__all__ = ['MatchResult', 'EmailAutomaton', 'PhoneAutomaton', 'DateAutomaton', 'URLAutomaton', 'PlateAutomaton', 'DocumentAutomaton', 'PatternMatcher']