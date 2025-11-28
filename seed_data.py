"""
Seed initial prompts for Kiro Prompt Library
"""

import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent / "data" / "prompts.json"

SEED_PROMPTS = [
    {
        "id": 1,
        "title": "API Client Generator",
        "category": "API Development",
        "prompt": """Erstelle einen Python REST API Client mit folgenden Anforderungen:

ARCHITEKTUR:
- BaseClient Klasse mit gemeinsamer Logik
- Spezifische Endpoint-Methoden als Subclass
- Dependency Injection für Configuration

FEATURES:
- Retry Logic mit exponential backoff (tenacity)
- Timeout Configuration
- Request/Response Logging
- Type Hints für alle Methoden
- Pydantic Models für Request/Response

ERROR HANDLING:
- Custom Exceptions (APIError, AuthenticationError, RateLimitError)
- Structured Error Messages mit Context
- Automatic Token Refresh bei 401

TESTING:
- pytest mit responses/httpx-mock
- Fixtures für API Responses
- Edge Cases (Timeout, 5xx, Rate Limit)

CODE QUALITY:
- Black formatiert
- Type Hints
- Docstrings (Google Style)
- Logging statt Print""",
        "author": "Daniel Jährling",
        "tags": ["python", "api", "rest", "client", "testing"],
        "rating": 4.5,
        "votes": 2,
        "usage_count": 5,
        "created_at": datetime.now().isoformat(),
        "comments": []
    },
    {
        "id": 2,
        "title": "Data Pipeline Builder",
        "category": "Data Processing",
        "prompt": """Erstelle eine Data Processing Pipeline mit folgender Architektur:

PIPELINE STAGES:
1. Input Stage: Multi-Format Reader (CSV, Excel, JSON, XML)
2. Validation Stage: Schema Validation mit Pydantic
3. Transformation Stage: Business Logic
4. Output Stage: Multi-Format Writer

FEATURES:
- Streaming für große Dateien (nicht alles in Memory)
- Progress Bar (tqdm)
- Partial Resume bei Fehler (Checkpoint-System)
- Parallel Processing (ThreadPoolExecutor/ProcessPoolExecutor)
- Dry-Run Mode für Testing

ERROR HANDLING:
- Validation Errors sammeln (nicht bei erstem Fehler abbrechen)
- Error Report mit Zeilen-Nummern
- Quarantine für fehlerhafte Records
- Retry-Mechanismus für transiente Fehler

MONITORING:
- Structured Logging mit Context
- Metrics (processed, failed, skipped)
- Execution Time Tracking
- Memory Usage Monitoring

CLI:
- argparse mit Subcommands
- Config File Support (YAML/JSON)
- Verbose/Debug Modes""",
        "author": "Daniel Jährling",
        "tags": ["python", "etl", "pipeline", "batch", "data-processing"],
        "rating": 5.0,
        "votes": 3,
        "usage_count": 8,
        "created_at": datetime.now().isoformat(),
        "comments": []
    },
    {
        "id": 3,
        "title": "Pytest Test Suite Generator",
        "category": "Testing",
        "prompt": """Generiere eine vollständige Pytest Test Suite für die gegebene Funktion/Klasse:

REQUIREMENTS:
- Fixtures für Setup/Teardown
- Parametrized Tests für verschiedene Inputs
- Edge Cases (None, Empty, Invalid)
- Mock externe Dependencies
- Assert mit aussagekräftigen Messages

COVERAGE:
- Happy Path
- Error Cases
- Boundary Conditions
- Type Validation

STRUCTURE:
- Arrange-Act-Assert Pattern
- Descriptive Test Names (test_should_...)
- Docstrings für komplexe Tests

QUALITY:
- Type Hints
- pytest-cov für Coverage Report
- pytest-mock für Mocking""",
        "author": "Daniel Jährling",
        "tags": ["python", "testing", "pytest", "tdd", "quality"],
        "rating": 4.8,
        "votes": 5,
        "usage_count": 12,
        "created_at": datetime.now().isoformat(),
        "comments": []
    },
    {
        "id": 4,
        "title": "CLI Tool with argparse",
        "category": "DevOps/CI-CD",
        "prompt": """Erstelle ein Python CLI-Tool mit argparse:

REQUIREMENTS:
- Subcommands für verschiedene Operationen
- Required und Optional Arguments
- Type Validation
- Help Messages
- Config File Support (optional)

FEATURES:
- Verbose/Debug Modes
- Dry-Run Option
- Output Format (JSON, YAML, Table)
- Exit Codes (0=success, 1=error)

ERROR HANDLING:
- Argument Validation
- User-friendly Error Messages
- Logging statt Print

QUALITY:
- Type Hints
- Docstrings
- No hardcoded paths
- Environment-agnostic""",
        "author": "Daniel Jährling",
        "tags": ["python", "cli", "argparse", "automation"],
        "rating": 4.2,
        "votes": 4,
        "usage_count": 15,
        "created_at": datetime.now().isoformat(),
        "comments": []
    },
    {
        "id": 5,
        "title": "Refactoring: Extract Method",
        "category": "Refactoring",
        "prompt": """Refactore die gegebene Funktion durch Extract Method:

GOALS:
- Reduziere Komplexität (max 10 Zeilen pro Funktion)
- Single Responsibility Principle
- Verbessere Lesbarkeit
- Erhöhe Testbarkeit

APPROACH:
- Identifiziere logische Blöcke
- Extrahiere in separate Funktionen
- Aussagekräftige Namen
- Type Hints hinzufügen
- Docstrings für neue Funktionen

PRESERVE:
- Funktionalität (keine Behavior-Änderung)
- Bestehende Tests (sollten weiter funktionieren)
- Public API

IMPROVE:
- Error Handling
- Edge Cases
- Performance (wenn möglich)""",
        "author": "Daniel Jährling",
        "tags": ["refactoring", "clean-code", "maintainability"],
        "rating": 4.6,
        "votes": 3,
        "usage_count": 7,
        "created_at": datetime.now().isoformat(),
        "comments": []
    }
]

def seed_prompts():
    """Seed initial prompts"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(SEED_PROMPTS, f, indent=2, ensure_ascii=False)
    print(f"✅ Seeded {len(SEED_PROMPTS)} prompts to {DATA_FILE}")

if __name__ == "__main__":
    seed_prompts()
