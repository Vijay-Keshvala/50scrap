import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/gustorafoods.com'
NEW_ADDRESS = "House No. 67, Near Capital Police Station, Bhubaneswar – 751001, Odisha"
NEW_EMAIL = "odisha@saucelane.com"
NEW_LOGO_PATH = "assets/SauceLane.png"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Address Replacement
        # "B-207" was found in grep
        content = content.replace("B-207, Road No. 9, VKI Area, Jaipur, Rajasthan 302013", NEW_ADDRESS)
        content = content.replace("B-207, Road No. 9, VKI Area", "House No. 67, Near Capital Police Station")
        content = content.replace("Jaipur, Rajasthan 302013", "Bhubaneswar – 751001, Odisha")
        # Also check for "Jaipur, Rajasthan"
        content = content.replace("Jaipur, Rajasthan", "Bhubaneswar, Odisha")
        
        # 2. Email Replacement
        # Grep missed some? Or maybe they were obfuscated?
        # Let's replace knowns again just in case
        content = content.replace("hello@gustorafoods.com", NEW_EMAIL)
        
        # 3. Logo Replacement - Specific Fixes
        # <link rel="prefetch" ... href="...Gustora_Logo_copy_x320.png...">
        content = re.sub(r'href="[^"]*Gustora_Logo[^"]*"', f'href="{NEW_LOGO_PATH}"', content)
        
        # Header Logo
        # Found in view_file: <a ... class="header__heading-link link link--text focus-inset">... <span class="h2">Sauce Lane Foods</span></a>
        # It seems it might be using text if logo missing?
        # Or checking `sticky-header`:
        # <sticky-header data-sticky-type="reduce-logo-size" ...>
        #   ... 
        #   <img ... src="..." ... class="header__heading-logo">
        
        # I'll search for class="header__heading-logo" and replace src.
        def replace_header_logo(match):
            img_tag = match.group(0)
            # Replace src with new logo
            img_tag = re.sub(r'src="[^"]+"', f'src="{NEW_LOGO_PATH}"', img_tag)
            # Remove srcset
            img_tag = re.sub(r'srcset="[^"]+"', '', img_tag)
            # Fix width/height/style
            img_tag = re.sub(r'width="[^"]+"', '', img_tag)
            img_tag = re.sub(r'height="[^"]+"', '', img_tag)
            
            if 'style="' in img_tag:
                img_tag = re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
            else:
                img_tag = img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')
            return img_tag

        content = re.sub(r'<img[^>]+class="header__heading-logo"[^>]*>', replace_header_logo, content)
        
        # Also "header__logo" or similar if different theme version?
        # The view_file output was truncated so I couldn't see the exact img tag near line 4000.
        # But grep showed "header__heading-logo-wrapper" exists.
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned up: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
