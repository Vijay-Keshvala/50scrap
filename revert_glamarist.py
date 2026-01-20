import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/glamrisdermacare.com'
OLD_NAME = "Glamarist"
NEW_NAME = "Excel Cosmetics"

OLD_URL = "glamarist.com"
NEW_URL = "excelcosmetics.in"

OLD_EMAIL = "business@glamarist.com"
NEW_EMAIL = "director@excelcosmetics.in"

OLD_ADDRESS = "Ground Floor, Opposite MGF Metropolitan Mall, Khirki Extension, Malviya Nagar, New Delhi — 110017"
NEW_ADDRESS = "House No. 156, Nikas Road, Budhwara, Ujjain – 456006, Madhya Pradesh"

NEW_LOGO_PATH = "assets/ExcelCosmetics.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    content = content.replace(OLD_NAME, NEW_NAME)
    
    # 2. Replace URL
    content = content.replace(OLD_URL, NEW_URL)
    
    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)

    # 4. Replace Address
    content = content.replace(OLD_ADDRESS, NEW_ADDRESS)
    
    # 5. Replace Logo
    # Match the Glamarist.png logo and replace with ExcelCosmetics.png
    content = content.replace("assets/Glamarist.png", NEW_LOGO_PATH)
    
    # Specifically check img tags for styling
    logo_pattern = re.compile(r'<img[^>]+src=["\'][^"\']*ExcelCosmetics\.png[^"\']*["\'][^>]*>')
    
    def logo_styler(match):
        img_tag = match.group(0)
        # Re-apply the 85px max-height which was used for Excel Cosmetics
        if 'style=' in img_tag:
            img_tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 85px; width: auto;"', img_tag)
        else:
            img_tag = img_tag.replace('>', ' style="max-height: 85px; width: auto;">')
        return img_tag

    content = logo_pattern.sub(logo_styler, content)

    # Asset restoration: ensure remote images point back to original if needed
    # Though both glamris and excel were using original images mostly.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Reverting {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Revert complete.")
