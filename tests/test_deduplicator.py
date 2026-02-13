
import unittest
import os
import shutil
import hashlib
from pathlib import Path
from src.deduplicator import Deduplicator, get_file_hash

class TestDeduplicator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_dedup_data")
        self.quarantine_dir = Path("test_quarantine")
        
        self.test_dir.mkdir(exist_ok=True)
        # Quarantine created by class usually, but good to clean up
        
        self.deduplicator = Deduplicator(quarantine_dir=str(self.quarantine_dir))
        
    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if self.quarantine_dir.exists():
            shutil.rmtree(self.quarantine_dir)

    def create_file(self, name, content):
        p = self.test_dir / name
        with open(p, "wb") as f:
            f.write(content)
        return p

    def test_hash_calculation(self):
        content = b"hello world"
        p = self.create_file("test.txt", content)
        expected_hash = hashlib.md5(content).hexdigest()
        self.assertEqual(get_file_hash(p), expected_hash)

    def test_duplicate_detection(self):
        content = b"duplicate content"
        
        # File 1
        f1 = self.create_file("file1.txt", content)
        status1 = self.deduplicator.process_file(f1)
        self.assertEqual(status1, "unique")
        self.assertTrue(f1.exists())
        
        # File 2 (Duplicate)
        f2 = self.create_file("file2.txt", content)
        status2 = self.deduplicator.process_file(f2)
        self.assertEqual(status2, "duplicate")
        self.assertFalse(f2.exists()) # Should be moved
        
        # Check quarantine
        quarantined_files = list(self.quarantine_dir.glob("*"))
        self.assertEqual(len(quarantined_files), 1)
        self.assertEqual(quarantined_files[0].name, "file2.txt")

    def test_unique_files(self):
        f1 = self.create_file("a.txt", b"content A")
        f2 = self.create_file("b.txt", b"content B")
        
        self.assertEqual(self.deduplicator.process_file(f1), "unique")
        self.assertEqual(self.deduplicator.process_file(f2), "unique")
        
        self.assertEqual(len(list(self.quarantine_dir.glob("*"))), 0)

if __name__ == '__main__':
    unittest.main()
