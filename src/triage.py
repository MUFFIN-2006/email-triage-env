"""Core email triage engine."""

DEFAULT_CATEGORY = "General"
DEFAULT_PRIORITY = 1


class EmailTriageEngine:
    """Triage engine that categorizes and prioritizes emails using rules.

    Rules are evaluated in order. The first matching rule determines the
    category and priority of the email. If no rule matches, the email is
    assigned the default category and lowest priority.

    Args:
        rules: A list of rule dicts as returned by :func:`src.rules.load_rules`.
    """

    def __init__(self, rules):
        self._rules = rules

    def triage(self, email):
        """Triage a single email.

        Args:
            email: A dict with at least an ``id`` key. May also contain
                ``subject``, ``body``, and ``sender`` keys.

        Returns:
            A dict with keys:
                - ``id``: the email id.
                - ``category``: matched category or ``'General'``.
                - ``priority``: matched priority or ``1``.
                - ``matched_rules``: list of rule names that matched.
        """
        matched_rules = []
        best_category = None
        best_priority = None

        for rule in self._rules:
            if self._rule_matches(rule, email):
                matched_rules.append(rule["name"])
                # Keep the highest-priority matching rule for category/priority.
                if best_priority is None or rule["priority"] > best_priority:
                    best_category = rule["category"]
                    best_priority = rule["priority"]

        return {
            "id": email.get("id"),
            "category": best_category if best_category is not None else DEFAULT_CATEGORY,
            "priority": best_priority if best_priority is not None else DEFAULT_PRIORITY,
            "matched_rules": matched_rules,
        }

    def triage_batch(self, emails):
        """Triage a list of emails.

        Args:
            emails: An iterable of email dicts.

        Returns:
            A list of triage result dicts, one per email, sorted by priority
            descending (most urgent first).
        """
        results = [self.triage(email) for email in emails]
        results.sort(key=lambda r: r["priority"], reverse=True)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _rule_matches(self, rule, email):
        """Return True if *all* conditions in *rule* match *email*."""
        for condition in rule["conditions"]:
            field_value = email.get(condition["field"], "") or ""
            field_lower = field_value.lower()
            keywords = [kw.lower() for kw in condition["contains"]]
            if not any(kw in field_lower for kw in keywords):
                return False
        return True
