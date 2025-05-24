# Tests

Test suite for InsightAI components.

## Structure

```
tests/
├── test_parsers.py    # Tests for code parsers
├── test_plugins.py    # Tests for analysis plugins
└── test_rag.py        # Tests for RAG pipeline
```

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_parsers.py

# Run with coverage
python -m pytest --cov=.

# Run with verbose output
python -m pytest -v
```

## Writing Tests

### Parser Tests
Test new parsers in `test_parsers.py`:
```python
def test_my_parser():
    parser = MyParser()
    result = parser.parse("test.ext")
    assert result.language == "mylang"
```

### Plugin Tests
Test plugins in `test_plugins.py`:
```python
def test_my_plugin():
    plugin = MyPlugin()
    result = plugin.analyze(content)
    assert "metrics" in result
```

### RAG Tests
Test RAG components in `test_rag.py`:
```python
def test_role_template():
    manager = RoleManager()
    template = manager.get_template("role_id")
    assert template["name"] == "Role Name"
```

## Test Data

Sample files in `tests/data/`:
- Python files
- JavaScript files
- Test repositories

## Coverage Reports

Generate coverage report:
```bash
coverage run -m pytest
coverage report
coverage html  # Generate HTML report
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Push to main branch
- Nightly builds