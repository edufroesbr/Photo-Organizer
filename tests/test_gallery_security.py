
import unittest
import os
import shutil
from pathlib import Path
from src.gallery_generator import GalleryGenerator

class TestGallerySecurity(unittest.TestCase):
    def setUp(self):
        self.test_root = Path("test_gallery_sec_root")
        self.output_dir = Path("test_gallery_sec_out")
        
        self.test_root.mkdir(exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy file
        self.sub_dir = self.test_root / "2024" / "01" / "01"
        self.sub_dir.mkdir(parents=True, exist_ok=True)
        (self.sub_dir / "test.jpg").touch()

    def tearDown(self):
        if self.test_root.exists():
            shutil.rmtree(self.test_root)
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_html_contains_password_logic(self):
        gen = GalleryGenerator(self.test_root, self.output_dir)
        gen.generate_simple()
        
        index_path = self.output_dir / "index.html"
        self.assertTrue(index_path.exists())
        
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Check for overlay elements
            self.assertIn('id="login-overlay"', content)
            self.assertIn('id="password-input"', content)
            
            # Check for simple password logic
            self.assertIn('const CORRECT_PASSWORD = "admin";', content)
            self.assertNotIn("crypto.subtle", content)
            


if __name__ == '__main__':
    unittest.main()
