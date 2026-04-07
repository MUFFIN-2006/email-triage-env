"""Tests for the EmailTriageEngine."""

import pytest

from src.triage import DEFAULT_CATEGORY, DEFAULT_PRIORITY, EmailTriageEngine

SAMPLE_RULES = [
    {
        "name": "urgent_keyword",
        "category": "Urgent",
        "priority": 10,
        "conditions": [
            {"field": "subject", "contains": ["urgent", "critical"]}
        ],
    },
    {
        "name": "support_request",
        "category": "Support",
        "priority": 5,
        "conditions": [
            {"field": "subject", "contains": ["help", "issue"]}
        ],
    },
    {
        "name": "spam_indicator",
        "category": "Spam",
        "priority": 0,
        "conditions": [
            {"field": "subject", "contains": ["win", "prize"]}
        ],
    },
]


@pytest.fixture
def engine():
    return EmailTriageEngine(SAMPLE_RULES)


class TestTriage:
    def test_matches_urgent_rule(self, engine):
        email = {"id": "1", "subject": "URGENT: fix this now", "body": ""}
        result = engine.triage(email)
        assert result["category"] == "Urgent"
        assert result["priority"] == 10
        assert "urgent_keyword" in result["matched_rules"]

    def test_case_insensitive_match(self, engine):
        email = {"id": "2", "subject": "Critical outage detected", "body": ""}
        result = engine.triage(email)
        assert result["category"] == "Urgent"

    def test_matches_support_rule(self, engine):
        email = {"id": "3", "subject": "Help with my account", "body": ""}
        result = engine.triage(email)
        assert result["category"] == "Support"
        assert result["priority"] == 5

    def test_matches_spam_rule(self, engine):
        email = {"id": "4", "subject": "You won a prize!", "body": ""}
        result = engine.triage(email)
        assert result["category"] == "Spam"
        assert result["priority"] == 0

    def test_no_match_returns_defaults(self, engine):
        email = {"id": "5", "subject": "Monthly newsletter", "body": ""}
        result = engine.triage(email)
        assert result["category"] == DEFAULT_CATEGORY
        assert result["priority"] == DEFAULT_PRIORITY
        assert result["matched_rules"] == []

    def test_highest_priority_rule_wins(self, engine):
        # Subject matches both 'urgent' and 'help' – urgent should win (priority 10 > 5)
        email = {"id": "6", "subject": "Urgent help needed", "body": ""}
        result = engine.triage(email)
        assert result["category"] == "Urgent"
        assert result["priority"] == 10
        assert "urgent_keyword" in result["matched_rules"]
        assert "support_request" in result["matched_rules"]

    def test_missing_field_treated_as_empty(self, engine):
        # Email has no 'subject' key; should not crash and should return defaults.
        email = {"id": "7"}
        result = engine.triage(email)
        assert result["category"] == DEFAULT_CATEGORY

    def test_result_contains_id(self, engine):
        email = {"id": "42", "subject": "test"}
        result = engine.triage(email)
        assert result["id"] == "42"

    def test_triage_batch_sorted_by_priority(self, engine):
        emails = [
            {"id": "a", "subject": "Monthly newsletter"},
            {"id": "b", "subject": "Help with issue"},
            {"id": "c", "subject": "URGENT fix now"},
        ]
        results = engine.triage_batch(emails)
        priorities = [r["priority"] for r in results]
        assert priorities == sorted(priorities, reverse=True)

    def test_triage_batch_empty_list(self, engine):
        assert engine.triage_batch([]) == []

    def test_no_rules_returns_defaults(self):
        engine_no_rules = EmailTriageEngine([])
        email = {"id": "1", "subject": "urgent problem"}
        result = engine_no_rules.triage(email)
        assert result["category"] == DEFAULT_CATEGORY
        assert result["matched_rules"] == []
