# Contributing to OffStar

We welcome contributions to the OffStar Autonomous Agent project! This document outlines how to contribute effectively.

## 🎯 Ways to Contribute

### 1. Plugin Development
- Create new plugins for specific domains (NFT, GameFi, AI, etc.)
- Enhance existing plugins with additional features
- Improve plugin performance and reliability

### 2. Core Features
- Enhance the autonomous engine
- Improve task scheduling and optimization
- Add new communication protocols
- Strengthen security measures

### 3. IO.NET Integration
- Improve P2P communication
- Optimize distributed task execution
- Add new resource discovery mechanisms
- Enhance fault tolerance

### 4. Documentation
- Improve code documentation
- Add tutorials and guides
- Create architectural diagrams
- Write plugin development guides

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps
```bash
# Clone the repository
git clone https://github.com/protechtimenow/offstar-autonomous-agent.git
cd offstar-autonomous-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# Run tests
pytest

# Run examples
python examples/basic_usage.py
```

## 📝 Plugin Development

### Creating a New Plugin

1. **Create plugin file**: `offstar/plugins/your_plugin.py`

2. **Implement the base interface**:
```python
from .base import OffStarPlugin

class YourPlugin(OffStarPlugin):
    def __init__(self):
        super().__init__("your_plugin", "1.0.0")
    
    async def execute(self, task):
        # Your implementation here
        return {"status": "success", "result": result}
    
    async def get_capabilities(self):
        return ["capability1", "capability2"]
```

3. **Register in `__init__.py`**:
```python
from .your_plugin import YourPlugin
```

4. **Add tests**: `tests/test_your_plugin.py`

5. **Update documentation**: Add your plugin to README.md

### Plugin Guidelines

- **Error Handling**: Always use try/catch blocks
- **Health Monitoring**: Use `_log_error()` and `_update_metrics()`
- **Async Operations**: Use async/await for all I/O
- **Documentation**: Document all public methods
- **Testing**: Include comprehensive test coverage

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=offstar

# Run async tests only
pytest -m asyncio
```

### Test Structure
```
tests/
├── test_core.py           # Core functionality tests
├── test_plugins.py        # Plugin system tests
├── plugins/
│   ├── test_defi.py      # DeFi plugin tests
│   └── test_base.py      # Base plugin tests
└── conftest.py           # Pytest configuration
```

## 📖 Code Style

### Python Style Guide
- Follow PEP 8
- Use Black for formatting
- Use type hints
- Maximum line length: 88 characters

### Formatting
```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy offstar/
```

### Documentation Style
- Use Google-style docstrings
- Include type hints in signatures
- Document all public APIs
- Add examples where helpful

## 🚀 Submission Process

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Implement** your changes with tests
4. **Format** code using Black
5. **Test** thoroughly
6. **Commit** with clear messages
7. **Push** to your fork
8. **Create** a Pull Request

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
- `feat(plugins): add NFT analytics plugin`
- `fix(core): resolve task queue memory leak`
- `docs(readme): update installation instructions`

### Review Process

1. **Automated Checks**: All tests and style checks must pass
2. **Code Review**: Maintainers will review your code
3. **Discussion**: Address feedback and make necessary changes
4. **Approval**: Maintainer approval required for merge

## 🏗️ Architecture Guidelines

### Plugin Architecture
- Keep plugins focused and modular
- Minimize dependencies between plugins
- Use the event system for plugin communication
- Implement proper cleanup in shutdown

### Performance Considerations
- Use async/await for all I/O operations
- Implement caching where appropriate
- Monitor memory usage
- Optimize for concurrent execution

### Security Best Practices
- Validate all inputs
- Use secure communication channels
- Implement proper authentication
- Follow principle of least privilege

## 🎁 Recognition

Contributors will be:
- Listed in the CONTRIBUTORS.md file
- Mentioned in release notes for significant contributions
- Invited to join the core contributors team for outstanding work

## 📞 Communication

### Getting Help
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: Join our community (link in README)

### Reporting Issues
When reporting issues, include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## 📜 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to OffStar! Together we're building the future of autonomous AI agents. 🤖✨