import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/knayamfoods.com"

# Coordinates for New Delhi Cantonment
NEW_COORDS_URL = "28.5947%2C+77.1205"

FIXES = {
    # Fix phone number artifact
    r', <a href="tel:919315412619"></a>': '',
    r', <a href="tel:919315412619"> </a>': '',
    
    # Fix Company Name capitalization/format
    r"The Pulse Plate PIONEER PRIVATE LIMITED": "The Pulse Plate Private Limited",
    
    # Fix Title Capitalization (specific cases)
    r"<title>thepulseplate": "<title>The Pulse Plate",
    r"title=\"thepulseplate": "title=\"The Pulse Plate",
    
    # Fix Map Coordinates in iframe
    r"28.42247335200344%2C\+77.55002695164202": NEW_COORDS_URL,
    
    # Attempt to fix specific text that might be lowercase
    r">thepulseplate<": ">The Pulse Plate<",
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in FIXES.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
