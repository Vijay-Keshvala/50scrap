import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/gustorafoods.com'
NEW_LOGO_PATH = "assets/SauceLane.png"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Promo Code Fix
        # "AVAIL FLAT 10% OFF with code "GUSTORA""
        content = content.replace('code "GUSTORA"', 'code "SAUCELANE"')
        content = content.replace("code 'GUSTORA'", "code 'SAUCELANE'")
        content = content.replace('code "Gustora"', 'code "SAUCELANE"')
        
        # 2. Comprehensive Logo Replacement
        
        # Regex to find img tags with "Gustora" in src, regardless of path (CDN or local)
        # Matches: <img ... src="...Gustora..." ...>
        
        def replace_logo_img(match):
            img_tag = match.group(0)
            # Check if it's likely a logo or branding image we want to replace
            if "Gustora" in img_tag and ("logo" in img_tag.lower() or "chrismas" in img_tag.lower() or "christmas" in img_tag.lower()):
                 # Replace src
                img_tag = re.sub(r'src="[^"]+"', f'src="{NEW_LOGO_PATH}"', img_tag)
                # Remove srcset
                img_tag = re.sub(r'srcset="[^"]+"', '', img_tag)
                # Remove sizes if present to avoid browser picking old ones?
                # img_tag = re.sub(r'sizes="[^"]+"', '', img_tag) 
                # Better to keep sizes or remove? Let's remove to be safe if we change size.
                img_tag = re.sub(r'sizes="[^"]+"', '', img_tag)
                
                 # Styling
                if 'style="' in img_tag:
                    img_tag = re.sub(r'style="[^"]+"', 'style="max-height: 85px; width: auto;"', img_tag)
                else:
                    img_tag = img_tag.replace('<img ', '<img style="max-height: 85px; width: auto;" ')
                
                # Clear explicit width/height attributes if they conflict
                img_tag = re.sub(r'width="[^"]+"', '', img_tag)
                img_tag = re.sub(r'height="[^"]+"', '', img_tag)

                return img_tag
            return img_tag

        # Apply to all img tags
        content = re.sub(r'<img[^>]+>', replace_logo_img, content)
        
        # 3. Direct path replacements for things potentially missed by regex (e.g. background images or CSS)
        # CDN paths: //www.gustorafoods.com/cdn/shop/files/Gustora_Logo_Christmas.png?v=1766368902...
        # We replace the whole filename part with our local asset
        
        # Regex for CDN logo paths
        # Pattern: .../Gustora_Logo_Christmas... .png
        content = re.sub(r'(https?:)?//[^"\s\)]+Gustora_Logo[^"\s\)]+\.(png|jpg|webp|jpeg)', NEW_LOGO_PATH, content)
        
        # 4. Favicon?
        # <link rel="icon" ... href="//www.gustorafoods.com/cdn/shop/files/Favicon_Gustora.png...">
        # Check if we want to replace favicon. User didn't explicitly ask but good practice.
        # I'll leave it unless it's easy. Favicon likely "SauceLane.png" too? 
        # User said "just the logo ... nothing else". Favicon is logo-ish.
        # Let's replace favicon href with SauceLane.png for consistency if it matches "Gustora"
        content = re.sub(r'<link rel="icon"[^>]+href="[^"]*Gustora[^"]*"[^>]*>', f'<link rel="icon" type="image/png" href="{NEW_LOGO_PATH}">', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed logo/promo in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
