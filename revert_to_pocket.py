import os
import re
import shutil

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/shantis.in"
IMAGES_SRC_DIR = "/Users/vijaykeshvala/Documents/scraped_data/images"
NEW_LOGO_FILENAME = "Pocket_Eat.png"
SOURCE_LOGO_PATH = os.path.join(IMAGES_SRC_DIR, "Pocket Eat.png")
TARGET_IMG_DIR = os.path.join(BASE_DIR, "assets")
TARGET_LOGO_PATH = os.path.join(TARGET_IMG_DIR, NEW_LOGO_FILENAME)

REPLACEMENTS = {
    # Name
    r"Kalpana Masala": "PocketEat",
    r"KalpanaMasala": "PocketEat",
    
    # URL
    r"kalpanamasala\.com": "pocketeat.com",
    r"www\.kalpanamasala\.com": "www.pocketeat.com",
    r"kalpanamasalafoods": "PocketEatfoods",
    r"kalpanamasalafood": "PocketEatfood",
    
    # Email
    r"feedback@kalpanamasala\.com": "manager@pocketeat.com",
    
    # Address
    r"Survey No\. 79-28B, Office No\. 104, I Floor, Kundan Heritage, Old Mumbai-Pune Highway, Bopodi, Pune – 411020, Maharashtra": "Bhaskar Tower, Ground Floor, Plot No.-13, Kharvelnagar, Bhubaneswar – 751001, Odisha",
    r"Pune, Maharashtra": "Bhubaneswar, Odisha",
}

def setup_assets():
    if os.path.exists(SOURCE_LOGO_PATH):
        if not os.path.exists(TARGET_IMG_DIR):
             os.makedirs(TARGET_IMG_DIR)
        shutil.copy2(SOURCE_LOGO_PATH, TARGET_LOGO_PATH)
        print(f"Copied logo to: {TARGET_LOGO_PATH}")

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        
        # 1. Logo Replacements
        # Replace Kalpana_Masala.png
        new_content = re.sub(r'src="assets/Kalpana_Masala\.png"', f'src="assets/{NEW_LOGO_FILENAME}"', new_content, flags=re.IGNORECASE)
        
        # 2. General Text Replacements
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
        print(f"Base Directory not found: {BASE_DIR}")
        return

    setup_assets()
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
