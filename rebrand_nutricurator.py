import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'
NEW_BRAND_NAME = "Nutri Curator"
NEW_ADDRESS = "66, Flat No. 101/A, Phase 3, Barrack Road, Barrackpore – 743101, West Bengal"
NEW_URL = "www.nutricurator.com"
NEW_EMAIL = "franchise@nutricurator.com"
NEW_LOGO_FILENAME = "NutriCurator.png"

# Replacement Dictionary
REPLACEMENTS = {
    # Brand Names
    "OrganicSiri Farms": NEW_BRAND_NAME,
    "OrganicSiri": NEW_BRAND_NAME,
    "Organic Siri": NEW_BRAND_NAME,
    "Organic Logos": NEW_BRAND_NAME, # Alt text
    
    # URLs and Emails
    "organicsiri.com": "nutricurator.com",
    "www.organicsiri.com": NEW_URL,
    "siri@organicsiri.com": NEW_EMAIL,
    
    # Copyright
    "NaturePinks LLP": NEW_BRAND_NAME,
}

# Regex for Address (if found, otherwise we might need to insert it)
# I couldn't find a clear address in the grep, so I will try to find a pattern or just rely on global replace if I find parts of it. 
# Since I didn't find the old address, I will NOT blindly replace a string I don't know. 
# instead, I will look for the footer copyright or similar to append/replace if needed. 
# For now, I'll stick to the text replacements. 

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Text Replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)

        # 2. Logo Replacement & Styling
        # Target: src="...Organic_Logos....png"
        # We want to replace the filename AND add the style.
        
        # Regex to find the logo image tag or just the src attribute if possible.
        # The HTML has: <img ... src="...Organic_Logos-300x94.png" ... >
        # We want to replace the SRC content.
        
        # Strategy: Replace the specifically known logo filenames first.
        logo_filenames = [
            "Organic_Logos-300x94.png",
            "Organic_Logos-64x20.png",
            "Organic_Logos-450x141.png",
            "Organic_Logos.png"
        ]
        
        for logo in logo_filenames:
            if logo in content:
                content = content.replace(logo, NEW_LOGO_FILENAME)
        
        # Now apply styling to the logo. 
        # Find img tags with src content containing the new logo filename
        def resize_logo(match):
            img_tag = match.group(0)
            if 'style="' in img_tag:
                 # Update existing style
                return re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
            else:
                # Add style
                return img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')

        # Regex for img tag containing the new logo
        # <img ... src="...NutriCurator.png" ...>
        content = re.sub(r'<img[^>]+src="[^"]*NutriCurator\.png"[^>]*>', resize_logo, content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
