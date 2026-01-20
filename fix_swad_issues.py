import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/swayampaak.com"
NEW_LOGO_PATH = "assets/Swad_Pickles.png"

FIXES = {
    # Fix broken logo paths where branding replaced 'swayampaak' inside filenames
    r"assets/Swad Pickle_logo_e1711807510428_5424\.png": NEW_LOGO_PATH,
    r"assets/Swad Pickle_logo.*\.png": NEW_LOGO_PATH,
    r"wp-content/uploads/2024/02/Swad Pickle-logo-e1711807510428\.png": NEW_LOGO_PATH,
    r"wp-content/uploads/2024/02/Swad Pickle-logo.*\.png": NEW_LOGO_PATH,
    
    # Fix Email
    r"Swad Pickle@gmail\.com": "info@swadpickle.com",
    r"Swad Pickle@swadpickle\.com": "info@swadpickle.com",
    
    # Fix URL Spaces/Typos
    r"New Delhii": "New Delhi", # Fix Nagpuri -> New Delhii
    r"author/Swad Pickle/": "author/swadpickle/",
    
    # Fix broken logo alt/title if needed
    r"Swad Pickle-logo": "Swad Pickles Logo",
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
            print(f"Fixed issues in: {filepath}")

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".php")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
