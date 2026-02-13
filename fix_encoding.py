
import sys

def fix_encoding(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # The content seems to be UTF-8 bytes interpreted as Latin-1 (Windows-1252)
        # So we encode back to latin-1 to get the original bytes, then decode as utf-8
        try:
            fixed_content = content.encode('latin1').decode('utf-8')
        except UnicodeError:
            # Fallback: manually replace common mojibake if strict decoding fails
            print("Strict decoding failed, attempting manual replacement")
            replacements = {
                'Ã§': 'ç', 'Ã£': 'ã', 'Ãµ': 'õ', 'Ã¡': 'á', 'Ã©': 'é', 
                'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú', 'Ã¢': 'â', 'Ãª': 'ê', 
                'Ã´': 'ô', 'Ã ': 'à', 'Ã': 'à' # Context dependent, but best guess
            }
            fixed_content = content
            for k, v in replacements.items():
                fixed_content = fixed_content.replace(k, v)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Successfully fixed encoding for {file_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fix_encoding(sys.argv[1])
    else:
        print("Usage: python fix_encoding.py <file_path>")
