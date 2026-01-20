import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/store.wellversed.in'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # We need to revert "Nutri Curator" / "nutricurator" back to "Wellversed" / "wellversed"
        # ONLY inside image paths (src, href, url, srcset)
        # BUT NOT if it is "NutriCurator.png" (our new logo)
        
        def revert_path(match):
            full_match = match.group(0)
            if "NutriCurator.png" in full_match:
                return full_match
            
            # Revert "Nutri Curator" -> "Wellversed" (if spaces were introduced in filenames)
            # Revert "nutricurator" -> "wellversed"
            reverted = full_match.replace("Nutri Curator", "Wellversed").replace("nutricurator", "wellversed").replace("NutriCurator", "Wellversed")
            return reverted

        # Patterns to check
        content = re.sub(r'src="[^"]*nutricurator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        content = re.sub(r'src="[^"]*Nutri Curator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        
        content = re.sub(r'href="[^"]*nutricurator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        # Careful with href, might be links we WANT to change? 
        # Usually image assets in href are for lightboxes or favicons. 
        # But external links should be Nutri Curator. 
        # If it ends in .jpg, .png, .css, .js -> Revert. 
        # If it is a domain... keep it? 
        # The rebrand script replaced "wellversed.in" -> "nutricurator.com".
        # If there was a file "wellversed.js", it became "nutricurator.js". We want to revert that.
        
        def revert_asset_link(match):
            full_match = match.group(0)
            if any(ext in full_match for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.css', '.js', '.woff', '.woff2']):
                # It's an asset, revert formatting
                if "NutriCurator.png" in full_match: return full_match
                return full_match.replace("Nutri Curator", "Wellversed").replace("nutricurator", "wellversed").replace("NutriCurator", "Wellversed")
            return full_match # Keep it (e.g. valid link to nutricurator.com)

        content = re.sub(r'href="[^"]+"', revert_asset_link, content)
        content = re.sub(r'srcset="[^"]+"', revert_asset_link, content)
        content = re.sub(r'url\([^)]+\)', revert_asset_link, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed images in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.css', '.js')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
