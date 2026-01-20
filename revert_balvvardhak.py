import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com"

# Reverse mappings
REPLACEMENTS = {
    # Brand Name
    r"Kiddi Well": "Balvvardhak",
    
    # URL/Email
    r"kiddiwell\.com": "balvvardhak.com",
    r"www\.kiddiwell\.com": "www.balvvardhak.com",
    r"city@kiddiwell\.com": "info@balvvardhak.com", # Defaulting to info@ since we lost the distinction
    # Address
    r"12/25, Block E, 2nd Floor, Flat No. 204, KNC Road, Barasat, 24 Parganas, West Bengal, 700124": 
    "Warje Jakat Naka, Pune, Maharashtra",

    # Logo
    r"Kiddiwell\.png": "Balvvardhak_logo_0504.webp",
}

FILES_TO_REMOVE = [
    os.path.join(BASE_DIR, "assets/Kiddiwell.png"),
    os.path.join(BASE_DIR, "assets/balvvardhak-banner-header.webp"),
    os.path.join(BASE_DIR, "assets/balvvardhak-header-mobile.jpg"),
]

def revert_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # 1. Remove logo styling
        # style="max-height: 85px; width: auto;" src="assets/Kiddiwell.png"
        # We want to remove the style and revert the src.
        # The replacement loop below will handle the filename.
        # We just need to strip the specific style if it exists.
        
        if 'style="max-height: 85px; width: auto;"' in new_content:
             new_content = new_content.replace(' style="max-height: 85px; width: auto;"', "") # Try with space
             new_content = new_content.replace('style="max-height: 85px; width: auto;"', "") # Try without space

        # 2. Apply reverse replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Reverted: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    # Revert Content
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".json")): 
                filepath = os.path.join(root, file)
                revert_file(filepath)

    # Remove added files
    for file_path in FILES_TO_REMOVE:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    main()
