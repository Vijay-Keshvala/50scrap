import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/segashoes.com'
OLD_NAME = "Sega"
NEW_NAME = "Sole Label"

OLD_CORP_NAME = "Star Impact Pvt. Ltd."

OLD_URL = "segashoes.com"
NEW_URL = "solelabel.com"

OLD_EMAIL = "info@segashoes.in"
NEW_EMAIL = "report@solelabel.com"

OLD_ADDRESS = "Rehman Nagar, Opp. Power Grid, Ludhiana Road, Malerkotla - 148023 Punjab, India"
NEW_ADDRESS = "Ghazipur, A-5, Mandawali Main Road, Mandawali, New Delhi — 110092"

NEW_LOGO_PATH = "assets/SoleLabel.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    content = content.replace("Sega", NEW_NAME)
    content = content.replace("SEGA", NEW_NAME.upper())
    content = content.replace(OLD_CORP_NAME, NEW_NAME)
    
    # 2. Replace URL
    content = content.replace(OLD_URL, NEW_URL)
    content = content.replace("segashoes.in", "solelabel.com")
    
    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)

    # 4. Replace Address
    # Looking for the specific address string found in grep
    content = content.replace("Rehman Nagar, Opp. Power Grid,<br />Ludhiana Road, Malerkotla - 148023<br />Punjab, India", NEW_ADDRESS.replace(", ", ",<br />"))
    content = content.replace("Rehman Nagar, Opp. Power Grid, Ludhiana Road, Malerkotla - 148023 Punjab, India", NEW_ADDRESS)

    # 5. Replace Logo
    # assets/logo_2026.webp, assets/logo_3391.webp, template/assets/images/logo-black.png
    logo_patterns = [
        r'assets/logo_2026\.webp',
        r'assets/logo_3391\.webp',
        r'template/assets/images/logo-black\.png'
    ]
    
    for pattern in logo_patterns:
        content = re.sub(r'src=["\']' + pattern + r'["\']', f'src="{NEW_LOGO_PATH}"', content)

    # Apply styling to the new logo
    def logo_styler(match):
        tag = match.group(0)
        # remove old width/height
        tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', tag)
        tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', tag)
        # update alt
        tag = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{NEW_NAME}"', tag)
        if 'alt=' not in tag:
            tag = tag.replace('>', f' alt="{NEW_NAME}">')
        # add style
        if 'style=' in tag:
            tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 55px; width: auto;"', tag)
        else:
            tag = tag.replace('>', ' style="max-height: 55px; width: auto;">')
        return tag

    content = re.sub(r'<img[^>]+src=["\']' + re.escape(NEW_LOGO_PATH) + r'["\'][^>]*>', logo_styler, content)

    # Asset preservation: restore original domain for remote assets
    asset_restore_pattern = re.compile(r'(https?://(?:www\.)?)solelabel\.com(/[^"\'\s>]*(?:wp-content|wp-includes|uploads|cdn|(?:\.(?:png|jpg|jpeg|gif|webp|pdf|js|css|svg|ico|otf|ttf|woff2?|ashx))))', re.IGNORECASE)
    content = asset_restore_pattern.sub(r'\1segashoes.com\2', content)

    # Clean up social links if they point to senga
    content = content.replace("facebook.com/segashoes", "facebook.com/solelabel")
    content = content.replace("instagram.com/segashoes", "instagram.com/solelabel")

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
