import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/peachmode.com'
OLD_NAME = "Peachmode"
NEW_NAME = "Nandini Ethnics"

OLD_URL = "peachmode.com"
NEW_URL = "nandiniethnics.com"

OLD_EMAIL = "contact@peachmode.com"
NEW_EMAIL = "ceo@nandiniethnics.com"

# The user didn't explicitly give an 'old address' to replace, but I should look for it or add it.
# Based on common Shopify footers, it might be in a specific block.
NEW_ADDRESS = "Dhatt Cansa Tivim Sircain, Bardez, North Goa – 403502, Goa"

OLD_LOGO_NAME = "Peachmode_Logo_d591d907_a905_4b79_b2c2_d8afb40f5c71_390x_9943.png"
NEW_LOGO_PATH = "assets/NandiniEthnics.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace Name
    content = content.replace("Peachmode", NEW_NAME)
    content = content.replace("Peach mode", NEW_NAME)
    content = content.replace("peachmode", NEW_NAME.lower().replace(" ", ""))
    content = content.replace("PEACHMODE", NEW_NAME.upper())
    
    # 2. Replace URL
    content = content.replace(OLD_URL, NEW_URL)
    
    # 3. Replace Email
    content = content.replace(OLD_EMAIL, NEW_EMAIL)

    # 4. Replace/Add Address
    # If "Contact Us" section has email but no address, I'll add the address.
    # Original: <p>Need to contact us ? Just send us an e-mail to contact@peachmode.com</p>
    content = content.replace(f"Just send us an e-mail to {NEW_EMAIL}", f"Visit us at {NEW_ADDRESS} or send us an e-mail to {NEW_EMAIL}")

    # 5. Replace Logo
    # <img class="header__logo-image" width="500" height="92" src="assets/Peachmode_Logo_d591d907_a905_4b79_b2c2_d8afb40f5c71_390x_9943.png" alt="">
    logo_pattern = re.compile(r'<img[^>]+src=["\'][^"\']*' + re.escape(OLD_LOGO_NAME) + r'[^"\']*["\'][^>]*>')
    
    def logo_replacer(match):
        img_tag = match.group(0)
        # Replace src
        img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{NEW_LOGO_PATH}"', img_tag)
        # Update alt
        img_tag = re.sub(r'alt=["\'][^"\']+["\']', f'alt="{NEW_NAME}"', img_tag)
        if 'alt=' not in img_tag:
            img_tag = img_tag.replace('>', f' alt="{NEW_NAME}">')
            
        # Adjust height/styling
        img_tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', img_tag)
        img_tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', img_tag)
        
        if 'style=' in img_tag:
            img_tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 45px; width: auto;"', img_tag)
        else:
            img_tag = img_tag.replace('>', ' style="max-height: 45px; width: auto;">')
        return img_tag

    content = logo_pattern.sub(logo_replacer, content)

    # Asset preservation: restore original domain for remote assets
    asset_restore_pattern = re.compile(r'(https?://(?:www\.)?)nandiniethnics\.com(/[^"\'\s>]*(?:wp-content|wp-includes|uploads|cdn|(?:\.(?:png|jpg|jpeg|gif|webp|pdf|js|css|svg|ico|otf|ttf|woff2?|ashx))))', re.IGNORECASE)
    content = asset_restore_pattern.sub(r'\1peachmode.com\2', content)

    # Clean up social links if they point to peachmode
    content = content.replace("youtube.com/c/NandiniEthnics", "youtube.com/c/peachmode") # Restore if it's youtube
    content = content.replace("instagram.com/nandiniethnics", "instagram.com/peachmode")
    content = content.replace("facebook.com/nandiniethnics", "facebook.com/peachmode")

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
