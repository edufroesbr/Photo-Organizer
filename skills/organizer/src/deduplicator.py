
import hashlib
import os
import shutil
from pathlib import Path

def get_file_hash(file_path, block_size=65536):
    """
    Calculates the MD5 hash of a file.
    Uses chunking to handle large files efficiently.
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

class Deduplicator:
    def __init__(self, quarantine_dir="Quarantine"):
        self.seen_hashes = set()
        self.quarantine_dir = Path(quarantine_dir)
        
    def process_file(self, file_path):
        """
        Checks if file is a duplicate based on hash.
        If duplicate, moves to quarantine.
        If not, records hash and leaves file alone.
        Returns: 'duplicate' or 'unique'
        """
        file_path = Path(file_path)
        if not file_path.exists():
            return "skipped"
            
        file_hash = get_file_hash(file_path)
        
        if file_hash in self.seen_hashes:
            self._quarantine_file(file_path)
            return "duplicate"
        else:
            self.seen_hashes.add(file_hash)
            return "unique"
            
    def _quarantine_file(self, file_path):
        """
        Moves file to quarantine directory.
        """
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        target_path = self.quarantine_dir / file_path.name
        
        # Handle collision in quarantine too
        counter = 1
        stem = file_path.stem
        suffix = file_path.suffix
        while target_path.exists():
            target_path = self.quarantine_dir / f"{stem}_{counter}{suffix}"
            counter += 1
            
        shutil.move(str(file_path), str(target_path))

    def scan_directory(self, directory):
        """
        Scans a directory and processes all files.
        """
        directory = Path(directory)
        results = {"unique": 0, "duplicate": 0}
        
        # Walk effectively to process all files recursively? 
        # The prompt implies we might process incoming files, but scanning existing is also good.
        for root, _, files in os.walk(directory):
            # Skip quarantine itself if it is inside the scanned directory
            if self.quarantine_dir.resolve().is_relative_to(Path(root).resolve()):
               continue

            for file in files:
                file_path = Path(root) / file
                # Skip quarantine dir check again just in case relative path logic is tricky
                if self.quarantine_dir.name in file_path.parts:
                    continue
                    
                status = self.process_file(file_path)
                if status in results:
                    results[status] += 1
        return results
