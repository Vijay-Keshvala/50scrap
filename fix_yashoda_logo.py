import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/vijaydairy.com"
NEW_LOGO_PATH = "assets/YashodaDairy.png"
# The file I found in the grep output
OLD_LOGO_FILENAME = "assets/Logo_websitenew_png_9160.webp"

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Replace the specific logo file found in index.html (and potentially others)
        if OLD_LOGO_FILENAME in new_content:
            new_content = new_content.replace(OLD_LOGO_FILENAME, NEW_LOGO_PATH)
            
            # Also fix the img tag style if needed
            # <img ... src="assets/YashodaDairy.png" ... style="...">
            # The existing tag has specific style: style="--smush-placeholder-width: 139px; --smush-placeholder-aspect-ratio: 139/144;"
            # We might want to override or append max-height.
            
            # Helper to add dimensions if not present or replace bad ones
            # For now, let's just ensure the replacement happens.
            # If the user sees the image, we can tune the size.
            
            # I'll strip the lazy loading 'data-src' if it points to the old domain/file to avoid confusion, 
            # or replace it with the new local path too if the script supports it.
            # The grep showed: data-src="https://www.yashodadairy.com/wp-content/webp-express/webp-images/uploads/2023/02/Logo-websitenew.png.webp"
            # Note: I previously replaced 'vijaydairy.com' -> 'yashodadairy.com' so the URL is already updated but pointing to a file that might not exist on the new domain (conceptually).
            # But here `data-src` can also be replaced to point to the local asset to be safe.
            
            # Regex to clean up data-src
            new_content = re.sub(
                r'data-src="[^"]*Logo-websitenew\.png\.webp"',
                f'data-src="{NEW_LOGO_PATH}"',
                new_content
            )

            # Add max-height style for safety
            if 'style="max-height: 100px;' not in new_content:
                 # Find the tag we just updated
                 # <img ... src="assets/YashodaDairy.png" ...>
                 new_content = re.sub(
                     r'(src="assets/YashodaDairy\.png"[^>]*?)>',
                     r'\1 style="max-height: 100px; width: auto;">',
                     new_content
                 )

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".json")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
