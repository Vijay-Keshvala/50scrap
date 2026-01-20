import os
import re
import shutil

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/shantis.in"
IMAGES_SRC_DIR = "/Users/vijaykeshvala/Documents/scraped_data/images"
NEW_LOGO_FILENAME = "Pocket_Eat.png"
SOURCE_LOGO_PATH = os.path.join(IMAGES_SRC_DIR, "Pocket Eat.png")
TARGET_IMG_DIR = os.path.join(BASE_DIR, "assets") # Based on previous inspect, it uses assets/
TARGET_LOGO_PATH = os.path.join(TARGET_IMG_DIR, NEW_LOGO_FILENAME)

REPLACEMENTS = {
    # Name
    r"Shanti's": "PocketEat",
    r"Shanti’s": "PocketEat",
    r"Shanti 's": "PocketEat",
    r"Shantis": "PocketEat",
    
    # URL
    r"shantis\.in": "pocketeat.com",
    r"www\.shantis\.in": "www.pocketeat.com",
    r"shantis\.com": "pocketeat.com", 
    r"www\.shantis\.com": "www.pocketeat.com",
    r"shantifood": "pocketeat",
    
    # Emails
    r"info@shantis\.com": "manager@pocketeat.com",
    r"info@shantis\.in": "manager@pocketeat.com",
    r"customercare@shantis\.in": "manager@pocketeat.com",
    
    # Address
    r"Bhavnagar Road, Bhagyalaxmi Ind\. Estate, B/H\. Mahesh Timber, Rajkot-360003": "Bhaskar Tower, Ground Floor, Plot No.-13, Kharvelnagar, Bhubaneswar – 751001, Odisha",
    r"Rajkot, Gujarat": "Bhubaneswar, Odisha",
    
    # Taglines/Descriptions specific to Shantis
    r"Serving Taste, Tradition, and Trust since 1984": "Serving Taste, Tradition, and Trust",
}

def setup_assets():
    # Fix missing img directory
    if not os.path.exists(TARGET_IMG_DIR):
        os.makedirs(TARGET_IMG_DIR)
    
    # Copy Logo
    if os.path.exists(SOURCE_LOGO_PATH):
        shutil.copy2(SOURCE_LOGO_PATH, TARGET_LOGO_PATH)
        print(f"Copied logo to: {TARGET_LOGO_PATH}")
    else:
        print(f"Warning: Source logo not found at {SOURCE_LOGO_PATH}")

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        
        # 1. Logo Replacements
        # Replace existing logo src with new logo
        # Based on index.html: <img src="assets/logo_5925.png" alt="logo">
        new_content = re.sub(r'src="assets/logo_[^"]+\.png"', f'src="assets/{NEW_LOGO_FILENAME}"', new_content, flags=re.IGNORECASE)
        # Also handle footer or other logos if they follow similar pattern or explicit filename if known.
        # But user said "do not remove existing images", so only target the main logo if possible.
        # Let's target specific logo filenames if we find more, but for now the regex above targets the main one which seems to be randomly numbered? 
        # Actually in index.html it was logo_5925.png. Let's be safer and replace specific known logo files if we can, or strict context.
        # But since I need to do this across all files, and the filenames might vary (scraped), I'll try to target the logo by context or just replace the known one if it's constant, 
        # OR replace "logo" alt text images? 
        # Safer: Replace exact known logo references if consistent, or regex matching typical logo patterns.
        # Given scraped nature, "logo_.*.png" might be common for the logo.
        
        # 2. General Text Replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            
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
