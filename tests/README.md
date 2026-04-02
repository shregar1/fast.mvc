# Tests

## Overview

The **`tests`** package contains automated tests for the FastX application:

- **`tests/dev/`** - **Your application tests** (runs by default)
- **`tests/framework/`** - FastX framework tests (excluded by default)

## Test Structure

```text
tests/
├── conftest.py              # Shared fixtures, markers, hooks
├── dev/                     # Your application tests (run by default)
│   ├── __init__.py
│   └── test_example.py      # Example/template tests
├── framework/               # FastX framework tests (excluded by default)
│   ├── test_abstractions/   # Framework abstraction tests
│   ├── test_constants/      # Framework constants tests
│   ├── test_controllers/    # Framework controller tests
│   ├── test_core/           # Framework core tests
│   ├── test_dependencies/   # Framework dependency tests
│   ├── test_dtos/           # Framework DTO tests
│   ├── test_services/       # Framework service tests
│   ├── test_utilities/      # Framework utility tests
│   └── test_*.py            # Additional framework tests
└── utils/                   # Test utilities/helpers
```

## Running Tests

### Run developer tests only (default)
```bash
# Only runs tests in tests/dev/ and tests/* (not tests/framework/)
pytest

# Or explicitly
pytest tests/dev

# Or using make
make test
make test-dev
```

### Run framework tests only
```bash
# Only runs tests in tests/framework/
pytest tests/framework

# Or using make
make test-framework
```

### Run all tests (developer + framework)
```bash
# Runs all tests
pytest tests/ tests/framework

# Or using make
make test-all
```

### Other useful commands
```bash
# Run with coverage
make test-coverage

# Run with verbose output
make test-verbose

# Run specific test file
pytest tests/dev/test_your_feature.py

# Run specific test
pytest tests/dev/test_your_feature.py::TestYourClass::test_your_method
```

## Writing Tests

### For Application Features

Add your tests to `tests/dev/`:

```python
# tests/dev/test_your_feature.py
from __future__ import annotations

import pytest


class TestYourFeature:
    """Tests for your feature."""

    def test_something_works(self):
        """Test that something works."""
        from services.your_service import YourService
        service = YourService()
        result = service.do_something()
        assert result == expected_value
```

### Test Markers

Use pytest markers to categorize tests:

```python
import pytest


@pytest.mark.unit
def test_unit_test():
    pass


@pytest.mark.integration
def test_integration_test():
    pass


@pytest.mark.slow
def test_slow_test():
    pass
```

Run marked tests selectively:
```bash
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Exclude slow tests
```

## Configuration

- **`pytest.ini`** - Pytest configuration (markers, defaults, ignore patterns)
- **`pyproject.toml`** - Coverage settings
- **`Makefile`** - Convenient test commands (`make test`, `make test-all`, etc.)

## Best Practices

1. **Place tests in `tests/dev/`** for your application code
2. **Use descriptive test names** that explain what is being tested
3. **Mark slow or integration tests** for selective runs
4. **Use fixtures** from `conftest.py` for shared setup
5. **Run `pytest` before committing** to catch issues early
6. **Keep tests isolated** - each test should be independent
