import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/knayamfoods.com"

RESTORE_MAPPINGS = {
    # Restore hotlinked images/assets that were broken by domain replacement
    r"https://thepulseplate\.com/wp-content/": "https://knayamfoods.com/wp-content/",
    r"https://thepulseplate\.com/wp-includes/": "https://knayamfoods.com/wp-includes/",
    r"https://www\.thepulseplate\.com/wp-content/": "https://www.knayamfoods.com/wp-content/",
    r"https://www\.thepulseplate\.com/wp-includes/": "https://www.knayamfoods.com/wp-includes/",
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        for pattern, replacement in RESTORE_MAPPINGS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Restored assets in: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

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
