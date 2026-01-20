import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com"
NEW_LOGO_PATH = "assets/Kiddiwell.png"
OLD_LOGO_FILENAME = "Balvvardhak_logo_0504.webp"
NEW_NAME = "Kiddi Well"

REPLACEMENTS = {
    # Brand Name
    r"Balvvardhak Foods": NEW_NAME,
    r"Balvvardhak": NEW_NAME,
    
    # URL/Email
    r"balvvardhak\.com": "kiddiwell.com",
    r"www\.balvvardhak\.com": "www.kiddiwell.com",
    r"info@balvvardhak\.com": "city@kiddiwell.com",
    r"support@balvvardhak\.com": "city@kiddiwell.com",
    
    # Address
    r"Warje Jakat Naka, Pune, Maharashtra": 
    "12/25, Block E, 2nd Floor, Flat No. 204, KNC Road, Barasat, 24 Parganas, West Bengal, 700124",

    # Logo
    r"Balvvardhak_logo_0504\.webp": "Kiddiwell.png",
    r"Kiddi Well_logo_0504\.webp": "Kiddiwell.png",
    
    # URL Cleanup (Fix spaces introduced by brand name replacement)
    r"Kiddi Well\.com": "kiddiwell.com",
    r"www\.Kiddi Well\.com": "www.kiddiwell.com",
}

def fix_logo_style(content):
    # Ensure logo looks good.
    # Matched pattern: <img ... src="...Kiddiwell.png" ...>
    if "Kiddiwell.png" in content:
        # Check if style is present, if not add max-height
        # The existing logo might be too large if width/height attributes are respected from original
        # We can try to enforce some constraints if needed, or just let it be if it replaces exact dimensions.
        # But usually a resize helper is good.
        if 'max-height' not in content:
             content = re.sub(
                 r'(src="[^"]*Kiddiwell\.png"[^>]*?)>',
                 r'\1 style="max-height: 100px; width: auto;">',
                 content
             )
    return content

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Fix logo style
        new_content = fix_logo_style(new_content)
        
        # Specific Logo Asset path fix if it's pointing to old filename in a path
        if OLD_LOGO_FILENAME in new_content:
             new_content = new_content.replace(OLD_LOGO_FILENAME, "Kiddiwell.png")
        if "Kiddi Well_logo_0504.webp" in new_content:
             new_content = new_content.replace("Kiddi Well_logo_0504.webp", "Kiddiwell.png")
             
        # Cleanup spaced URLs from previous run
        new_content = new_content.replace("Kiddi Well.com", "kiddiwell.com")
        new_content = new_content.replace("www.Kiddi Well.com", "www.kiddiwell.com")
        
        # Enforce logo style
        style_str = 'style="max-height: 85px; width: auto;"'
        # Regex to find src="assets/Kiddiwell.png" (allowing for different quotes) and prepend style if not present
        if 'Kiddiwell.png' in new_content and 'max-height: 85px' not in new_content:
             new_content = re.sub(
                 r'(src=["\']assets/Kiddiwell\.png["\'])', 
                 f'{style_str} \\1', 
                 new_content
             )

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".json")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
