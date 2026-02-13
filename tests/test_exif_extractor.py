
import unittest
import os
from datetime import datetime
from PIL import Image
from src.exif_extractor import get_image_date
import time

class TestExifExtractor(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_images"
        os.makedirs(self.test_dir, exist_ok=True)
        
    def tearDown(self):
        # Cleanup test images
        # Check if dir exists to avoid errors incase setup failed halfway
        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

    def test_file_modification_time_fallback(self):
        # Create a dummy image without EXIF
        path = os.path.join(self.test_dir, "no_exif.jpg")
        img = Image.new('RGB', (100, 100))
        img.save(path)
        
        extracted_date = get_image_date(path)
        file_time = datetime.fromtimestamp(os.path.getmtime(path))
        
        # Allow small difference due to processing execution time (e.g. 1 second)
        self.assertAlmostEqual(extracted_date.timestamp(), file_time.timestamp(), delta=1.0)

if __name__ == '__main__':
    unittest.main()
