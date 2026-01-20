import os
import re

TARGET_DIR = "/Users/vijaykeshvala/Documents/scraped_data/1ststep.com"

# Search for the sticky logo div
# <div class="sticky-logo">
OLD_TAG = '<div class="sticky-logo">'
NEW_TAG = '<div class="sticky-logo" style="margin-right: 50px;">'

def fix_logo_alignment(directory):
    print(f"Fixing logo alignment in: {directory}")
    files_processed = 0
    files_updated = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                files_processed += 1
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content
                    
                    # Simple string replace for the div class
                    if OLD_TAG in content:
                        content = content.replace(OLD_TAG, NEW_TAG)
                    
                    # Also, let's make sure we haven't already applied it or applied it multiple times
                    # If we find margin-right: 50px already, we might interpret it as done, 
                    # but since we are doing replace(OLD, NEW) it should be fine as long as NEW doesn't contain OLD exactly 
                    # (NEW contains OLD as a substring? No. OLD is '<div class="sticky-logo">')
                    # NEW is '<div class="sticky-logo" style="margin-right: 50px;">'
                    # So replace works cleanly.

                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_updated += 1
                        print(f"Updated: {path}")

                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Fix Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    fix_logo_alignment(TARGET_DIR)
