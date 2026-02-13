
import unittest
import os
import shutil
import time
import threading
from pathlib import Path
from src.monitor import ImageHandler
from watchdog.events import FileCreatedEvent
from PIL import Image

class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.src_dir = Path("test_monitor_src")
        self.dest_dir = Path("test_monitor_dest")
        self.quar_dir = Path("test_monitor_quar")
        
        self.src_dir.mkdir(exist_ok=True)
        self.dest_dir.mkdir(exist_ok=True)
        self.quar_dir.mkdir(exist_ok=True)
        
        self.handler = ImageHandler(str(self.dest_dir), str(self.quar_dir))

    def tearDown(self):
        if self.src_dir.exists():
            shutil.rmtree(self.src_dir)
        if self.dest_dir.exists():
            shutil.rmtree(self.dest_dir)
        if self.quar_dir.exists():
            shutil.rmtree(self.quar_dir)

    def create_dummy_image(self, name):
        p = self.src_dir / name
        img = Image.new('RGB', (100, 100))
        img.save(p)
        return p

    def test_process_new_file_unique(self):
        # Simulate creating a file
        img_path = self.create_dummy_image("unique.jpg")
        
        # Manually trigger processing logic (bypassing Observer wait times for unit test speed)
        self.handler.process_new_file(img_path)
        
        # Should be moved to dest
        # We don't know exact date folder without mocking time, 
        # but source should be gone and dest should have something
        self.assertFalse(img_path.exists())
        
        # Find file in dest
        found = list(self.dest_dir.glob("**/*.jpg"))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "unique.jpg")

    def test_process_new_file_duplicate(self):
        # 1. Create and process first file
        img_path1 = self.create_dummy_image("original.jpg")
        self.handler.process_new_file(img_path1)
        
        # 2. Create duplicate file (same content)
        img_path2 = self.create_dummy_image("dupe.jpg")
        
        # We need to ensure deduplicator has seen the hash.
        # Since we use a fresh handler in setUp, and Deduplicator is init inside ImageHandler,
        # the state is preserved if we reuse self.handler.
        
        self.handler.process_new_file(img_path2)
        
        # Should be moved to Quarantine
        self.assertFalse(img_path2.exists())
        
        quarantined = list(self.quar_dir.glob("*"))
        self.assertEqual(len(quarantined), 1)
        self.assertEqual(quarantined[0].name, "dupe.jpg")

if __name__ == '__main__':
    unittest.main()
