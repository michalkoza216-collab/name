# Project Overview: Product Variant Renaming Tool

## Summary

A complete Python-based tool for analyzing and renaming Shopify product variants using AI. The tool reads CSV files exported from Shopify, uses OpenAI's GPT-4 Vision API to analyze products and their images, proposes improved variant names, and exports the changes back to CSV format for re-import to Shopify.

## Project Status

✅ **COMPLETE AND READY FOR USE**

- All core features implemented
- 15 comprehensive tests passing
- Security vulnerabilities fixed
- Documentation complete
- Example files provided

## Key Features

1. **CSV Import/Export**: Full compatibility with Shopify CSV format
2. **AI-Powered Analysis**: Uses GPT-4 Vision for image-based variant analysis
3. **Interactive Workflow**: User approval before any changes are committed
4. **Flexible Usage**: Both CLI and programmatic API available
5. **Comprehensive Testing**: Unit and integration tests included
6. **Security**: All dependencies checked and vulnerabilities patched

## Project Structure

```
.
├── variant_renamer.py          # Main application (CLI + library)
├── setup.py                     # Package installation script
├── requirements.txt             # Python dependencies
├── test_variant_renamer.py      # Unit tests (9 tests)
├── test_integration.py          # Integration tests (6 tests)
├── demo.py                      # Demo script showing programmatic usage
│
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── CONTRIBUTING.md              # Contribution guidelines
├── PROJECT_OVERVIEW.md          # This file
├── LICENSE                      # MIT License
│
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
│
└── examples/
    ├── README.md                # Example documentation
    └── sample_products.csv      # Sample Shopify CSV file
```

## Usage Examples

### CLI Usage

```bash
# Basic usage
python variant_renamer.py examples/sample_products.csv

# With package installation
pip install -e .
variant-renamer examples/sample_products.csv
```

### Programmatic Usage

```python
from variant_renamer import VariantRenamer

# Initialize
renamer = VariantRenamer(api_key="your_key")

# Load and process
df = renamer.load_csv("products.csv")
proposed = renamer.process_variants(df)

# Review and apply
renamer.display_proposals(df, proposed)
df_modified = renamer.apply_changes(df, proposed)
renamer.export_csv(df_modified, "output.csv")
```

## Technical Details

### Dependencies

- **openai** (>=1.0.0): OpenAI API client for AI analysis
- **pandas** (>=2.0.0): CSV processing and data manipulation
- **pillow** (>=10.3.0): Image processing (security patched)
- **python-dotenv** (>=1.0.0): Environment variable management
- **requests** (>=2.31.0): HTTP requests for image downloads

### AI Models Used

- **GPT-4 Vision** (gpt-4o): For variants with images
- **GPT-4 Mini** (gpt-4o-mini): For text-only variants

### API Costs

Approximate costs per variant:
- With images: $0.01-0.03
- Without images: $0.001

For a catalog of 100 variants with images: ~$1-3

## Testing

### Run All Tests

```bash
# Run all tests
python -m unittest discover -s . -p "test_*.py" -v

# Run specific test suites
python test_variant_renamer.py      # Unit tests
python test_integration.py          # Integration tests
```

### Test Coverage

- ✅ CSV loading and parsing
- ✅ API integration (mocked)
- ✅ Variant processing workflow
- ✅ Name proposal generation
- ✅ CSV export functionality
- ✅ Error handling
- ✅ Data preservation
- ✅ Empty variant handling

## Security

### Vulnerabilities Fixed

- **Pillow**: Updated from 10.0.0 to 10.3.0
  - Fixed buffer overflow vulnerability
  - Fixed bundled libwebp vulnerability

### Security Scans

- ✅ GitHub Advisory Database: No vulnerabilities
- ✅ CodeQL Analysis: No alerts

### Best Practices

- API keys loaded from environment variables
- No secrets committed to repository
- Input validation on CSV files
- Safe file operations with proper error handling

## Documentation

1. **README.md**: Comprehensive user documentation
2. **QUICKSTART.md**: 5-minute getting started guide
3. **CONTRIBUTING.md**: Guidelines for contributors
4. **examples/README.md**: Example file documentation
5. **This file**: Technical overview

## Installation Methods

### Method 1: Package Installation (Recommended)

```bash
git clone https://github.com/michalkoza216-collab/name.git
cd name
pip install -e .
variant-renamer path/to/products.csv
```

### Method 2: Direct Script Usage

```bash
git clone https://github.com/michalkoza216-collab/name.git
cd name
pip install -r requirements.txt
python variant_renamer.py path/to/products.csv
```

## Configuration

### Required

- `OPENAI_API_KEY`: Your OpenAI API key

### Setup

```bash
# Copy example file
cp .env.example .env

# Edit and add your key
echo "OPENAI_API_KEY=sk-..." > .env
```

## Workflow

1. **Export from Shopify**: Products → Export → Plain CSV
2. **Run Tool**: `variant-renamer products.csv`
3. **Review Proposals**: Check AI-generated variant names
4. **Approve/Reject**: Type "yes" to approve
5. **Import to Shopify**: Products → Import → Upload `output_*.csv`

## Future Enhancements

Potential areas for contribution:

- [ ] Progress bar for batch processing
- [ ] Caching to avoid re-processing unchanged variants
- [ ] Custom naming templates and rules
- [ ] Support for other e-commerce platforms (WooCommerce, etc.)
- [ ] Web interface (Flask/Streamlit)
- [ ] Parallel processing for faster batch operations
- [ ] More detailed logging and reporting
- [ ] Dry-run mode to preview changes without API calls

## License

MIT License - See LICENSE file for details

## Support

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Check README.md and QUICKSTART.md
- **Examples**: See examples/ directory

## Authors

Product Variant Renaming Tool Contributors

---

**Last Updated**: 2025-11-15
**Version**: 1.0.0
**Status**: Production Ready
