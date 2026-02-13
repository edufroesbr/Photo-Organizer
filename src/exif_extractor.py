
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import os

def get_image_date(image_path):
    """
    Extracts the date from an image file.
    Priority:
    1. EXIF DateTimeOriginal
    2. EXIF DateTime
    3. File modification time
    """
    try:
        with Image.open(image_path) as image:
            exif_data = image.getexif()
            
            # 36867 is DateTimeOriginal
            date_time_original = exif_data.get(36867)
            if date_time_original:
                return datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")
                
            # 306 is DateTime
            date_time = exif_data.get(306)
            if date_time:
                return datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
            
    except Exception as e:
        # Log error if needed, but for now just fall through to file time
        pass
        
    # Fallback to file modification time
    timestamp = os.path.getmtime(image_path)
    return datetime.fromtimestamp(timestamp)

if __name__ == "__main__":
    # Test with a dummy file if needed
    pass
