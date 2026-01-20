import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/hd-enterprise.ueniweb.com'
NEW_BRAND_NAME = "MM Bazar"
NEW_ADDRESS = "Plot No. 64, Agricultural Development Area, Achalpur Road – Amravati – 444805, Maharashtra"
NEW_EMAIL = "sales@mmbazar.in"
NEW_URL = "www.mmbazar.in"
NEW_LOGO_PATH = "assets/MMBazar.png"

# Old brand patterns
OLD_BRAND_PATTERNS = [
    r'\bHd Enterprise\b',
    r'\bHD Enterprise\b'
]

def rebrand_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content

    # 1. URL Replacement
    content = re.sub(r'hd-enterprise\.ueniweb\.com', NEW_URL, content, flags=re.IGNORECASE)
    
    # 2. Email Replacement
    content = re.sub(r'[\w\.-]+@hd-enterprise\.ueniweb\.com', NEW_EMAIL, content, flags=re.IGNORECASE)
    content = re.sub(r'vadaliya329@gmail\.com', NEW_EMAIL, content, flags=re.IGNORECASE)
    
    # 3. Text Branding Replacements
    content = re.sub(r'\bHd Enterprise\b', NEW_BRAND_NAME, content)
    content = re.sub(r'\bHD Enterprise\b', NEW_BRAND_NAME, content)
    
    # 4. Address Replacement - need to find the old address first
    # From the meta tags: "Block No-55, Surbhi Residency, Kothariya Main Road"
    old_address_pattern = r'Block No-55,\s*Surbhi Residency,\s*Kothariya Main Road'
    content = re.sub(old_address_pattern, NEW_ADDRESS, content, flags=re.IGNORECASE)
    
    # Also replace city/state info
    content = re.sub(r'Rajkot[,\s]*Gujarat', 'Amravati, Maharashtra', content, flags=re.IGNORECASE)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                rebrand_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("\nRebrand complete!")
