"""Tests for the rules loader."""

import json
import os

import pytest

from src.rules import load_rules


VALID_RULE = {
    "name": "urgent_keyword",
    "category": "Urgent",
    "priority": 10,
    "conditions": [{"field": "subject", "contains": ["urgent"]}],
}


class TestLoadRules:
    def test_loads_valid_rules(self, tmp_path):
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([VALID_RULE]), encoding="utf-8")
        rules = load_rules(str(path))
        assert len(rules) == 1
        assert rules[0]["name"] == "urgent_keyword"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_rules("/nonexistent/path/rules.json")

    def test_not_a_list_raises_value_error(self, tmp_path):
        path = tmp_path / "rules.json"
        path.write_text(json.dumps({"name": "bad"}), encoding="utf-8")
        with pytest.raises(ValueError, match="JSON array"):
            load_rules(str(path))

    def test_missing_name_raises_value_error(self, tmp_path):
        rule = {k: v for k, v in VALID_RULE.items() if k != "name"}
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="'name'"):
            load_rules(str(path))

    def test_missing_category_raises_value_error(self, tmp_path):
        rule = {k: v for k, v in VALID_RULE.items() if k != "category"}
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="'category'"):
            load_rules(str(path))

    def test_missing_priority_raises_value_error(self, tmp_path):
        rule = {k: v for k, v in VALID_RULE.items() if k != "priority"}
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="'priority'"):
            load_rules(str(path))

    def test_missing_conditions_raises_value_error(self, tmp_path):
        rule = {k: v for k, v in VALID_RULE.items() if k != "conditions"}
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="'conditions'"):
            load_rules(str(path))

    def test_condition_missing_field_raises_value_error(self, tmp_path):
        rule = dict(VALID_RULE)
        rule["conditions"] = [{"contains": ["urgent"]}]
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="missing 'field'"):
            load_rules(str(path))

    def test_condition_missing_contains_raises_value_error(self, tmp_path):
        rule = dict(VALID_RULE)
        rule["conditions"] = [{"field": "subject"}]
        path = tmp_path / "rules.json"
        path.write_text(json.dumps([rule]), encoding="utf-8")
        with pytest.raises(ValueError, match="missing 'contains'"):
            load_rules(str(path))

    def test_loads_default_rules_file(self):
        """Smoke-test: the bundled config/rules.json should load without errors."""
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rules_path = os.path.join(repo_root, "config", "rules.json")
        rules = load_rules(rules_path)
        assert len(rules) > 0
