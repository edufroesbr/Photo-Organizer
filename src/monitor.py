
import time
import sys
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.deduplicator import Deduplicator
from src.organizer import organize_file

class ImageHandler(FileSystemEventHandler):
    def __init__(self, destination_root, quarantine_dir):
        self.destination_root = destination_root
        self.deduplicator = Deduplicator(quarantine_dir=quarantine_dir)
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Simple extension check
        if file_path.suffix.lower() not in self.supported_extensions:
            return

        # Wait a brief moment for file write to complete (debounce)
        # In production this might need robust retries or check if file is locked
        time.sleep(1) 
        
        self.process_new_file(file_path)

    def process_new_file(self, file_path):
        logging.info(f"Processing new file: {file_path}")
        
        try:
            # 1. Deduplication
            # Deduplicator moves file if duplicate, so check existence after
            status = self.deduplicator.process_file(file_path)
            
            if status == "duplicate":
                logging.info(f"Detected duplicate: {file_path} -> Quarantine")
                return
            
            # 2. Organization (if unique and still exists)
            if file_path.exists():
                new_path = organize_file(file_path, self.destination_root, move=True)
                if new_path:
                    logging.info(f"Organized: {file_path} -> {new_path}")
                    
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")

def start_monitoring(source_dir, destination_root, quarantine_dir):
    event_handler = ImageHandler(destination_root, quarantine_dir)
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()
    logging.info(f"Started monitoring {source_dir}")
    logging.info(f"Destination: {destination_root}")
    logging.info(f"Quarantine: {quarantine_dir}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <source_dir> [destination_dir] [quarantine_dir]")
        sys.exit(1)
        
    source = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else "OrganizedPhotos"
    quar = sys.argv[3] if len(sys.argv) > 3 else "Quarantine"
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
                        
    start_monitoring(source, dest, quar)
