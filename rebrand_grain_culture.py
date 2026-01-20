import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/grainculture.store"
NEW_LOGO_PATH = "assets/RiceRoyal.png"
NEW_BRAND_NAME = "Rice Royal"
NEW_URL = "www.riceroyal.com"
NEW_EMAIL = "support@riceroyal.com"
NEW_ADDRESS = "IV-1/48, Gopinath Bazzar, Delhi Cantonment, New Delhi – 110010"

REPLACEMENTS = {
    # Text/Names
    r"Grain Culture": NEW_BRAND_NAME,
    r"Warangal Rice Stores": NEW_BRAND_NAME,
    r"Warangal": "New Delhi", # Location replacement if generic
    
    # URL/Email
    r"www\.grainculture\.store": NEW_URL,
    r"grainculture\.store": "riceroyal.com",
    r"graincultureofficial@gmail\.com": NEW_EMAIL,
    
    # Logos (Specific file names found in index.html)
    r"assets/logo_180044headerlogo_66504974321298_header_logo_0341\.png": NEW_LOGO_PATH,
    r"assets/new_logo_44_68044518063869_footer_logo_5030\.jpg": NEW_LOGO_PATH,
    
    # CDN Logo links (data-src)
    r"https://cdn\.shopaccino\.com/edible-smart/images/logo-180044headerlogo-66504974321298_header_logo\.png\?v=651\?v=1": NEW_LOGO_PATH,
    r"https://cdn\.shopaccino\.com/edible-smart/images/new-logo-44-68044518063869_footer_logo\.jpg\?v=651": NEW_LOGO_PATH,
    
    # Socials (Generic fix if any)
    r"graincultureofficial": "riceroyal",
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Address injection/Replacement logic
        # If we find the contact block or footer address placeholder, we can try to be smart.
        # But for now, let's trust the text replacements.
        # If "New Delhi" replacement happened on "Warangal", that covers some ground.
        
            
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
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
