
import unittest
import os
import shutil
from pathlib import Path
from src.organizer import organize_file
from src.exif_extractor import get_image_date
import time
from PIL import Image

class TestOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_src = Path("test_organizer_src")
        self.test_dest = Path("test_organizer_dest")
        
        self.test_src.mkdir(exist_ok=True)
        self.test_dest.mkdir(exist_ok=True)
        
    def tearDown(self):
        if self.test_src.exists():
            shutil.rmtree(self.test_src)
        if self.test_dest.exists():
            shutil.rmtree(self.test_dest)

    def create_dummy_image(self, name):
        p = self.test_src / name
        img = Image.new('RGB', (100, 100))
        img.save(p)
        return p

    def test_organize_file_basic(self):
        # Create image
        img_path = self.create_dummy_image("photo.jpg")
        
        # Determine expected date (modification time since no EXIF)
        expected_date = get_image_date(str(img_path))
        year = expected_date.strftime("%Y")
        month = expected_date.strftime("%m")
        day = expected_date.strftime("%d")
        
        # Run organizer - copy mode for testing to keep source intact if needed, 
        # but function defaults to move. Let's use default move.
        new_path = organize_file(img_path, self.test_dest)
        
        expected_path = self.test_dest / year / month / day / "photo.jpg"
        
        self.assertTrue(os.path.exists(new_path))
        self.assertEqual(Path(new_path).resolve(), expected_path.resolve())
        self.assertFalse(img_path.exists()) # Should be moved

    def test_collision_handling(self):
        # Create two images with same name (simulating coming from different folders ideally, 
        # but here we'll move one, recreate it, and move again)
        
        # 1. Move first file
        img_path1 = self.create_dummy_image("duplicate.jpg")
        # Ensure distinct mtime if system is too fast? 
        # Actually organize_file calculates path based on date.
        # If we create them quickly, they go to same YYYY/MM/DD folder.
        
        new_path1 = organize_file(img_path1, self.test_dest)
        
        # 2. Recreate file with same name
        img_path2 = self.create_dummy_image("duplicate.jpg")
        
        new_path2 = organize_file(img_path2, self.test_dest)
        
        # Check both exist
        self.assertTrue(os.path.exists(new_path1))
        self.assertTrue(os.path.exists(new_path2))
        self.assertNotEqual(new_path1, new_path2)
        
        # Start ends with duplicate_1.jpg
        self.assertTrue(new_path2.endswith("duplicate_1.jpg"))

if __name__ == '__main__':
    unittest.main()
