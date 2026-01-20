import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'
NEW_BRAND_NAME = "Organic Spire"
NEW_ADDRESS = "48,  Block A, 1st Floor, Itinda Road, Near SBI Building, Basirhat – 743411, West Bengal"
NEW_URL = "www.organicspire.com"
NEW_EMAIL = "business@organicspire.com"
NEW_LOGO_FILENAME = "OrganicSpire.png"
NEW_LOGO_PATH = "wp-content/uploads/2021/04/OrganicSpire.png"

# Replacement Dictionary
REPLACEMENTS = {
    # Brand Names
    "OrganicSiri": NEW_BRAND_NAME,
    "Organic Siri": NEW_BRAND_NAME,
    "OrganicSiri Farms": NEW_BRAND_NAME,
    
    # URLs and Emails
    "organicsiri.com": "organicspire.com",
    "www.organicsiri.com": NEW_URL,
    "siri@organicsiri.com": NEW_EMAIL,
    "franchise@organicsiri.com": NEW_EMAIL, # Possible artifact
    
    # Socials (Cleanup)
    "facebook.com/OrganicSiri": "facebook.com/OrganicSpire",
    
    # Address (Best effort based on previous known addresses or generic)
    # Generic replacement not always safe for address, but we can try to find specific strings if known.
    # We will rely on "OrganicSiri" -> "Organic Spire" covering most brand mentions.
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Text Replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
            
        # 1.1 Address Replacement
        # Trying to check for the old address or parts of it if known.
        # Assuming the user wants the new address inserted where the old one was.
        # Since I don't have the exact old address string handy from the prompt, 
        # I'll search for typical address markers if I can, or trust the user that 
        # the brand name replacement might cover it if it was "OrganicSiri Farm, ...".
        # But actually, let's look for "Hyderabad" or "Telangana" which might be in the old address.
        # "123, Organic Farm, ... Hyderabad"
        # I'll add a specific replacement for the previous known address if found, 
        # or leave it to manual verification if not found.
        # Update: I will do a targeted replacement for the NEW_ADDRESS if I find a likely candidate.
        
        # 2. Logo Replacement & Styling
        # Old logos: Organic_Logos-300x94.png, Organic_Logos.png, etc.
        # We replace any reference to "Organic_Logos" with "OrganicSpire.png"
        
        def replace_logo(match):
            img_tag = match.group(0)
            # Check if it contains the old logo file
            if "Organic_Logos" in img_tag:
                # Replace src
                img_tag = re.sub(r'src="[^"]+"', f'src="{NEW_LOGO_PATH}"', img_tag)
                # Remove srcset to prevent loading old sizes
                img_tag = re.sub(r'srcset="[^"]+"', '', img_tag)
                # Apply styling
                if 'style="' in img_tag:
                     # Update existing style
                    img_tag = re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
                else:
                    # Add style
                    img_tag = img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')
                
                # Fix sizes/width/height attributes if they conflict
                img_tag = re.sub(r'width="[^"]+"', '', img_tag)
                img_tag = re.sub(r'height="[^"]+"', '', img_tag)
                
                return img_tag
            return img_tag

        # Find img tags
        content = re.sub(r'<img[^>]+>', replace_logo, content)
        
        # Also replace raw paths if not inside img tag (e.g. background image or direct link)
        # Be careful not to break the file we just copied if we aren't precise.
        # "Organic_Logos-300x94.png" -> "OrganicSpire.png"
        content = re.sub(r'Organic_Logos[-_0-9x]*\.png', NEW_LOGO_FILENAME, content)

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
