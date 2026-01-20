import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/myparipoornaoil.com"
NEW_LOGO_PATH = "assets/SureGhee.png"

# Replacements to fix broken URLs and text from previous run
FIX_REPLACEMENTS = {
    # Fix broken URL/Email
    r"mySure Gheeoil\.com": "sureghee.com",
    r"sales@mySure Gheeoil\.com": "management@sureghee.com",
    
    # Fix broken logo filename
    r"assets/Sure Ghee_cold_pressed_oil_4203\.webp": NEW_LOGO_PATH,
    r"assets/images/bg/Sure Ghee-cold-pressed-oil\.webp": NEW_LOGO_PATH, # Schema logo probably broken too
    
    # Fix broken Socials
    r"Sure Gheeorganicoil": "sureghee",
    r"Sure Ghee_coldpressed_oil": "sureghee",
    
    # Fix Title if strictly needed (Top Wooden Cold Pressed...) -> content might be fine, but let's check branding.
    # The user asked to "do the same" which implies replacing "Paripoorna" with "Sure Ghee".
    # Existing title: "Top Wooden Cold Pressed Oil Manufacturer & Exporter in India" - generic, maybe fine.
    # Meta description: "Sure Ghee is the top..." - This looks correct after first pass.
    
    # Fix any remaining specific broken patterns
    r"www\.mySure Gheeoil\.com": "www.sureghee.com",
}

def fix_logo_dimensions(content):
    # Fix Logo dimensions again if they were missed or messed up
    if NEW_LOGO_PATH in content:
        # Check if we have the width/height still there or if we need to apply style
        # Pattern: <img src="assets/SureGhee.png" ... width="256" height="64">
        # Replace with style
        content = re.sub(
            r'(src="assets/SureGhee\.png"[^>]*?)width="256" height="64"',
            r'\1 style="max-height: 100px; width: auto;"',
            content
        )
    return content

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        for pattern, replacement in FIX_REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        new_content = fix_logo_dimensions(new_content)
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".json", ".js", ".css")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
