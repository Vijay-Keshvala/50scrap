import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/store.wellversed.in'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Fix Email artifacts
        # `support@wellversed.in` -> `nutricurator.com` replacement caused `support@nutricurator.com`
        content = content.replace("support@nutricurator.com", "franchise@nutricurator.com")
        content = content.replace("support@wellversed.in", "franchise@nutricurator.com") # Just in case
        
        # 2. Fix URL spacing artifacts
        # If "Nutri Curator" replaces "Wellversed" in URLs:
        # facebook.com/Wellversed -> facebook.com/Nutri Curator
        content = content.replace("facebook.com/Nutri Curator", "facebook.com/NutriCurator")
        content = content.replace("instagram.com/Nutri Curator", "instagram.com/NutriCurator")
        content = content.replace("twitter.com/Nutri Curator", "twitter.com/NutriCurator")
        
        # 3. Cleanup specific paths
        # "store.Nutri Curator.in" -> "nutricurator.com" ??
        # "store.wellversed.in" -> "nutricurator.com".
        # If "Wellversed" -> "Nutri Curator", then "store.Wellversed.in" -> "store.Nutri Curator.in"
        # My rebrand script had "store.wellversed.in": "nutricurator.com". 
        # But case sensitivity might have missed "store.Wellversed.in" if it existed.
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned up: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
