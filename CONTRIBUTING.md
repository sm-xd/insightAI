# Contributing to InsightAI

## Development Setup

1. Fork and clone the repository
2. Create Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```

## Project Structure

```
insightAI/
├── backend/        # FastAPI server
├── frontend/       # React application
├── parsers/        # Code parsers
├── rag/           # RAG pipeline
└── tests/         # Test suite
```

## Code Style

- Python: Follow PEP 8
- JavaScript: Use ESLint config
- Run formatters before committing:
  ```bash
  # Python
  black .
  isort .
  
  # JavaScript
  npm run lint
  ```

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes

3. Run tests:
   ```bash
   python -m pytest
   cd frontend && npm test
   ```

4. Submit a pull request

## Adding Features

### New Parser
1. Add parser class in `parsers/languages/`
2. Register in `parser_registry.py`
3. Add tests in `tests/test_parsers.py`

### New Role
1. Add template in `rag/templates/`
2. Register in `role_manager.py`
3. Update frontend role selector

### New Plugin
1. Add plugin in `parsers/plugins/`
2. Register in plugin manager
3. Add tests in `tests/test_plugins.py`

### New Visualization
1. Add component in `frontend/src/components/visualizations/`
2. Register in visualization index
3. Update `InsightDisplay`

## Documentation

- Update relevant README files
- Document new features in docstrings
- Update API documentation

## Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review

## Release Process

1. Update version in:
   - Package files
   - Documentation
2. Create changelog entry
3. Create release tag
4. Build and publish