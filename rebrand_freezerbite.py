import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/maplesfood.com"
NEW_LOGO_PATH = "assets/FreezerBite.png"
OLD_LOGO_FILENAME = "Final-Logo-whitebg.png"
NEW_NAME = "Freezeer Bite"

REPLACEMENTS = {
    # Brand Name
    r"Maples Food Store": NEW_NAME,
    r"Maples Food": NEW_NAME,
    
    # URL/Email
    r"maplesfood\.com": "freezerbite.com",
    r"www\.maplesfood\.com": "www.freezerbite.com",
    r"feedback@maplesfood\.com": "feedback@freezerbite.com", # Hypothetical or if found
    
    # Address (Vadodara)
    # Found: Ground floor, Avishkar Complex, Near GEB Colony, Old Padra Road, Vadodara – 390015
    # Regex loosely matching the address to be safe
    r"Ground floor, Avishkar Complex, Near GEB Colony, Old Padra Road, Vadodara – 390015": 
    "89, 1st Floor, Phase 2, Machantala, Bankura – 722101, West Bengal",

    # Logo
    # Specific logo file in index.html: 
    # wp-content/uploads/2020/11/Final-Logo-whitebg.png
    # Replace the filename/path locally
    r"Final-Logo-whitebg\.png": "FreezerBite.png",
    r"Final_Logo_redbg_5944\.png": "FreezerBite.png",
}

def fix_logo_style(content):
    # Ensure logo looks good.
    # Matched pattern: <img ... src="...FreezerBite.png" ...>
    if "FreezerBite.png" in content:
        # Check if style is present, if not add max-height
        # The existing logo had width:150, height:71.
        # Let's try to set a reasonable max-height like 80px or 100px.
        if 'max-height' not in content:
             content = re.sub(
                 r'(src="[^"]*FreezerBite\.png"[^>]*?)>',
                 r'\1 style="max-height: 100px; width: auto;">',
                 content
             )
    return content

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Fix logo style
        new_content = fix_logo_style(new_content)
        
        # Specific Logo Asset path fix if it's pointing to old filename in a path
        if OLD_LOGO_FILENAME in new_content:
             new_content = new_content.replace(OLD_LOGO_FILENAME, "FreezerBite.png")
        if "Final_Logo_redbg_5944.png" in new_content:
             new_content = new_content.replace("Final_Logo_redbg_5944.png", "FreezerBite.png")

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".json")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
