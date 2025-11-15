# Contributing to Product Variant Renaming Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/name.git
   cd name
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY to .env
   ```

## Development Setup

### Running Tests

Run the unit tests to ensure everything works:

```bash
python test_variant_renamer.py
```

All tests should pass before submitting a pull request.

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Testing Your Changes

1. Test with the sample CSV:
   ```bash
   python variant_renamer.py examples/sample_products.csv
   ```

2. Test with your own CSV files

3. Run the full test suite:
   ```bash
   python test_variant_renamer.py
   ```

## Types of Contributions

### Bug Reports

When reporting a bug, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

### Feature Requests

We welcome feature requests! Please:
- Describe the feature clearly
- Explain the use case
- Provide examples if possible

### Code Contributions

1. **Pick an issue** or create a new one describing what you want to work on
2. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation as needed
4. **Test your changes** thoroughly
5. **Commit your changes**:
   ```bash
   git commit -m "Add: brief description of changes"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if UI changes)

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts

### PR Description Should Include

- Summary of changes
- Motivation for changes
- Testing performed
- Screenshots (if applicable)
- Breaking changes (if any)

## Areas for Contribution

Here are some ways you can contribute:

### High Priority

- [ ] Add progress bar for batch processing
- [ ] Implement caching to avoid re-processing
- [ ] Add support for custom naming templates
- [ ] Improve error handling and recovery

### Medium Priority

- [ ] Add support for WooCommerce CSV format
- [ ] Create web interface (Flask/Streamlit)
- [ ] Add batch processing with parallel requests
- [ ] Implement dry-run mode

### Documentation

- [ ] Add more example CSV files
- [ ] Create video tutorial
- [ ] Add troubleshooting guide
- [ ] Translate documentation to other languages

### Testing

- [ ] Add integration tests
- [ ] Add test coverage reporting
- [ ] Test with large CSV files (1000+ variants)
- [ ] Add performance benchmarks

## Code Review Process

1. Maintainers will review your PR within a few days
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged in the changelog

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Project README (for significant contributions)
- Release notes

Thank you for contributing! 🎉
