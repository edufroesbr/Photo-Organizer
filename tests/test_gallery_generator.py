
import unittest
import os
import shutil
from pathlib import Path
from PIL import Image
from src.gallery_generator import GalleryGenerator

class TestGalleryGenerator(unittest.TestCase):
    def setUp(self):
        self.test_root = Path("test_gallery_root")
        self.output_dir = Path("test_gallery_out")
        
        self.test_root.mkdir(exist_ok=True)
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

        # Create dummy YYYY/MM/DD structure
        self.sub_dir = self.test_root / "2024" / "01" / "01"
        self.sub_dir.mkdir(parents=True, exist_ok=True)
        
        self.img_path = self.sub_dir / "test.jpg"
        img = Image.new('RGB', (400, 400), color='red')
        img.save(self.img_path)

    def tearDown(self):
        if self.test_root.exists():
            shutil.rmtree(self.test_root)
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_generate_simple(self):
        gen = GalleryGenerator(self.test_root, self.output_dir)
        gen.generate_simple()
        
        # Verify output structure
        self.assertTrue(self.output_dir.exists())
        self.assertTrue((self.output_dir / "index.html").exists())
        self.assertTrue((self.output_dir / "thumbnails").exists())
        
        # Verify index.html content
        with open(self.output_dir / "index.html", "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Organized Photos", content)
            self.assertIn("test.jpg", content)
            
        # Verify thumbnail creation
        # Thumb path relative to root: 2024/01/01/test.jpg
        thumb_path = self.output_dir / "thumbnails" / "2024" / "01" / "01" / "test.jpg"
        self.assertTrue(thumb_path.exists())
        
        # Verify thumb size
        with Image.open(thumb_path) as thumb:
            self.assertTrue(thumb.width <= 200)
            self.assertTrue(thumb.height <= 200)

if __name__ == '__main__':
    unittest.main()
