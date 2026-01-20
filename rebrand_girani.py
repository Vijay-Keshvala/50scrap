import os
import re
import shutil

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/girani.in"
IMAGES_SRC_DIR = "/Users/vijaykeshvala/Documents/scraped_data/images"
NEW_LOGO_FILENAME = "Kalpana_Masala.png"
SOURCE_LOGO_PATH = os.path.join(IMAGES_SRC_DIR, "Kalna Masala.png")
TARGET_IMG_DIR = os.path.join(BASE_DIR, "assets/images") # Girani uses assets/images
TARGET_LOGO_PATH = os.path.join(TARGET_IMG_DIR, NEW_LOGO_FILENAME)

# Create assets/images if it doesn't exist (it should, but just in case)
if not os.path.exists(TARGET_IMG_DIR):
    os.makedirs(TARGET_IMG_DIR)

REPLACEMENTS = {
    # Name
    r"Girani": "Kalpana Masala",
    r"Adhikruta Foods PVT\.LTD": "Kalpana Masala",
    r"Adhikruta Foods": "Kalpana Masala",
    
    # URL
    r"girani\.in": "kalpanamasala.com",
    r"www\.girani\.in": "www.kalpanamasala.com",
    r"girani_mill": "kalpanamasala", # social handles
    
    # Address/Location
    r"Bangalore": "Pune",
    r"Karnataka": "Maharashtra",
    
    # Email (if any found)
    r"feedback@girani\.in": "feedback@kalpanamasala.com",
    r"info@girani\.in": "feedback@kalpanamasala.com",
    
    # Address Replacements (if full address found)
    # I didn't see the full address in valid view, but I'll add the new one if generic address logic is needed.
    # For now, relying on textual replacements.
}

def setup_assets():
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
        # Identified potential logo files: Group 30386.png, logo.png
        new_content = re.sub(r'src=["\'].*/Group 30386\.png["\']', f'src="assets/images/{NEW_LOGO_FILENAME}"', new_content, flags=re.IGNORECASE)
        new_content = re.sub(r'href=["\'].*/Group 30386\.png["\']', f'href="assets/images/{NEW_LOGO_FILENAME}"', new_content, flags=re.IGNORECASE) # Favicon
        new_content = re.sub(r'src=["\'].*/logo\.png["\']', f'src="assets/images/{NEW_LOGO_FILENAME}"', new_content, flags=re.IGNORECASE)
        
        # 2. General Text Replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # 3. Add Contact Details if missing or generically place them?
        # The user provided: "Survey No. 79-28B..." and "feedback@kalpanamasala.com"
        # I will replace any specific placeholder or just rely on "Bangalore" -> "Pune" logic for now, 
        # but I should try to inject the address in the footer if possible.
        # Looking at lines 2246, there is copyright.
        # I'll look for "Bangalore" context specifically for address.
        
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
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".php")): # PHP files are likely HTML in scraped data
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
