"""Command-line interface for the email triage environment."""

import argparse
import json
import sys

from src.rules import load_rules
from src.triage import EmailTriageEngine


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Triage a batch of emails using configurable rules."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a JSON file containing a list of email objects.",
    )
    parser.add_argument(
        "--rules",
        required=True,
        help="Path to a JSON file containing triage rules.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write the triage report JSON. "
        "Defaults to stdout.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    try:
        rules = load_rules(args.rules)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error loading rules: {exc}", file=sys.stderr)
        return 1

    try:
        with open(args.input, "r", encoding="utf-8") as fh:
            emails = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error loading emails: {exc}", file=sys.stderr)
        return 1

    engine = EmailTriageEngine(rules)
    results = engine.triage_batch(emails)

    report = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Triage report written to {args.output}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
