import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/dresswalanx.com'
OLD_NAME = "Dresswala NX"
NEW_NAME = "Man Shear"

OLD_URL = "dresswalanx.com"
NEW_URL = "manshear.com"

OLD_EMAIL = "contact@dresswalanx.com"
NEW_EMAIL = "feedback@manshear.com"

# Exact address pattern from the file
OLD_ADDRESS = "DRESSWALA NX, OPP. IMPERAIL HEIGHTS, 177 178, HEMANG ARCADE, 150 FEET RING ROAD, RAJKOT, GUJARAT, 360007"
NEW_ADDRESS = "42-C, Phase 3, Block M, 1st Floor, Risali Sector, Bhilai – 490006, Chhattisgarh"

OLD_LOGO_NAME = "Logo_for_header_side_text_8417.png"
NEW_LOGO_PATH = "assets/Manshear.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    # Various forms of the name
    content = content.replace("Dresswala NX", NEW_NAME)
    content = content.replace("DresswalaNX", NEW_NAME)
    content = content.replace("dresswalanx", NEW_NAME.lower().replace(" ", ""))
    content = content.replace("DRESSWALA NX", NEW_NAME.upper())
    
    # 2. Replace URL (Careful with shopify links, etc.)
    # Replace the main domain.
    content = content.replace(OLD_URL, NEW_URL)
    
    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)

    # 4. Replace Address
    content = content.replace(OLD_ADDRESS, NEW_ADDRESS)
    content = content.replace("Shop premium men's wedding wear in Rajkot", f"Shop premium men's wedding wear in {NEW_ADDRESS.split(',')[-2].strip()}")
    content = content.replace("Rajkot, Gujarat", f"{NEW_ADDRESS.split(',')[-2].strip()}, {NEW_ADDRESS.split(',')[-1].strip()}")
    
    # 5. Replace Logo
    # Replace header logo
    logo_pattern = re.compile(r'<img[^>]+src=["\'][^"\']*Logo_for_header_side_text_8417\.png[^"\']*["\'][^>]*>')
    
    def logo_replacer(match):
        img_tag = match.group(0)
        # Replace src
        img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{NEW_LOGO_PATH}"', img_tag)
        # Update alt
        img_tag = re.sub(r'alt=["\'][^"\']+["\']', f'alt="{NEW_NAME}"', img_tag)
        # Adjust height/styling
        # Remove hardcoded height attributes
        img_tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', img_tag)
        img_tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', img_tag)
        
        if 'style=' in img_tag:
            img_tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 55px; width: auto;"', img_tag)
        else:
            img_tag = img_tag.replace('>', ' style="max-height: 55px; width: auto;">')
        return img_tag

    content = logo_pattern.sub(logo_replacer, content)

    # Replace absolute URLs for assets and images that should be restored to Dresswala (to prevent broken links)
    # We do this backwards: anything that now says manshear.com/... but should be dresswalanx.com/...
    # This prevents the rebrand script from breaking existing remote images.
    asset_restore_pattern = re.compile(r'(https?://(?:www\.)?)manshear\.com(/[^"\'\s>]*(?:wp-content|wp-includes|uploads|cdn|(?:\.(?:png|jpg|jpeg|gif|webp|pdf|js|css|svg|ico|otf|ttf|woff2?|ashx))))', re.IGNORECASE)
    content = asset_restore_pattern.sub(r'\1dresswalanx.com\2', content)

    # Ensure favicon is updated to the new logo if it was replaced by generic text
    content = content.replace("logo512x512-white-bg.jpg", "Manshear.png")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Rebranding {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Rebranding complete.")
