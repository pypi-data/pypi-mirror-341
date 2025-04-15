# tests/test_passman.py
import pytest
from anythingpassword import passgenerator, passanalyzer, passentropy, passcommon

def test_passgenerator_length():
    password = passgenerator(12)
    assert len(password) == 12

def test_passanalyzer_strong():
    is_strong, feedback = passanalyzer("K7#mP9$qL2wR")
    assert is_strong
    assert feedback == "Password is strong!"

def test_passanalyzer_weak():
    is_strong, feedback = passanalyzer("weak")
    assert not is_strong
    assert "at least 8 characters" in feedback

def test_passentropy():
    entropy = passentropy("MyPass123!")
    assert entropy > 50  # Approximate check

def test_passcommon():
    is_common, message = passcommon("password")
    assert is_common
    assert "haveibeenpwned" in message