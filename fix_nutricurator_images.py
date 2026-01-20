import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'
# We need to revert "nutricurator" back to "organicsiri" IN FILENAMES/PATHS (src, href, url)
# BUT NOT if it matches our new logo "NutriCurator.png"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Regex to find paths containing "nutricurator" (case insensitive likely due to previous script)
        # We look for src="...", href="...", url(...) containing "nutricurator"
        # And revert it to "organicsiri" UNLESS it is "NutriCurator.png"
        
        def revert_path(match):
            full_match = match.group(0)
            # If it's the new logo, keep it
            if "NutriCurator.png" in full_match:
                return full_match
            
            # Otherwise, revert "nutricurator" -> "organicsiri"
            # The previous script likely replaced "organicsiri" with "nutricurator.com" or "Nutri Curator"
            # We need to handle variations.
            
            # Case 1: "nutricurator.com" was "organicsiri.com" - potentially valid replacement for external links, 
            # BUT if it's an internal asset path that WAS "organicsiri.com/...", it might be broken if files weren't renamed.
            # However, usually assets are relative or absolute.
            
            # Case 2: "Nutri Curator" in filename. e.g. "Nutri Curator_gallery..."
            # The rebrand script replaced "OrganicSiri" -> "Nutri Curator" or "organicsiri" -> "nutricurator"
            
            reverted = full_match.replace("Nutri Curator", "OrganicSiri").replace("nutricurator", "organicsiri")
            return reverted

        # Patterns to check
        # src="..."
        content = re.sub(r'src="[^"]*nutricurator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        # data-src="..."
        content = re.sub(r'data-src="[^"]*nutricurator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        # srcset="..."
        content = re.sub(r'srcset="[^"]*nutricurator[^"]*"', revert_path, content, flags=re.IGNORECASE)
        # url(...)
        content = re.sub(r'url\([^)]*nutricurator[^)]*\)', revert_path, content, flags=re.IGNORECASE)
        
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
