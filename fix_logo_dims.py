import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/knayamfoods.com"

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # 1. Fix Header Logo (custom-logo)
        # Old: <img width="210" height="53" src="assets/PulsePlate.png" class="custom-logo" ...>
        # New: <img src="assets/PulsePlate.png" class="custom-logo" style="max-height: 160px; width: auto;" ...>
        # We perform a replace on the specific sequence of attributes
        # Note: We need to match the PREVIOUS replacement if running again, or the original if disjoint.
        # Since I'm editing the script to run essentially "from scratch" concept on patterns, 
        # I should handle the case where it might have already been changed or matches the original.
        # But this script is 'fix_logo_dims.py' intended to be run on the files. 
        # The previous run replaced 'width="210" ...' with 'style="..."'. 
        
        # Strategy: Match the *current* state of the file which has 'style="max-height: 80px; width: auto;"'
        # OR the original state if we are re-running on fresh files (though we are likely running on modified files).
        
        # Strategy: Match the *current* state (160px) and revert to 80px
        new_content = re.sub(
            r'style="max-height: 160px; width: auto;"',
            r'style="max-height: 80px; width: auto;"',
            new_content
        )
        
        # Also catch the original or intermediate states just in case
        new_content = re.sub(
            r'width="210" height="53" src="assets/PulsePlate\.png" class="custom-logo"',
            r'src="assets/PulsePlate.png" class="custom-logo" style="max-height: 80px; width: auto;"',
            new_content
        )
        
        # 2. Fix Footer Logo (class="image ...)
        # Current state might be 200x200. Revert to 150x150.
        new_content = re.sub(
            r'width="200" height="200" src="assets/PulsePlate\.png"',
            r'width="150" height="150" src="assets/PulsePlate.png"',
            new_content
        )
        
        # Catch other possibilities
        new_content = re.sub(
            r'width="150" height="150" src="assets/PulsePlate\.png"',
            r'width="150" height="150" src="assets/PulsePlate.png"',
            new_content
        )
        
        new_content = re.sub(
            r'width="210" height="53" src="assets/PulsePlate\.png" class="image',
            r'width="150" height="150" src="assets/PulsePlate.png" class="image',
            new_content
        )

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed logo dims in: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
