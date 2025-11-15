# Example Files

This directory contains sample CSV files for testing the Product Variant Renaming Tool.

## Files

### sample_products.csv
A complete Shopify product export with multiple products and variants. This file demonstrates:
- Products with multiple color and size variants
- Full Shopify CSV format with all columns
- Variant images for AI analysis

### Testing the Tool

To test with the sample file:

```bash
# Make sure you're in the repository root
cd /home/runner/work/name/name

# Run the tool with the sample file
python variant_renamer.py examples/sample_products.csv
```

**Note**: This requires a valid OpenAI API key in your `.env` file.

## Expected Behavior

When you run the tool with `sample_products.csv`, it will:

1. Load 12 product variants (6 t-shirts, 6 hoodies)
2. Analyze each variant considering:
   - Product type (T-Shirt vs Hoodie)
   - Color (Navy Blue, Charcoal Gray, Black, Heather Gray)
   - Size (Small, Medium, Large)
3. Propose improved variant names such as:
   - "Navy Blue / Small" → "Deep Navy / S"
   - "Charcoal Gray / Large" → "Graphite / L"
   - "Black / Medium" → "Classic Black / M"

## Creating Your Own Test Files

To create your own test CSV:

1. Export products from Shopify (Products → Export)
2. Ensure the CSV includes these key columns:
   - `Handle`: Product identifier
   - `Title`: Product name
   - `Option1 Name` and `Option1 Value`: First variant option
   - `Option2 Name` and `Option2 Value`: Second variant option
   - `Variant Image`: URL to variant image (optional but recommended)
   - `Variant SKU`: Stock keeping unit
   - `Variant Price`: Price

3. Save the file and run:
   ```bash
   python variant_renamer.py path/to/your/file.csv
   ```

## Minimal Example

Here's a minimal CSV structure that works:

```csv
Handle,Title,Option1 Name,Option1 Value,Variant Image
shirt-001,Test Shirt,Color,Red,https://example.com/image.jpg
shirt-001,Test Shirt,Color,Blue,https://example.com/image2.jpg
```

This minimal format is sufficient for testing, though the tool works best with complete Shopify exports.
