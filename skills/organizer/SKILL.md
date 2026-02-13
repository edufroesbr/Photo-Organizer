
---
name: Photo Organizer
description: Organizes photos by date, removes duplicates, and generates a gallery.
---

# Photo Organizer Skill

This skill provides a suite of tools to manage and organize photo collections.

## Capabilities

1.  **Date-based Organization**: Moves images into a folder structure `YYYY/MM/DD` based on EXIF data.
2.  **Deduplication**: Identifies duplicate files using MD5 hashing and moves them to a `Quarantine` folder.
3.  **Monitoring**: Watches a directory for new files and automatically organizes them.
4.  **Gallery Generation**: Creates a static HTML gallery with thumbnails for optimized viewing.

## Usage

### 1. Organize Existing Photos

To organize a directory of existing photos into a destination:

```python
from skills.organizer.src.organizer import process_directory

process_directory(source_dir="raw_photos", destination_root="organized_photos")
```

### 2. Remove Duplicates

To scan a directory for duplicates:

```python
from skills.organizer.src.deduplicator import Deduplicator

deduper = Deduplicator(quarantine_dir="Quarantine")
deduper.scan_directory("organized_photos")
```

### 3. Start Watchdog Monitor

To keep a folder organized in real-time:

```bash
python skills/organizer/src/monitor.py <source_dir> <destination_dir> <quarantine_dir>
```

### 4. Generate Web Gallery

To create a browsable gallery of the organized photos:

```python
from skills.organizer.src.gallery_generator import GalleryGenerator

gen = GalleryGenerator(root_dir="organized_photos", output_dir="gallery_output")
gen.generate_simple()
```

## Dependencies

- Pillow
- watchdog

## Structure

- `src/organizer.py`: Core file moving logic.
- `src/exif_extractor.py`: Helper to read dates from images.
- `src/deduplicator.py`: Logic for finding duplicates.
- `src/monitor.py`: Real-time directory watching service.
- `src/gallery_generator.py`: HTML gallery creator.
