import os
import re

TARGET_DIR = "/Users/vijaykeshvala/Documents/scraped_data/carplus.in"

# Logo Replacement Configuration
OLD_LOGO_PATTERN = re.compile(r'<img[^>]*src="[^"]*Carplus_Logo[^"]*"[^>]*>', re.IGNORECASE | re.DOTALL)
NEW_LOGO_TAG = '<img src="assets/Krishna_Automotive_Logo.png" alt="Krishna Automotive" style="max-width: 250px; width: auto; height: auto; display: block;">'

# Address Replacement Configuration
# Targeted replacement for the specific footer structure found in index.html
OLD_ADDRESS_START = "Basement Floor AND 1st Floor 86 FIE"
NEW_ADDRESS_TEXT = "SCO 165/166, Madhya Marg, Sector 8C, Chandigarh — 160009"

NEW_EMAIL = "chairman@krishnaautomotive.co.in"
NEW_DOMAIN = "www.krishnaautomotive.co.in"

def rebrand_carplus(directory):
    print(f"Rebranding Carplus to Krishna Automotive in: {directory}")
    
    files_processed = 0
    files_updated = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                files_processed += 1
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 1. Logo Replacement
                    if OLD_LOGO_PATTERN.search(content):
                        content = OLD_LOGO_PATTERN.sub(NEW_LOGO_TAG, content)
                    
                    # 2. Text Replacement (Careful to avoid breaking assets)
                    # Replace Brand Name in Title/Meta/Text
                    content = content.replace("Carplus", "Krishna Automotive")
                    content = content.replace("CARPLUS", "Krishna Automotive") # Case sensitive check
                    
                    # Replace Email
                    content = content.replace("Info@carplus.in", NEW_EMAIL)
                    content = content.replace("info@carplus.in", NEW_EMAIL)
                    
                    # Replace Domain in text (avoid src/href unless specific)
                    # We will replace "carplus.in" in text content, but be careful with URLs.
                    # Given the risk of breaking assets (many assets might be on carplus.in/cdn...), 
                    # we will mostly rely on the logo and direct text replacements.
                    # If we see >carplus.in< (visible text), replace it.
                    content = content.replace(">carplus.in<", f">{NEW_DOMAIN}<")
                    content = content.replace(">www.carplus.in<", f">{NEW_DOMAIN}<")
                    
                    # 3. Footer Address Replacement
                    if OLD_ADDRESS_START in content:
                        # We'll do a focused replace on the address part
                        # Using a unique substring of the old address
                        content = content.replace("Basement Floor AND 1st Floor 86 FIE, Patparganj Industrial Area, East Delhi,  110092.", NEW_ADDRESS_TEXT)
                        content = content.replace("Basement Floor AND 1st Floor 86 FIE, Patparganj Industrial Area, East Delhi, 110092.", NEW_ADDRESS_TEXT) # Trying variant with single space
                        
                    
                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_updated += 1
                        
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Rebrand Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    rebrand_carplus(TARGET_DIR)
