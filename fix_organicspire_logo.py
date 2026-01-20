import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'
NEW_LOGO_PATH = "wp-content/uploads/2021/04/OrganicSpire.png"
NEW_LOGO_FILENAME = "OrganicSpire.png"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Targeted fix for the logo missed in the first pass
        # "assets/logo_400_6014.png"
        
        def replace_logo_audit(match):
            img_tag = match.group(0)
            # Check for known old logo filenames
            if "logo_400_6014.png" in img_tag or "Organic_Logos" in img_tag:
                # Replace src
                img_tag = re.sub(r'src="[^"]+"', f'src="{NEW_LOGO_PATH}"', img_tag)
                # Remove srcset
                img_tag = re.sub(r'srcset="[^"]+"', '', img_tag)
                
                # Sizing
                if 'style="' in img_tag:
                    img_tag = re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
                else:
                    img_tag = img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')
                
                # Clear dimensions to let CSS handle it
                img_tag = re.sub(r'width="[^"]+"', '', img_tag)
                img_tag = re.sub(r'height="[^"]+"', '', img_tag)
                
                return img_tag
            return img_tag

        content = re.sub(r'<img[^>]+>', replace_logo_audit, content)
        
        # Direct replacement if not caught by img tag regex (rare but possible for background imgs)
        content = content.replace("assets/logo_400_6014.png", NEW_LOGO_PATH)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed logo in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
