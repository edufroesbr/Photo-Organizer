
import os
import shutil
from pathlib import Path
from src.exif_extractor import get_image_date

def organize_file(file_path, destination_root, move=True):
    """
    Organizes a single file into destination_root/YYYY/MM/DD/.
    Handles collisions by appending a counter.
    Returns the new path of the file.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")

    # Get date
    date = get_image_date(str(file_path))
    
    # Construct target directory
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    target_dir = Path(destination_root) / year / month / day
    
    # Create directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine target filename to avoid collisions
    original_name = file_path.name
    stem = file_path.stem
    suffix = file_path.suffix
    target_path = target_dir / original_name
    
    counter = 1
    while target_path.exists():
        # Check if it's the exact same file (optional optimization for future, 
        # but for now we assume we want to keep both if names collide but content might differ
        # logic for deduplication is in US-003)
        target_path = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1
        
    # Move or Copy logic
    try:
        if move:
            shutil.move(str(file_path), str(target_path))
        else:
            shutil.copy2(str(file_path), str(target_path))
    except OSError as e:
        print(f"Error moving file {file_path}: {e}")
        return None
        
    return str(target_path)

def process_directory(source_dir, destination_root):
    """
    Scans source_dir and organizes all supported files.
    """
    supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    source_path = Path(source_dir)
    
    for item in source_path.iterdir():
        if item.is_file() and item.suffix.lower() in supported_extensions:
            organize_file(item, destination_root)

