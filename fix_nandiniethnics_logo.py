import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/peachmode.com'
NEW_NAME = "Nandini Ethnics"
NEW_ADDRESS = "Dhatt Cansa Tivim Sircain, Bardez, North Goa – 403502, Goa"
NEW_EMAIL = "ceo@nandiniethnics.com"
NEW_URL = "nandiniethnics.com"
OLD_URL = "peachmode.com"

NEW_LOGO_PATH = "assets/NandiniEthnics.png"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Fix the logo (identifying both the original and partially replaced versions)
    # The previous run might have changed Peachmode_Logo... to Nandini Ethnics_Logo...
    logo_src_patterns = [
        r'assets/Peachmode_Logo_[^"\'\s>]+',
        r'assets/Nandini\sEthnics_Logo_[^"\'\s>]+'
    ]
    
    for pattern in logo_src_patterns:
        content = re.sub(r'src=["\']' + pattern + r'["\']', f'src="{NEW_LOGO_PATH}"', content)

    # Apply styling to the new logo
    def logo_styler(match):
        tag = match.group(0)
        # remove old width/height
        tag = re.sub(r'\swidth=["\'][^"\']*["\']', '', tag)
        tag = re.sub(r'\sheight=["\'][^"\']*["\']', '', tag)
        # update alt
        tag = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{NEW_NAME}"', tag)
        if 'alt=' not in tag:
            tag = tag.replace('>', f' alt="{NEW_NAME}">')
        # add style
        if 'style=' in tag:
            tag = re.sub(r'style=["\']([^"\']+)["\']', r'style="\1; max-height: 85px; width: auto;"', tag)
        else:
            tag = tag.replace('>', ' style="max-height: 85px; width: auto;">')
        return tag

    content = re.sub(r'<img[^>]+src=["\']' + re.escape(NEW_LOGO_PATH) + r'["\'][^>]*>', logo_styler, content)

    # 2. Add Address in footer Contact Us section
    # The initial script might have already added it, check for double additions
    if NEW_ADDRESS not in content:
        content = content.replace(f"Just send us an e-mail to {NEW_EMAIL}", f"Visit us at {NEW_ADDRESS} or send us an e-mail to {NEW_EMAIL}")

    # 3. Restore remote assets (fix broken domains)
    # Anything in //nandiniethnics.com/cdn or //nandiniethnics.com/s/files that should be peachmode.com
    # Also handle the ones that got 'Nandini Ethnics' in the filename if they are remote
    content = content.replace("//nandiniethnics.com/cdn", "//peachmode.com/cdn")
    content = content.replace("//nandiniethnics.com/s/files", "//peachmode.com/s/files")
    
    # Identify remote images that had 'peachmode' in filename replaced by 'nandiniethnics' or 'nandini ethnics'
    # Example: navy-blue-...-peachmode-1.jpg -> navy-blue-...-nandini ethnics-1.jpg
    # This is tricky, but we can try to restore //peachmode.com/ links if they look like they were modified
    content = re.sub(r'//peachmode\.com/([^"\'\s>]*)(?:nandini\s+ethnics|nandiniethnics)([^"\'\s>]*)', r'//peachmode.com/\1peachmode\2', content, flags=re.IGNORECASE)

    # 4. Fix some miscellaneous broken strings
    content = content.replace("youtube.com/c/Nandini Ethnics", "youtube.com/c/Peachmode")
    content = content.replace("youtube.com/c/NandiniEthnics", "youtube.com/c/Peachmode")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Fixing {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Fixing complete.")
