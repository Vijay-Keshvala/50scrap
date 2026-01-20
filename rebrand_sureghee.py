import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/myparipoornaoil.com"
NEW_LOGO_PATH = "assets/SureGhee.png"
New_Brand_Name = "Sure Ghee"
New_Domain = "sureghee.com"
New_Email = "management@sureghee.com"
New_Address = "Plot C, Block B, House No. 60, Sahar Airport Road, Andheri East, Mumbai, Maharashtra – 400099"

# Replacements Dictionary
# Regex patterns to find and replace
REPLACEMENTS = {
    # 1. CSS/Asset Path Fix
    r'\.\./assets/': 'assets/',  # Fix broken paths like <link href="../assets/css...">
    
    # 2. Brand Name
    r"Paripoorna Wood Pressed Oil": New_Brand_Name,
    r"Paripoorna Oil": New_Brand_Name,
    r"Paripoorna": New_Brand_Name, # Broad replacement, might be risky but "Paripoorna" seems to be the brand name.
    
    # 3. Domain/URL
    r"myparipoornaoil\.com": New_Domain,
    r"www\.myparipoornaoil\.com": "www." + New_Domain,
    
    # 4. Email
    r"sales@myparipoornaoil\.com": New_Email,
    
    # 5. Address (Found in index.html)
    r"Chettipalayam<br>\s*Tamil Nadu - 641201": New_Address, # Flexible whitespace
    
    # 6. Logos
    # Header Logo
    r"assets/paripoorna_cold_pressed_oil_4203\.webp": NEW_LOGO_PATH,
    # Schema Logo
    r"assets/images/bg/paripoorna-cold-pressed-oil\.webp": NEW_LOGO_PATH,
    # Any other logo ref?
    r"assets/images/logo/icon\.png": "assets/SureGhee.png", # Favicon potentially? Or leave it if we don't have one. user said "Same as we done it previously", usually we replace main logos.
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Additional specific fixes if regex isn't enough
        
        # Logo styling fix (if needed, similar to previous tasks)
        # The current logo has width="256" height="64". 
        # The new logo is a square png likely (Sure Ghee.png). 
        # We should constrain it contextually.
        if NEW_LOGO_PATH in new_content:
             # Header logo container context
             # <img src="assets/SureGhee.png" ... width="256" height="64">
             # We want to change this to something like max-height: 80px; width: auto;
             new_content = re.sub(
                 r'(src="assets/SureGhee\.png"[^>]*?)width="256" height="64"',
                 r'\1 style="max-height: 100px; width: auto;"',
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
            if file.lower().endswith((".html", ".htm", ".json")): # Include JSON for schema if it was in a separate file, mostly in HTML
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
