#!/usr/bin/env python3
"""
Demo script showing how to use the Variant Renamer programmatically.
This is an alternative to the CLI interface for integration into other tools.
"""

from variant_renamer import VariantRenamer
import os
from dotenv import load_dotenv

def demo_basic_usage():
    """Demonstrate basic usage of the VariantRenamer."""
    
    load_dotenv()
    
    print("="*80)
    print("VARIANT RENAMER - PROGRAMMATIC USAGE DEMO")
    print("="*80)
    
    # Check if API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  Note: This is a demo showing the API structure.")
        print("For actual usage, set OPENAI_API_KEY in your .env file\n")
        return
    
    try:
        # Initialize the renamer
        print("\n1. Initializing VariantRenamer...")
        renamer = VariantRenamer()
        print("   ✓ Initialized")
        
        # Load CSV
        print("\n2. Loading CSV file...")
        csv_path = "examples/sample_products.csv"
        df = renamer.load_csv(csv_path)
        print(f"   ✓ Loaded {len(df)} rows")
        
        # Process variants
        print("\n3. Processing variants (this may take a moment)...")
        proposed_names = renamer.process_variants(df)
        print(f"   ✓ Analyzed {len(proposed_names)} variants")
        
        # Display proposals
        print("\n4. Displaying proposals...")
        renamer.display_proposals(df, proposed_names)
        
        # For demo purposes, we'll automatically approve
        print("\n5. Applying changes...")
        df_modified = renamer.apply_changes(df, proposed_names)
        print("   ✓ Changes applied")
        
        # Export
        print("\n6. Exporting to CSV...")
        output_path = "demo_output.csv"
        renamer.export_csv(df_modified, output_path)
        print(f"   ✓ Exported to {output_path}")
        
        print("\n" + "="*80)
        print("DEMO COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def demo_api_structure():
    """Show the API structure without actually calling OpenAI."""
    
    print("\n" + "="*80)
    print("VARIANT RENAMER - API STRUCTURE")
    print("="*80)
    
    print("""
The VariantRenamer class provides the following methods:

1. __init__(api_key=None)
   - Initialize with OpenAI API key
   - If not provided, loads from OPENAI_API_KEY environment variable

2. load_csv(csv_path: str) -> pd.DataFrame
   - Load a Shopify CSV file
   - Returns the loaded DataFrame

3. process_variants(df: pd.DataFrame) -> Dict[int, str]
   - Process all variants and generate proposed names
   - Returns dictionary mapping row indices to proposed names

4. analyze_variant_with_image(product_title, variant_title, image_url, variant_info)
   - Analyze a single variant using AI
   - Returns proposed name for the variant

5. display_proposals(df: pd.DataFrame, proposed_names: Dict[int, str])
   - Display proposed changes to the user

6. apply_changes(df: pd.DataFrame, proposed_names: Dict[int, str]) -> pd.DataFrame
   - Apply approved name changes to the DataFrame
   - Returns modified DataFrame

7. export_csv(df: pd.DataFrame, output_path: str)
   - Export DataFrame to CSV file

Example usage:
    
    from variant_renamer import VariantRenamer
    
    # Initialize
    renamer = VariantRenamer(api_key="your_key")
    
    # Load and process
    df = renamer.load_csv("products.csv")
    proposed = renamer.process_variants(df)
    
    # Review and apply
    renamer.display_proposals(df, proposed)
    df_modified = renamer.apply_changes(df, proposed)
    
    # Export
    renamer.export_csv(df_modified, "output.csv")
""")


if __name__ == "__main__":
    import sys
    
    if "--structure" in sys.argv:
        demo_api_structure()
    else:
        demo_basic_usage()
