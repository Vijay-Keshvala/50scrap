import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/grainculture.store"
NEW_LOGO_PATH = "assets/RiceRoyal.png"

FIXES = {
    # App Store / Play Store links
    r"https://apps\.apple\.com/in/app/grain-culture/id\d+": "#",
    r"https://play\.google\.com/store/apps/details\?id=store\.grainculture.*": "#",
    r"app-id=store\.grainculture": "app-id=store.riceroyal",
    
    # OG Image
    r"https://cdn\.shopaccino\.com/edible-smart/images/logo-180044headerlogo-66505045801656_social_sharing\.png\?v=651": NEW_LOGO_PATH,
    
    # Remaining Grain Culture refs
    r"Grain Culture": "Rice Royal",
    r"grain-culture": "rice-royal",
    r"grainculture": "riceroyal",
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in FIXES.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
