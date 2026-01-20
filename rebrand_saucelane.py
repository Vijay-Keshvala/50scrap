import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/gustorafoods.com'
NEW_BRAND_NAME = "Sauce Lane"
NEW_ADDRESS = "House No. 67, Near Capital Police Station, Bhubaneswar – 751001, Odisha"
NEW_URL = "www.saucelane.com"
NEW_EMAIL = "odisha@saucelane.com"
NEW_LOGO_FILENAME = "SauceLane.png"

# Replacement Dictionary
REPLACEMENTS = {
    # Brand Names
    "Gustora": "Sauce Lane",
    "Gustora Foods": "Sauce Lane",
    
    # URLs and Emails
    "gustorafoods.com": "saucelane.com",
    "www.gustorafoods.com": NEW_URL,
    "hello@gustorafoods.com": NEW_EMAIL,
    "odisha@gustorafoods.com": NEW_EMAIL, # Possible artifact replacement
    
    # Address parts (based on likely content)
    "B-207, Road No. 9, VKI Area": "House No. 67, Near Capital Police Station",
    "Jaipur, Rajasthan": "Bhubaneswar, Odisha",
    "Jaipur, Rajasthan 302013": "Bhubaneswar – 751001, Odisha",
    # Specific one found in manual check or broad replacement:
    # "Gustora Foods Pvt. Ltd." -> "Sauce Lane Pvt. Ltd."
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Text Replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # 2. Logo Replacement & Styling
        # Old logos likely: Gustora-Logo.webp, Gustora-Logo-1.webp etc.
        # User said "fix the logo size as according for gustorafoods.com" -> imply preserving original size or setting to a good default?
        # User said "fix the logo size as according for gustorafoods.com" in previous prompt "fix the logo size as according for organicsiri.com"
        # The prompt says "fix the logo size as according for gustorafoods.com", which is slightly ambiguous. 
        # It likely means "set it to the size appropriate for this site" or "make it look good like we did before".
        # I'll stick to a reasonable max-height like 85px or matching the existing one.
        # Let's inspect the existing logo size if possible?
        # Standard rebrand approach:
        
        def replace_logo(match):
            img_tag = match.group(0)
            if "Gustora" in img_tag or "logo" in img_tag.lower():
                # Replace src
                img_tag = re.sub(r'src="[^"]+"', f'src="assets/{NEW_LOGO_FILENAME}"', img_tag)
                # Remove srcset
                img_tag = re.sub(r'srcset="[^"]+"', '', img_tag)
                
                # Apply styling - Assuming 85px is a safe bet for headers unless instructed otherwise.
                # Or better 100px? Let's use 85px as a start.
                if 'style="' in img_tag:
                     # Update existing style
                    img_tag = re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
                else:
                    # Add style
                    img_tag = img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')
                
                return img_tag
            return img_tag

        # Replace known logo files specifically
        # Check grep output: "Gustora-Logo.webp"
        
        content = re.sub(r'<img[^>]+src="[^"]*Gustora-Logo[^"]*"[^>]*>', replace_logo, content)
        content = re.sub(r'<img[^>]+src="[^"]*logo[^"]*"[^>]*>', replace_logo, content) 
        # CAREFUL: "logo" might match other icons. 
        # Be more specific: <img class="header__heading-logo" ...> ??
        # I'll target "Gustora" in src.
        
        content = re.sub(r'Gustora-Logo[-_0-9a-zA-Z]*\.(webp|png|jpg)', NEW_LOGO_FILENAME, content)

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
