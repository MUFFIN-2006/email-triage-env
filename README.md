# email-triage-env

An email triage environment that automatically categorizes and prioritizes incoming emails using keyword-based rules and simple heuristics.

## Features

- **Categorization**: Classify emails into categories (e.g., Urgent, Support, Billing, Spam, General)
- **Priority scoring**: Assign a numeric priority score to each email
- **Rule-based engine**: Define custom triage rules via a JSON config file
- **CLI interface**: Process a batch of emails from a JSON file and output a triage report
- **Extensible**: Add new categories and rules without changing core logic

## Project Structure

```
email-triage-env/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── triage.py          # Core triage engine
│   ├── rules.py           # Rule definitions and loader
│   └── cli.py             # Command-line interface
├── config/
│   └── rules.json         # Default triage rules
├── samples/
│   └── emails.json        # Sample email data for testing
└── tests/
    ├── __init__.py
    ├── test_triage.py
    └── test_rules.py
```

## Installation

```bash
# Clone the repository
git clone https://github.com/muffin-2006/email-triage-env.git
cd email-triage-env

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Triage a batch of emails

```bash
python -m src.cli --input samples/emails.json --rules config/rules.json
```

### Use as a library

```python
from src.triage import EmailTriageEngine
from src.rules import load_rules

rules = load_rules("config/rules.json")
engine = EmailTriageEngine(rules)

email = {
    "id": "001",
    "subject": "URGENT: Server is down!",
    "body": "Production server is not responding. Please fix ASAP.",
    "sender": "ops@example.com"
}

result = engine.triage(email)
print(result)
# {'id': '001', 'category': 'Urgent', 'priority': 10, 'matched_rules': ['urgent_keyword']}
```

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/
```

## Configuration

Edit `config/rules.json` to add or modify triage rules. Each rule has:

| Field | Description |
|---|---|
| `name` | Unique rule identifier |
| `category` | Category to assign when rule matches |
| `priority` | Priority score (higher = more urgent) |
| `conditions` | List of field/keyword conditions to check |

Example rule:

```json
{
  "name": "urgent_keyword",
  "category": "Urgent",
  "priority": 10,
  "conditions": [
    {"field": "subject", "contains": ["urgent", "asap", "critical"]}
  ]
}
```

## License

MIT