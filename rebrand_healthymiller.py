import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/healthymiller.com"
NEW_LOGO_PATH = "assets/FlourFolk.png"
NEW_BRAND_NAME = "Flour Folk"
NEW_MKT_URL = "floufolk.com" # Display URL
NEW_MKT_URL_FULL = "www.floufolk.com"
NEW_EMAIL = "sales@floufolk.com"
NEW_ADDRESS = "Kanak Building, Ground Floor, 41 Jawaharlal Nehru Road, Opp. Jeevandeep Building, Kolkata – 700071"

# Old Address found in footer
OLD_ADDRESS_START = r"Shop No\.35, Ground Floor, Baani Square"
# We'll use a broader regex for address to catch the full block if possible, or just strict replace.
# The footer text was: Shop No.35, Ground Floor, Baani Square, Pocket C, South City II, Sector 50, Gurugram, Haryana 122018
OLD_ADDRESS_REGEX = r"Shop No\.35, Ground Floor, Baani Square, Pocket C, South City II, Sector 50, Gurugram, Haryana 122018"

REPLACEMENTS = {
    # Text/Names
    r"Healthy Miller": NEW_BRAND_NAME,
    r"healthy miller": "flour folk", # generic
    
    # URL/Email
    # Protect cdn/shop links. Replace healthymiller.com ONLY if NOT followed by /cdn or /shop or /shopifycloud
    # This might be tricky with regex order.
    # We want to replace 'healthymiller.com' with 'floufolk.com' generally.
    r"healthymiller\.com(?!/(cdn|shop|shopifycloud|checkouts))": NEW_MKT_URL,
    
    # Email (specifics first)
    r"care@healthymiller\.com": NEW_EMAIL,
    r"info@healthymiller\.com": NEW_EMAIL,
    r"support@healthymiller\.com": NEW_EMAIL,
    
    # Address
    OLD_ADDRESS_REGEX: NEW_ADDRESS,
    
    # Phone (if any specific one found, e.g. 9205658080)
    # The prompt didn't specify a new phone. We will leave it or replace if we had one.
    # Leaving it alone to avoid removing valid contact info if we don't have replacement.
    
    # Logos (Specific file names found)
    # Header
    r"assets/WhatsApp_Image_2024_10_24_at_14_20_09__1__jpeg_removebg_preview_1_6004\.png": NEW_LOGO_PATH,
    # Footer
    r"assets/white_logo_1_1_7212\.png": NEW_LOGO_PATH,
}

# Regex to clean up logo dimensions after replacement
# We want to replace the width/height attributes on the logo IMG tags to allow the new square logo to fit.
# Tag 1 (Header): <img src="assets/FlourFolk.png" ... width="140" height="68.333..." ...>
# Tag 2 (Footer): <img src="assets/FlourFolk.png" ... width="260" height="245">

def fix_logo_dimensions(content):
    # Header Logo Fix: Remove hardcoded width/height, add style
    # Look for the specific new logo path and adjacent attributes.
    # Pattern: <img src="assets/FlourFolk.png" ... width="..." height="...">
    
    # It's easier to verify visually, but let's try to patch it.
    # Replaces width="140" height="68..." with style="max-height: 80px; width: auto;"
    # Note: The attributes might be in any order. 
    
    # Header specific context: class="header__heading-logo
    # We can replace the class or style inside it.
    
    # Let's match the tag containing our NEW_LOGO_PATH and modify it.
    # Since we already ran string replacements, the content has NEW_LOGO_PATH.
    
    # Header
    content = re.sub(
        r'(<img[^>]*src="assets/FlourFolk\.png"[^>]*class="header__heading-logo[^"]*")[^>]*>',
        r'\1" style="max-height: 100px; width: auto;">',
        content
    )
    
    # Footer (if simpler)
    # class="footer-block..." container img? 
    # The footer img was: <img src="assets/FlourFolk.png" alt="" width="260" height="245">
    # We can just match the width/height pair if fairly unique or adjacent to src.
    content = re.sub(
        r'(src="assets/FlourFolk\.png"[^>]*?)width="260" height="245"',
        r'\1 style="max-height: 200px; width: auto;"',
        content
    )
    
    return content

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply Replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Fix dimensions
        new_content = fix_logo_dimensions(new_content)
            
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
            if file.lower().endswith((".html", ".htm", ".js", ".css")): # Include JS/CSS for text replacements
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
