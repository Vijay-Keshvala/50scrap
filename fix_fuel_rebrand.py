import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/camywafer.com"

# Fixes for the regex overlap issues
FIXES = {
    # Fix broken domain/emails caused by "CAMY" -> "Fuel Snax" replacement locally
    r"Fuel Snaxwafer\.com": "fuelsnax.com",
    r"Fuel Snaxwafer": "fuelsnax", 
    
    # Fix specific emails that might have been mangled
    r"Order@fuelsnax\.com": "management@fuelsnax.com",
    r"camy@fuelsnax\.com": "management@fuelsnax.com",
    r"Fuel Snax@fuelsnax\.com": "management@fuelsnax.com",
    
    # Catch-all for the mangled ones seen in verification
    r"Order@Fuel Snaxwafer\.com": "management@fuelsnax.com",
    r"Fuel Snax@Fuel Snaxwafer\.com": "management@fuelsnax.com",
    
    # Fix Copyright year if missed
    r"Copyright © Fuel Snax\. 2021": "Copyright © Fuel Snax. 2025",
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
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Base Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
