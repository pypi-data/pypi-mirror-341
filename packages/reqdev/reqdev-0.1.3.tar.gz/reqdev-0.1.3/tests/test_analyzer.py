import os
import tempfile
import unittest
from pathlib import Path

from requirements.requirements.analyzer import ImportAnalyzer
from requirements.requirements.mapping import get_package_name, is_std_lib

class TestAnalyzer(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = Path(self.temp_dir.name)
        
        # Create some test Python files
        self.create_test_files()
        
    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()
        
    def create_test_files(self):
        # Create a Python file with some imports
        file1 = self.project_path / "test1.py"
        with open(file1, "w") as f:
            f.write("""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import sys
            """)
            
        # Create another Python file with different imports
        file2 = self.project_path / "test2.py"
        with open(file2, "w") as f:
            f.write("""
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import json
            """)
            
    def test_find_python_files(self):
        analyzer = ImportAnalyzer(project_path=self.project_path)
        files = analyzer.find_python_files()
        
        # Should find exactly 2 Python files
        self.assertEqual(len(files), 2)
        
    def test_extract_imports(self):
        analyzer = ImportAnalyzer(project_path=self.project_path)
        
        # Test extracting imports from the first file
        file1 = os.path.join(self.project_path, "test1.py")
        imports = analyzer.extract_imports_from_file(file1)
        
        # Check if the imports are correctly extracted
        self.assertIn("numpy", imports)
        self.assertIn("pandas", imports)
        self.assertIn("sklearn", imports)
        self.assertIn("os", imports)
        self.assertIn("sys", imports)
        
    def test_analyze(self):
        analyzer = ImportAnalyzer(project_path=self.project_path)
        imports = analyzer.analyze()
        
        # Should identify 6 non-standard library packages
        self.assertEqual(len(imports), 6)
        
        # Check if the packages are correctly identified
        self.assertIn("numpy", analyzer.packages)
        self.assertIn("pandas", analyzer.packages)
        self.assertIn("scikit-learn", analyzer.packages)
        self.assertIn("matplotlib", analyzer.packages)
        self.assertIn("opencv-python", analyzer.packages)
        self.assertIn("pillow", analyzer.packages)
        
        # Standard library modules should not be included
        self.assertNotIn("os", analyzer.packages)
        self.assertNotIn("sys", analyzer.packages)
        self.assertNotIn("json", analyzer.packages)
        
    def test_generate_requirements(self):
        analyzer = ImportAnalyzer(project_path=self.project_path)
        output_file = os.path.join(self.project_path, "requirements.txt")
        
        # Generate requirements without versions to avoid test flakiness
        result = analyzer.generate_requirements(output_file=output_file, with_versions=False)
        
        # Should succeed
        self.assertTrue(result)
        
        # The file should exist
        self.assertTrue(os.path.exists(output_file))
        
        # Read the file contents
        with open(output_file, "r") as f:
            content = f.read()
            
        # Check if the packages are included
        self.assertIn("numpy", content)
        self.assertIn("pandas", content)
        self.assertIn("scikit-learn", content)
        self.assertIn("matplotlib", content)
        self.assertIn("opencv-python", content)
        self.assertIn("pillow", content)
        
class TestMapping(unittest.TestCase):
    
    def test_get_package_name(self):
        # Test direct mappings
        self.assertEqual(get_package_name("cv2"), "opencv-python")
        self.assertEqual(get_package_name("sklearn"), "scikit-learn")
        self.assertEqual(get_package_name("PIL"), "pillow")
        
        # Test unknown import (should return the same name)
        self.assertEqual(get_package_name("unknown_module"), "unknown_module")
        
    def test_is_std_lib(self):
        # Test standard library modules
        self.assertTrue(is_std_lib("os"))
        self.assertTrue(is_std_lib("sys"))
        self.assertTrue(is_std_lib("json"))
        
        # Test non-standard library modules
        self.assertFalse(is_std_lib("numpy"))
        self.assertFalse(is_std_lib("pandas"))
        self.assertFalse(is_std_lib("sklearn"))

if __name__ == "__main__":
    unittest.main() 