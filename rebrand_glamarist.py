import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/glamrisdermacare.com'
OLD_NAME = "Excel Cosmetics"
NEW_NAME = "Glamarist"

OLD_URL = "excelcosmetics.in"
NEW_URL = "glamarist.com"

OLD_EMAIL = "director@excelcosmetics.in"
NEW_EMAIL = "business@glamarist.com"

# Exact address pattern from the file
OLD_ADDRESS = "House No. 156, Nikas Road, Budhwara, Ujjain – 456006, Madhya Pradesh"
NEW_ADDRESS = "Ground Floor, Opposite MGF Metropolitan Mall, Khirki Extension, Malviya Nagar, New Delhi — 110017"

NEW_LOGO_PATH = "assets/Glamris_logo_2509.png" # Restoring the original logo

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    content = content.replace("Excel Cosmetics", NEW_NAME)
    content = content.replace("ExcelCosmetics", NEW_NAME)
    content = content.replace("excelcosmetics", NEW_NAME.lower())
    
    # 2. Replace URL
    content = content.replace(OLD_URL, NEW_URL)
    
    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)

    # 4. Replace Address
    content = content.replace(OLD_ADDRESS, NEW_ADDRESS)
    
    # 5. Replace Logo
    # The current logo is ExcelCosmetics.png
    logo_pattern = re.compile(r'<img[^>]+src=["\'][^"\']*ExcelCosmetics\.png[^"\']*["\'][^>]*>')
    
    def logo_replacer(match):
        img_tag = match.group(0)
        # Replace src
        img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{NEW_LOGO_PATH}"', img_tag)
        # Update alt
        img_tag = re.sub(r'alt=["\'][^"\']+["\']', f'alt="{NEW_NAME}"', img_tag)
        # Adjust height/styling
        img_tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', img_tag)
        img_tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', img_tag)
        
        if 'style=' in img_tag:
            img_tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 85px; width: auto;"', img_tag)
        else:
            img_tag = img_tag.replace('>', ' style="max-height: 85px; width: auto;">')
        return img_tag

    content = logo_pattern.sub(logo_replacer, content)

    # Asset preservation: restore original domain for remote assets
    # Since we are rebranding back to something close to the original, we should ensure remote assets point to glamrisdermacare.com
    asset_restore_pattern = re.compile(r'(https?://(?:www\.)?)glamarist\.com(/[^"\'\s>]*(?:wp-content|wp-includes|uploads|cdn|(?:\.(?:png|jpg|jpeg|gif|webp|pdf|js|css|svg|ico|otf|ttf|woff2?|ashx))))', re.IGNORECASE)
    content = asset_restore_pattern.sub(r'\1glamrisdermacare.com\2', content)

    # Also catch any missed 'Excel' instances
    content = content.replace("Excel", NEW_NAME)

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
