
import os
import shutil
from pathlib import Path
from PIL import Image

class GalleryGenerator:
    def __init__(self, root_dir, output_dir=None):
        self.root_dir = Path(root_dir)
        # If output_dir not specified, put gallery inside root_dir/gallery (risky if scanning recursively?)
        # Better: output_dir default to parallel folder
        self.output_dir = Path(output_dir) if output_dir else self.root_dir / "gallery"
        self.thumbnails_dir = self.output_dir / "thumbnails"
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}

    def generate(self):
        """
        Generates the static gallery.
        """
        if not self.root_dir.exists():
            print(f"Root dir {self.root_dir} does not exist.")
            return

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnails_dir.mkdir(parents=True, exist_ok=True)

        # 1. Collect images by date (Year/Month/Day structure)
        structure = self._scan_structure()
        
        # 2. Generate Thumbnails and individual pages
        self._process_images(structure)
        
        # 3. Generate Index HTML
        self._generate_index_html(structure)

    def _scan_structure(self):
        """
        Scans root_dir for YYYY/MM/DD structure.
        Returns dict: {year: {month: {day: [files]}}}
        """
        structure = {}
        for root, _, files in os.walk(self.root_dir):
            if Path(root) == self.output_dir or self.output_dir in Path(root).parents:
                continue # Skip gallery dir itself
                
            path = Path(root)
            # Check if path looks like .../YYYY/MM/DD
            # This is heuristic, but our organizer enforces it. 
            # We can also just collect all images and group them by folder name.
            
            image_files = [f for f in files if Path(f).suffix.lower() in self.supported_extensions]
            if not image_files:
                continue

            # We assume structure is relative to root_dir
            rel_path = path.relative_to(self.root_dir)
            parts = rel_path.parts
            
            # Simple aggregation by folder path
            current_level = structure
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            
            # Leaf is list of files
            current_level["__files__"] = sorted(image_files)
            
        return structure

    def _process_images(self, structure, current_path=Path(".")):
        """
        Walks the structure, generates thumbnails, and returns HTML snippet for this level.
        """
        # Recursive function not strictly needed if we just iterate files, 
        # but let's iterate to build pages.
        pass 
        # Actually doing a flat scan might be easier for a simple gallery logic:
        # Just walk, find images, verify/make thumb, add to list.
        
    def _generate_thumbnail(self, original_path):
        """
        Generates a thumbnail for the image.
        Returns relative path to thumbnail from gallery root.
        """
        rel_path = original_path.relative_to(self.root_dir)
        thumb_path = self.thumbnails_dir / rel_path
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not thumb_path.exists():
            try:
                img = Image.open(original_path)
                img.thumbnail((200, 200))
                img.save(thumb_path)
            except Exception as e:
                print(f"Failed to create thumbnail for {original_path}: {e}")
                return None
                
        return thumb_path.relative_to(self.output_dir)

    def generate_simple(self):
        """
        Simpler one-page gallery generation for Phase 1.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.thumbnails_dir.mkdir(parents=True, exist_ok=True)
        
        images = []
        for root, _, files in os.walk(self.root_dir):
            # Skip output dir
            if str(self.output_dir.resolve()) in str(Path(root).resolve()):
                continue
                
            for f in files:
                if Path(f).suffix.lower() in self.supported_extensions:
                    full_path = Path(root) / f
                    thumb_rel = self._generate_thumbnail(full_path)
                    if thumb_rel:
                        # Copy original logic? No, link to it. 
                        # To link to it, it needs to be accessible relative to html.
                        # If output_dir is parallel to organized folders, we can use ..
                        rel_original = os.path.relpath(full_path, self.output_dir)
                        images.append({
                            "thumb": thumb_rel,
                            "full": rel_original,
                            "name": f
                        })
        
        self._write_html(images)

    def _write_html(self, images):
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photo Gallery</title>
    <style>
        body { font-family: sans-serif; background: #222; color: #eee; margin: 0; padding: 20px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }
        .photo-card { background: #333; padding: 10px; border-radius: 8px; text-align: center; }
        .photo-card img { max-width: 100%; height: auto; border-radius: 4px; }
        .photo-card a { color: #fff; text-decoration: none; word-break: break-all; }
    </style>
</head>
<body>
    <h1>Organized Photos</h1>
    <div class="gallery">
"""
        for img in images:
            html_content += f"""
        <div class="photo-card">
            <a href="{img['full']}" target="_blank">
                <img src="{img['thumb']}" alt="{img['name']}" loading="lazy">
                <br>
                <span>{img['name']}</span>
            </a>
        </div>
"""
        html_content += """
    </div>
</body>
</html>
"""
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python gallery_generator.py <root_dir> [output_dir]")
    else:
        root = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else None
        gen = GalleryGenerator(root, out)
        gen.generate_simple()
