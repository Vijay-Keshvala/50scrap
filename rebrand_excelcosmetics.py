import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/glamrisdermacare.com'
OLD_NAME = "Glamris Dermacare"
NEW_NAME = "Excel Cosmetics"

OLD_URL = "www.glamrisdermacare.com"
NEW_URL = "www.excelcosmetics.in"

OLD_EMAIL = "glamrissales@gmail.com"
NEW_EMAIL = "director@excelcosmetics.in"

# Specific address patterns found in the site
OLD_ADDRESS_FULL = "PLOT NO. 279, INDUSTRIAL AREA PHASE -2, PANCHKULA, HARYANA-134109, India"
NEW_ADDRESS = "House No. 156, Nikas Road, Budhwara, Ujjain – 456006, Madhya Pradesh"

OLD_LOGO_PATH = "assets/Glamris_logo_2509.png"
NEW_LOGO_PATH = "assets/ExcelCosmetics.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    content = content.replace(OLD_NAME, NEW_NAME)
    content = content.replace("Glamris Dermaare", NEW_NAME) # Seen in some titles
    content = content.replace("Glamries", NEW_NAME) # Seen in meta description
    
    # 2. Replace URL
    content = content.replace(OLD_URL, NEW_URL)
    content = content.replace("glamrisdermacare.com", "excelcosmetics.in")

    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)
    content = content.replace("glamrissales @ gmail.com", NEW_EMAIL) # Handle potential spacing

    # 4. Replace Address
    # We replace the full address and also parts of it if they appear separately
    content = content.replace(OLD_ADDRESS_FULL, NEW_ADDRESS)
    content = content.replace("PLOT NO. 279, INDUSTRIAL AREA PHASE -2, PANCHKULA, HARYANA-134109", NEW_ADDRESS)
    
    # 5. Replace Logo
    # Match the logo img tags and apply new height
    # Original: <img class="logo-main scale-with-grid" src="assets/Glamris_logo_2509.png" ...>
    logo_pattern = re.compile(r'<img[^>]+src=["\'][^"\']*Glamris_logo_2509\.png[^"\']*["\'][^>]*>')
    
    def logo_replacer(match):
        img_tag = match.group(0)
        # Replace src
        img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{NEW_LOGO_PATH}"', img_tag)
        # Replace data-retina
        img_tag = re.sub(r'data-retina=["\'][^"\']+["\']', f'data-retina="{NEW_LOGO_PATH}"', img_tag)
        # Remove width/height attributes to allow CSS to control it
        img_tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', img_tag)
        img_tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', img_tag)
        # Add new styling
        if 'style=' in img_tag:
            img_tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 85px; width: auto;"', img_tag)
        else:
            img_tag = img_tag.replace('>', ' style="max-height: 85px; width: auto;">')
        return img_tag

    content = logo_pattern.sub(logo_replacer, content)

    # Also replace any other instances of the logo filename (e.g. in schema or CSS)
    content = content.replace("assets/Glamris_logo_2509.png", NEW_LOGO_PATH)
    content = content.replace("Glamris_logo_2509.png", "ExcelCosmetics.png")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Rebranding complete.")
