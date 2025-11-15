#!/usr/bin/env python3
"""
Integration test for the Variant Renamer tool.
This test simulates the complete workflow without making actual API calls.
"""

import unittest
import os
import tempfile
import pandas as pd
from io import StringIO
from unittest.mock import Mock, patch, MagicMock
import variant_renamer


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Sample Shopify CSV
        self.csv_content = """Handle,Title,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Variant SKU,Variant Price,Variant Image
tshirt-001,Premium T-Shirt,Color,Red,Size,Small,TSH-RED-S,29.99,https://example.com/red-small.jpg
tshirt-001,Premium T-Shirt,Color,Red,Size,Medium,TSH-RED-M,29.99,https://example.com/red-medium.jpg
tshirt-001,Premium T-Shirt,Color,Blue,Size,Small,TSH-BLU-S,29.99,https://example.com/blue-small.jpg
tshirt-001,Premium T-Shirt,Color,Blue,Size,Medium,TSH-BLU-M,29.99,https://example.com/blue-medium.jpg
"""
        
        # Create input CSV file
        self.input_csv = os.path.join(self.test_dir, "input.csv")
        with open(self.input_csv, 'w') as f:
            f.write(self.csv_content)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('variant_renamer.OpenAI')
    def test_complete_workflow(self, mock_openai_class):
        """Test the complete workflow from CSV input to CSV output."""
        
        # Mock the OpenAI API responses
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Mock responses for each variant
        mock_responses = [
            "Crimson Red / S",
            "Crimson Red / M", 
            "Ocean Blue / S",
            "Ocean Blue / M"
        ]
        
        response_idx = [0]  # Use list to make it mutable in closure
        
        def create_mock_response(text):
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = text
            return mock_response
        
        def mock_create(*args, **kwargs):
            response = create_mock_response(mock_responses[response_idx[0]])
            response_idx[0] += 1
            return response
        
        mock_client.chat.completions.create = mock_create
        
        # Run the workflow
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        # Step 1: Load CSV
        df = renamer.load_csv(self.input_csv)
        self.assertEqual(len(df), 4)
        
        # Step 2: Process variants
        proposed_names = renamer.process_variants(df)
        self.assertEqual(len(proposed_names), 4)
        self.assertIn(0, proposed_names)
        self.assertIn(1, proposed_names)
        self.assertIn(2, proposed_names)
        self.assertIn(3, proposed_names)
        
        # Step 3: Apply changes
        df_modified = renamer.apply_changes(df, proposed_names)
        self.assertEqual(len(df_modified), 4)
        
        # Step 4: Export to CSV
        output_csv = os.path.join(self.test_dir, "output.csv")
        renamer.export_csv(df_modified, output_csv)
        
        # Verify output file exists and is valid
        self.assertTrue(os.path.exists(output_csv))
        df_output = pd.read_csv(output_csv)
        self.assertEqual(len(df_output), 4)
        
        # Verify changes were applied
        self.assertEqual(df_output.at[0, 'Option1 Value'], 'Crimson Red')
        self.assertEqual(df_output.at[2, 'Option1 Value'], 'Ocean Blue')
    
    @patch('variant_renamer.OpenAI')
    def test_error_handling_invalid_csv(self, mock_openai_class):
        """Test error handling with invalid CSV."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        # Try to load non-existent file
        with self.assertRaises(Exception):
            renamer.load_csv("/nonexistent/file.csv")
    
    @patch('variant_renamer.OpenAI')
    def test_empty_variants(self, mock_openai_class):
        """Test handling of CSV with no variants."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # CSV with only main product row, no variants
        csv_content = """Handle,Title,Option1 Name,Option1 Value
tshirt-001,Premium T-Shirt,,
"""
        csv_file = os.path.join(self.test_dir, "no_variants.csv")
        with open(csv_file, 'w') as f:
            f.write(csv_content)
        
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        df = renamer.load_csv(csv_file)
        proposed_names = renamer.process_variants(df)
        
        # Should return empty dict for no variants
        self.assertEqual(len(proposed_names), 0)
    
    @patch('variant_renamer.OpenAI')
    def test_preserves_other_columns(self, mock_openai_class):
        """Test that other columns are preserved during processing."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "New Name"
        mock_client.chat.completions.create.return_value = mock_response
        
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        df = renamer.load_csv(self.input_csv)
        
        # Verify all columns are present
        expected_columns = ['Handle', 'Title', 'Option1 Name', 'Option1 Value', 
                          'Option2 Name', 'Option2 Value', 'Variant SKU', 
                          'Variant Price', 'Variant Image']
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # Process and apply changes
        proposed_names = renamer.process_variants(df)
        df_modified = renamer.apply_changes(df, proposed_names)
        
        # Verify all columns still exist
        for col in expected_columns:
            self.assertIn(col, df_modified.columns)
        
        # Verify data in unchanged columns is preserved
        self.assertEqual(float(df_modified.at[0, 'Variant Price']), 29.99)
        self.assertEqual(df_modified.at[0, 'Variant SKU'], 'TSH-RED-S')


class TestAPIIntegration(unittest.TestCase):
    """Test API integration without making actual calls."""
    
    @patch('variant_renamer.OpenAI')
    def test_api_calls_with_images(self, mock_openai_class):
        """Test that API is called correctly with image URLs."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Vibrant Red"
        mock_client.chat.completions.create.return_value = mock_response
        
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        # Call with image URL
        result = renamer.analyze_variant_with_image(
            product_title="Test Product",
            variant_title="Red",
            image_url="https://example.com/image.jpg",
            variant_info={"Color": "Red"}
        )
        
        # Verify API was called
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify correct model was used for images
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args[1]['model'], 'gpt-4o')
        
        # Verify result
        self.assertEqual(result, "Vibrant Red")
    
    @patch('variant_renamer.OpenAI')
    def test_api_calls_without_images(self, mock_openai_class):
        """Test that API is called correctly without images."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Standard Red"
        mock_client.chat.completions.create.return_value = mock_response
        
        renamer = variant_renamer.VariantRenamer(api_key="test_key")
        
        # Call without image URL
        result = renamer.analyze_variant_with_image(
            product_title="Test Product",
            variant_title="Red",
            image_url=None,
            variant_info={"Color": "Red"}
        )
        
        # Verify API was called
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify correct model was used for text-only
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args[1]['model'], 'gpt-4o-mini')
        
        # Verify result
        self.assertEqual(result, "Standard Red")


if __name__ == '__main__':
    unittest.main(verbosity=2)
