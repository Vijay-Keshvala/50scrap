import os
import re
import shutil

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/camywafer.com"
IMAGES_SRC_DIR = "/Users/vijaykeshvala/Documents/scraped_data/images"
NEW_LOGO_FILENAME = "Fuel_Snax.png"
SOURCE_LOGO_PATH = os.path.join(IMAGES_SRC_DIR, "Fuel Snax.png")
TARGET_IMG_DIR = os.path.join(BASE_DIR, "img")
TARGET_LOGO_PATH = os.path.join(TARGET_IMG_DIR, NEW_LOGO_FILENAME)

REPLACEMENTS = {
    # Name
    r"Camy Wafers": "Fuel Snax",
    r"CAMY Wafers": "Fuel Snax",
    r"CAMY": "Fuel Snax", # Be careful? camy-logo is handled separately?
    
    # URL
    r"camywafer\.com": "fuelsnax.com",
    r"www\.camywafer\.com": "www.fuelsnax.com",
    
    # Emails
    r"info@camywafer\.com": "management@fuelsnax.com",
    r"Order@camywafer\.com": "management@fuelsnax.com",
    r"camy@camywafer\.com": "management@fuelsnax.com",
    
    # Address
    r"Old Anjirwadi Number 1 Lane, Anjeer Wadi, Thakkar Estate, Mazgaon, Mumbai, Maharashtra 400010": "Police Station 18, Malviya Market, Grand Trunk Road, Rasal Ganj, Aligarh – 202001, Uttar Pradesh",
    
    # Copyright
    r"Copyright © CAMY Wafers.*All rights reserved\.": "Copyright © Fuel Snax. 2025. All rights reserved.",
}

def setup_assets():
    # Fix missing img directory
    if not os.path.exists(TARGET_IMG_DIR):
        os.makedirs(TARGET_IMG_DIR)
        print(f"Created directory: {TARGET_IMG_DIR}")
    
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
        
        # 1. Logo Replacements specific to img/ paths
        # Replace camy-logo.jpg with Fuel_Snax.png
        new_content = re.sub(r'img/camy-logo\.jpg', f'img/{NEW_LOGO_FILENAME}', new_content, flags=re.IGNORECASE)
        
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
            if file.lower().endswith((".html", ".htm", ".js", ".css")): # processing css/js too for refs
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
