import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/thehoneycompany.in'
NEW_BRAND_NAME = "Honey Glide"
NEW_ADDRESS = "House No. 132, Lubi Circular Road, Dhanbad – 826001, Jharkhand"
NEW_EMAIL = "contact@honeyglide.com"
NEW_URL = "www.honeyglide.com"
NEW_LOGO_PATH = "assets/HoneyGlide.png"

# Old brand patterns
OLD_BRAND_PATTERNS = [
    r'\bThe Honey Company\b',
    r'\bHoney Company\b'
]

# Logo pattern - the main logo file
OLD_LOGO_PATTERN = r'THC_LOGO_R_e1710743106241_4022\.png'

def rebrand_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content

    # 1. URL Replacement (Do this FIRST)
    content = re.sub(r'thehoneycompany\.in', NEW_URL, content, flags=re.IGNORECASE)
    
    # 2. Email Replacement - if there are any honey company emails
    content = re.sub(r'[\w\.-]+@thehoneycompany\.in', NEW_EMAIL, content, flags=re.IGNORECASE)
    
    # 3. Text Branding Replacements
    # Replace "The Honey Company"
    content = re.sub(r'\bThe Honey Company\b', NEW_BRAND_NAME, content)
    
    # Replace "Honey Company" (without "The")
    content = re.sub(r'\bHoney Company\b', NEW_BRAND_NAME, content)
    
    # 4. Logo Replacement - Replace the main logo file
    content = re.sub(OLD_LOGO_PATTERN, 'HoneyGlide.png', content)
    
    # 5. Update logo img tags to add proper styling
    # Find img tags with the new logo and ensure they have proper dimensions
    def update_logo_tag(match):
        img_tag = match.group(0)
        if 'HoneyGlide.png' not in img_tag:
            return img_tag
        
        # Remove existing width/height attributes
        new_tag = re.sub(r'width="[^"]+"', '', img_tag)
        new_tag = re.sub(r'height="[^"]+"', '', new_tag)
        
        # Add style for consistent sizing (similar to original 500x88)
        if 'style=' not in new_tag:
            new_tag = new_tag.replace('<img ', '<img style="max-height: 88px; width: auto;" ')
        
        return new_tag
    
    # Apply to all img tags
    content = re.sub(r'<img[^>]*HoneyGlide\.png[^>]*>', update_logo_tag, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                rebrand_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("\nRebrand complete!")
