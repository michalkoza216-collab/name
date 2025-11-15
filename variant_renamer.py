#!/usr/bin/env python3
"""
Product Variant Renaming Tool for Shopify CSV Files
This tool analyzes product variants using AI and proposes new names based on
the general product information and variant images.
"""

import os
import sys
import pandas as pd
import requests
from pathlib import Path
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()


class VariantRenamer:
    """Main class for renaming product variants using AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the VariantRenamer with OpenAI API key.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to load from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
                "or provide it as an argument."
            )
        self.client = OpenAI(api_key=self.api_key)
        self.original_data = None
        self.proposed_names = {}
        
    def load_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Load a Shopify CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            DataFrame containing the CSV data
        """
        try:
            df = pd.read_csv(csv_path)
            self.original_data = df.copy()
            print(f"✓ Loaded CSV file with {len(df)} rows")
            return df
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")
    
    def analyze_variant_with_image(
        self, 
        product_title: str,
        variant_title: str,
        image_url: Optional[str],
        variant_info: Dict
    ) -> str:
        """
        Analyze a variant using AI vision capabilities.
        
        Args:
            product_title: Title of the main product
            variant_title: Current variant title
            image_url: URL or path to the variant image
            variant_info: Additional variant information (color, size, etc.)
            
        Returns:
            Proposed new variant name
        """
        # Prepare the prompt
        variant_details = ", ".join([f"{k}: {v}" for k, v in variant_info.items() if pd.notna(v)])
        
        prompt = f"""You are an e-commerce product naming expert. Analyze this product variant and suggest a clear, descriptive name.

Product: {product_title}
Current Variant Name: {variant_title}
Variant Details: {variant_details}

Please suggest a better, more descriptive variant name that:
1. Is clear and customer-friendly
2. Highlights key distinguishing features
3. Follows e-commerce best practices
4. Is concise (2-5 words)

Respond with ONLY the suggested variant name, nothing else."""

        try:
            # If we have an image, use vision API
            if image_url and image_url.strip():
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url if image_url.startswith('http') else f"data:image/jpeg;base64,{self._encode_image(image_url)}"
                                }
                            }
                        ]
                    }
                ]
                
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=50
                )
            else:
                # Use text-only API if no image
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50
                )
            
            suggested_name = response.choices[0].message.content.strip()
            # Remove quotes if present
            suggested_name = suggested_name.strip('"\'')
            return suggested_name
            
        except Exception as e:
            print(f"Warning: Error analyzing variant: {e}")
            return variant_title  # Return original if analysis fails
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode local image to base64 for API submission.
        
        Args:
            image_path: Path to the local image
            
        Returns:
            Base64 encoded image string
        """
        import base64
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def process_variants(self, df: pd.DataFrame) -> Dict[int, str]:
        """
        Process all variants in the dataframe and propose new names.
        
        Args:
            df: DataFrame containing product data
            
        Returns:
            Dictionary mapping row index to proposed name
        """
        proposed_names = {}
        
        # Identify relevant columns (Shopify CSV format)
        # Common columns: Handle, Title, Option1 Name, Option1 Value, Variant Image, etc.
        
        print("\n🔍 Analyzing variants...")
        
        for idx, row in df.iterrows():
            # Skip if this is a main product row without variant info
            if pd.isna(row.get('Option1 Value')):
                continue
            
            product_title = row.get('Title', '')
            
            # Build current variant title from options
            variant_parts = []
            for i in range(1, 4):  # Check Option1, Option2, Option3
                opt_val = row.get(f'Option{i} Value')
                if pd.notna(opt_val):
                    variant_parts.append(str(opt_val))
            
            current_variant_title = " / ".join(variant_parts) if variant_parts else "Default"
            
            # Gather variant info
            variant_info = {
                'SKU': row.get('Variant SKU'),
                'Price': row.get('Variant Price'),
                'Color': row.get('Option1 Value') if row.get('Option1 Name') == 'Color' else None,
                'Size': row.get('Option1 Value') if row.get('Option1 Name') == 'Size' else None,
            }
            
            # Get image URL
            image_url = row.get('Variant Image') or row.get('Image Src')
            
            print(f"\n  Analyzing: {product_title} - {current_variant_title}")
            
            # Analyze and get proposed name
            proposed_name = self.analyze_variant_with_image(
                product_title=product_title,
                variant_title=current_variant_title,
                image_url=image_url,
                variant_info=variant_info
            )
            
            proposed_names[idx] = proposed_name
            print(f"    Current: {current_variant_title}")
            print(f"    Proposed: {proposed_name}")
        
        self.proposed_names = proposed_names
        return proposed_names
    
    def display_proposals(self, df: pd.DataFrame, proposed_names: Dict[int, str]):
        """
        Display proposed name changes to the user.
        
        Args:
            df: DataFrame containing product data
            proposed_names: Dictionary of proposed names
        """
        print("\n" + "="*80)
        print("📋 PROPOSED VARIANT NAME CHANGES")
        print("="*80)
        
        for idx, proposed_name in proposed_names.items():
            row = df.loc[idx]
            product_title = row.get('Title', '')
            
            # Build current variant title
            variant_parts = []
            for i in range(1, 4):
                opt_val = row.get(f'Option{i} Value')
                if pd.notna(opt_val):
                    variant_parts.append(str(opt_val))
            current_variant_title = " / ".join(variant_parts) if variant_parts else "Default"
            
            print(f"\nProduct: {product_title}")
            print(f"  Current:  {current_variant_title}")
            print(f"  Proposed: {proposed_name}")
    
    def apply_changes(self, df: pd.DataFrame, proposed_names: Dict[int, str]) -> pd.DataFrame:
        """
        Apply approved name changes to the dataframe.
        
        Args:
            df: DataFrame containing product data
            proposed_names: Dictionary of approved names
            
        Returns:
            Modified DataFrame with new variant names
        """
        df_modified = df.copy()
        
        for idx, new_name in proposed_names.items():
            # Split the new name into parts (assuming format like "Color / Size")
            parts = [p.strip() for p in new_name.split('/')]
            
            # Update Option values based on the new name
            # For simplicity, we'll update Option1 Value with the new name
            # In a real scenario, you might need more sophisticated parsing
            if len(parts) >= 1:
                df_modified.at[idx, 'Option1 Value'] = parts[0]
            if len(parts) >= 2:
                df_modified.at[idx, 'Option2 Value'] = parts[1]
            if len(parts) >= 3:
                df_modified.at[idx, 'Option3 Value'] = parts[2]
        
        return df_modified
    
    def export_csv(self, df: pd.DataFrame, output_path: str):
        """
        Export the modified dataframe to CSV.
        
        Args:
            df: DataFrame to export
            output_path: Path for the output CSV file
        """
        try:
            df.to_csv(output_path, index=False)
            print(f"\n✓ Exported modified CSV to: {output_path}")
        except Exception as e:
            raise Exception(f"Error exporting CSV: {e}")


def main():
    """Main CLI interface."""
    print("="*80)
    print("🏷️  PRODUCT VARIANT RENAMING TOOL")
    print("="*80)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key:")
        print("  OPENAI_API_KEY=your_api_key_here")
        print("\nOr set it as an environment variable:")
        print("  export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Get input CSV path
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = input("\n📁 Enter the path to your Shopify CSV file: ").strip()
    
    if not os.path.exists(csv_path):
        print(f"\n❌ Error: File not found: {csv_path}")
        sys.exit(1)
    
    try:
        # Initialize renamer
        renamer = VariantRenamer()
        
        # Load CSV
        df = renamer.load_csv(csv_path)
        
        # Process variants
        proposed_names = renamer.process_variants(df)
        
        if not proposed_names:
            print("\n⚠️  No variants found to process.")
            sys.exit(0)
        
        # Display proposals
        renamer.display_proposals(df, proposed_names)
        
        # Ask for approval
        print("\n" + "="*80)
        response = input("\n❓ Do you approve these changes? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            # Apply changes
            df_modified = renamer.apply_changes(df, proposed_names)
            
            # Generate output filename
            input_path = Path(csv_path)
            output_path = input_path.parent / f"output_{input_path.name}"
            
            # Export
            renamer.export_csv(df_modified, str(output_path))
            
            print("\n✅ Done! Your modified CSV is ready for Shopify import.")
        else:
            print("\n❌ Changes cancelled. No file was generated.")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
