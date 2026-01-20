import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Fix Spaces in URLs
        # "https://twitter.com/Nutri Curator" -> "https://twitter.com/NutriCurator"
        # "https://www.facebook.com/Nutri Curator" -> "https://www.facebook.com/NutriCurator"
        # General simplistic fix for URL contexts
        # We look for "Nutri Curator" inside href="..." or src="..."
        
        def remove_spaces_in_quotes(match):
            full_str = match.group(0)
            if "Nutri Curator" in full_str:
                return full_str.replace("Nutri Curator", "NutriCurator")
            return full_str

        content = re.sub(r'href="[^"]*Nutri Curator[^"]*"', remove_spaces_in_quotes, content)
        content = re.sub(r'src="[^"]*Nutri Curator[^"]*"', remove_spaces_in_quotes, content)

        # 2. Fix Email
        # `siri@nutricurator.com` -> `franchise@nutricurator.com`
        content = content.replace("siri@nutricurator.com", "franchise@nutricurator.com")
        
        # 3. Fix Image paths that might have been missed by previous fix if they were capitalized or something?
        # My previous fix script looked for "nutricurator" case-insensitive and reverted to "organicsiri"
        # unless it was "NutriCurator.png". 
        # But if the file was "organicsiri_gallery...", it became "Nutri Curator_gallery" or "nutricurator_gallery".
        # The fix script handled "Nutri Curator" -> "OrganicSiri" and "nutricurator" -> "organicsiri".
        # Let's add a check for "nutricurator" in src again just in case, but STRICTLY for non-logo.
        
        def revert_missed_images(match):
            full_match = match.group(0)
            if "NutriCurator.png" in full_match:
                return full_match
            # Revert
            return full_match.replace("nutricurator", "organicsiri").replace("NutriCurator", "OrganicSiri")

        # Re-run strict checks on src attributes for any lingering "nutricurator" in images (e.g. NutriCurator_gallery)
        # Note: Previous script replaced "Nutri Curator" with space. 
        # If text replace made it "Nutri Curator_gallery", fix script handled it.
        # If text replace made it "NutriCurator_gallery" (no space), fix script handled "nutricurator" (case insensitive).
        # So it should be fine. I'll just do the specific email and URL space fix.
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned up: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
