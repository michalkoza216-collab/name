# Product Variant Renaming Tool for Shopify

A Python-based tool that uses AI to analyze product variants and propose better, more descriptive names based on product information and images.

## Features

- 📊 **CSV Import/Export**: Compatible with Shopify CSV format
- 🤖 **AI-Powered Analysis**: Uses OpenAI's GPT-4 Vision to analyze product images
- 🎯 **Smart Naming**: Generates clear, customer-friendly variant names
- ✅ **Interactive Approval**: Review and approve changes before exporting
- 🔄 **Shopify-Ready**: Exports CSV files that can be directly imported to Shopify

## Requirements

- Python 3.8 or higher
- OpenAI API key (for AI analysis)

## Installation

### Option 1: Install as a Package (Recommended)

```bash
# Clone the repository
git clone https://github.com/michalkoza216-collab/name.git
cd name

# Install the package
pip install -e .
```

After installation, you can run the tool from anywhere:
```bash
variant-renamer path/to/your/products.csv
```

### Option 2: Install Dependencies Only

```bash
# Clone the repository
git clone https://github.com/michalkoza216-collab/name.git
cd name

# Install dependencies
pip install -r requirements.txt
```

Then run the tool with:
```bash
python variant_renamer.py path/to/your/products.csv
```

3. Set up your OpenAI API key:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Run the tool with your Shopify CSV file:

```bash
python variant_renamer.py path/to/your/products.csv
```

### Interactive Mode

If you don't provide a file path as an argument, the tool will prompt you:

```bash
python variant_renamer.py
```

### Workflow

1. **Load CSV**: The tool loads your Shopify product CSV file
2. **AI Analysis**: Each variant is analyzed using AI, considering:
   - Product title and description
   - Variant attributes (color, size, etc.)
   - Product images (if available)
3. **Review Proposals**: You'll see the current and proposed names side by side
4. **Approve/Reject**: Type "yes" to approve or "no" to cancel
5. **Export**: If approved, an `output_*.csv` file is generated for Shopify import

## CSV Format

The tool works with standard Shopify CSV exports, which typically include columns like:

- `Handle`: Product identifier
- `Title`: Product title
- `Option1 Name`, `Option1 Value`: First variant option (e.g., Color: Red)
- `Option2 Name`, `Option2 Value`: Second variant option (e.g., Size: Large)
- `Option3 Name`, `Option3 Value`: Third variant option
- `Variant SKU`: SKU for the variant
- `Variant Price`: Price
- `Image Src`: Product image URL
- `Variant Image`: Variant-specific image URL

## Example

### Input CSV
```csv
Handle,Title,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Variant Image
tshirt-001,Classic T-Shirt,Color,Red,Size,Large,https://example.com/red-large.jpg
tshirt-001,Classic T-Shirt,Color,Blue,Size,Medium,https://example.com/blue-medium.jpg
```

### Output
```
🔍 Analyzing variants...

  Analyzing: Classic T-Shirt - Red / Large
    Current: Red / Large
    Proposed: Bold Red / Large

  Analyzing: Classic T-Shirt - Blue / Medium
    Current: Blue / Medium
    Proposed: Ocean Blue / Medium

❓ Do you approve these changes? (yes/no): yes

✓ Exported modified CSV to: output_products.csv
```

## Sample CSV Files

Example CSV files are provided in the `examples/` directory:

- `sample_products.csv`: Example Shopify product CSV
- `sample_output.csv`: Example output after processing

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Advanced Options

You can modify the AI behavior by editing the prompt in `variant_renamer.py`:
- Adjust naming conventions
- Change the level of detail
- Add industry-specific terminology

## Troubleshooting

### "OpenAI API key not found"
Make sure you've created a `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

### "Error loading CSV file"
Ensure your CSV file:
- Is in valid CSV format
- Uses UTF-8 encoding
- Follows Shopify's CSV structure

### Rate Limits
If you have many variants, you may hit OpenAI API rate limits. The tool will show warnings if this happens.

## Cost Considerations

This tool uses OpenAI's API, which incurs costs:
- **GPT-4 Vision** (with images): ~$0.01-0.03 per variant
- **GPT-4 Mini** (text only): ~$0.001 per variant

For a product catalog with 100 variants, expect costs of $1-3.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the maintainers

## Roadmap

- [ ] Support for bulk processing with progress bars
- [ ] Caching to avoid re-analyzing unchanged variants
- [ ] Custom naming templates
- [ ] Support for other e-commerce platforms
- [ ] Web interface for non-technical users