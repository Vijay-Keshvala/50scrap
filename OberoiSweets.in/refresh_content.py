import os
import re

# Configuration
directory = '/Users/vijaykeshvala/Documents/scraped_data/bansalsweets.in'

replacements = [
    # Global Branding
    (r'Oberoi Sweets', 'Bansal Sweets'),
    (r'Pure Desi Ghee Sweets', 'Authentic Desi Ghee Delicacies'),
    
    # Headings
    (r"INDIA'S MOST TRUSTED BRAND", "CELEBRATING TRADITION & TASTE"),
    (r"Making India's Favourite Sweets Since 1981", "Crafting Premium Indian Sweets with Love"),
    (r"Our Specialities", "Our Signature Collections"),
    
    # Footer
    (r"© Copyright 2026. All Rights Reserved By Oberoi Sweets.", "© 2026 Bansal Sweets. All Rights Reserved."),
]

# Exclusions to prevent breaking URLs/scripts if they strictly rely on the old name (though most were fixed previously)
# We will focus on visible text content where possible, but global replace is requested.
# previous fix_bansal.py handled hrefs, so mostly display text is left.

def refresh_content():
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for pattern, replacement in replacements:
                # Use regex sub for case-insensitive matching where appropriate or strict string replace?
                # The prompt implies specific capitalizations, so we'll stick to exact matches first or smart regex.
                # 'Oberoi Sweets' appears in Titles, Alt tags, Text.
                
                content = content.replace(pattern, replacement)
            
            # Additional safety: Replace "Oberoi" standalone if it refers to the brand in text
            # Be careful not to break "Oberoi" if it's part of a needed file path not yet updated, 
            # BUT we want to replace visual instances.
            # Let's stick to the specific list first to be safe and "minimal".

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filename}")
                count += 1
            else:
                print(f"No changes needed for {filename}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    refresh_content()
