#!/usr/bin/env python3
"""
Simple tests for the Variant Renamer tool.
These tests validate basic functionality without requiring an API key.
"""

import unittest
import pandas as pd
import os
import sys
from io import StringIO
from unittest.mock import Mock, patch, MagicMock

# Import the module
import variant_renamer


class TestVariantRenamer(unittest.TestCase):
    """Test cases for VariantRenamer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample CSV data
        self.sample_csv_data = """Handle,Title,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Variant SKU,Variant Price,Variant Image
tshirt-001,Classic T-Shirt,Color,Red,Size,Small,TSH-RED-S,29.99,https://example.com/red.jpg
tshirt-001,Classic T-Shirt,Color,Blue,Size,Medium,TSH-BLU-M,29.99,https://example.com/blue.jpg
"""
        
        self.sample_df = pd.read_csv(StringIO(self.sample_csv_data))
    
    @patch('variant_renamer.OpenAI')
    def test_initialization_with_api_key(self, mock_openai):
        """Test VariantRenamer initialization with API key."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        self.assertEqual(renamer.api_key, "test_key")
        mock_openai.assert_called_once_with(api_key="test_key")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'env_test_key'})
    @patch('variant_renamer.OpenAI')
    def test_initialization_from_env(self, mock_openai):
        """Test VariantRenamer initialization from environment variable."""
        renamer = variant_renamer.VariantRenamer()
        self.assertEqual(renamer.api_key, "env_test_key")
    
    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                variant_renamer.VariantRenamer()
    
    @patch('variant_renamer.OpenAI')
    def test_load_csv(self, mock_openai):
        """Test CSV loading functionality."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        # Create a temporary CSV file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write(self.sample_csv_data)
            temp_csv = f.name
        
        try:
            df = renamer.load_csv(temp_csv)
            self.assertEqual(len(df), 2)
            self.assertIn('Title', df.columns)
            self.assertIn('Option1 Value', df.columns)
        finally:
            os.unlink(temp_csv)
    
    @patch('variant_renamer.OpenAI')
    def test_load_nonexistent_csv(self, mock_openai):
        """Test loading a non-existent CSV file."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        with self.assertRaises(Exception):
            renamer.load_csv('/nonexistent/file.csv')
    
    @patch('variant_renamer.OpenAI')
    def test_apply_changes(self, mock_openai):
        """Test applying name changes to dataframe."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        df = self.sample_df.copy()
        proposed_names = {
            0: "Crimson Red / S",
            1: "Ocean Blue / M"
        }
        
        df_modified = renamer.apply_changes(df, proposed_names)
        
        # Check that modifications were made
        self.assertEqual(df_modified.at[0, 'Option1 Value'], 'Crimson Red')
        self.assertEqual(df_modified.at[1, 'Option1 Value'], 'Ocean Blue')
    
    @patch('variant_renamer.OpenAI')
    def test_export_csv(self, mock_openai):
        """Test CSV export functionality."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            temp_output = f.name
        
        try:
            renamer.export_csv(self.sample_df, temp_output)
            self.assertTrue(os.path.exists(temp_output))
            
            # Verify the exported file is valid CSV
            df_exported = pd.read_csv(temp_output)
            self.assertEqual(len(df_exported), 2)
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)
    
    @patch('variant_renamer.OpenAI')
    def test_display_proposals(self, mock_openai):
        """Test display of proposed changes."""
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        proposed_names = {
            0: "Bright Red / Small",
            1: "Deep Blue / Medium"
        }
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            renamer.display_proposals(self.sample_df, proposed_names)
            output = captured_output.getvalue()
            
            self.assertIn("PROPOSED VARIANT NAME CHANGES", output)
            self.assertIn("Bright Red / Small", output)
            self.assertIn("Deep Blue / Medium", output)
        finally:
            sys.stdout = sys.__stdout__


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_module_imports(self):
        """Test that all required modules can be imported."""
        import pandas
        import requests
        from PIL import Image
        from dotenv import load_dotenv
        
        # If we get here, all imports succeeded
        self.assertTrue(True)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
