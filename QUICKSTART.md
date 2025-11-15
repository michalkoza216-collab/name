# Quick Start Guide

Get started with the Product Variant Renaming Tool in 5 minutes.

## Prerequisites

- Python 3.8 or higher installed
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your API Key

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

Or copy the example file and edit it:

```bash
cp .env.example .env
# Then edit .env and add your API key
```

### 3. Test with Sample Data

Run the tool with the provided sample CSV:

```bash
python variant_renamer.py examples/sample_products.csv
```

### 4. Use with Your Own Data

Export your products from Shopify:
1. In Shopify Admin, go to **Products**
2. Click **Export**
3. Choose "Plain CSV file"
4. Download the file

Then run the tool with your CSV:

```bash
python variant_renamer.py path/to/your/shopify-export.csv
```

## What Happens Next

1. **Analysis**: The tool analyzes each variant using AI
2. **Review**: You see a comparison of current vs proposed names
3. **Approval**: Type "yes" to approve or "no" to cancel
4. **Export**: An `output_*.csv` file is created

## Import Back to Shopify

1. In Shopify Admin, go to **Products**
2. Click **Import**
3. Upload the `output_*.csv` file
4. Choose "Overwrite products with the same handle"
5. Click **Import products**

## Tips

- **Cost**: Each variant costs ~$0.001-0.03 depending on whether images are analyzed
- **Images**: Include variant images for better AI analysis
- **Backup**: Always backup your Shopify data before importing

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'openai'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

### API Key Error
```
OpenAI API key not found
```
**Solution**: Create a `.env` file with `OPENAI_API_KEY=your_key`

### CSV Format Error
```
Error loading CSV file
```
**Solution**: Ensure you're using a valid Shopify CSV export

## Need Help?

- Check the [main README](README.md) for detailed documentation
- Review [examples/README.md](examples/README.md) for sample files
- Open an issue on GitHub if you encounter problems
