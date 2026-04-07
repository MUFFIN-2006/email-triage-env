"""Rule loading and validation for the email triage engine."""

import json


def load_rules(path):
    """Load triage rules from a JSON file.

    Args:
        path: Path to the JSON rules file.

    Returns:
        A list of rule dicts, each with keys: name, category, priority,
        and conditions.

    Raises:
        ValueError: If the rules file is invalid or missing required fields.
        FileNotFoundError: If the path does not exist.
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError("Rules file must contain a JSON array of rule objects.")

    validated = []
    for idx, rule in enumerate(data):
        _validate_rule(rule, idx)
        validated.append(rule)

    return validated


def _validate_rule(rule, idx):
    """Validate a single rule dict.

    Args:
        rule: The rule dict to validate.
        idx: Index of the rule in the list (used in error messages).

    Raises:
        ValueError: If required fields are missing or have wrong types.
    """
    required = ("name", "category", "priority", "conditions")
    for field in required:
        if field not in rule:
            raise ValueError(
                f"Rule at index {idx} is missing required field '{field}'."
            )

    if not isinstance(rule["name"], str) or not rule["name"]:
        raise ValueError(f"Rule at index {idx}: 'name' must be a non-empty string.")
    if not isinstance(rule["category"], str) or not rule["category"]:
        raise ValueError(
            f"Rule at index {idx}: 'category' must be a non-empty string."
        )
    if not isinstance(rule["priority"], (int, float)):
        raise ValueError(f"Rule at index {idx}: 'priority' must be a number.")
    if not isinstance(rule["conditions"], list):
        raise ValueError(f"Rule at index {idx}: 'conditions' must be a list.")

    for cidx, condition in enumerate(rule["conditions"]):
        if "field" not in condition:
            raise ValueError(
                f"Rule '{rule['name']}', condition {cidx}: missing 'field'."
            )
        if "contains" not in condition:
            raise ValueError(
                f"Rule '{rule['name']}', condition {cidx}: missing 'contains'."
            )
        if not isinstance(condition["contains"], list):
            raise ValueError(
                f"Rule '{rule['name']}', condition {cidx}: "
                "'contains' must be a list of strings."
            )
