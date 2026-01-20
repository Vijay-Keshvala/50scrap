import os
import re
import shutil

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/swayampaak.com"
NEW_LOGO_FILENAME = "Swad_Pickles.png"
# Logo already copied to assets/Swad_Pickles.png by previous step
NEW_LOGO_PATH = "assets/Swad_Pickles.png"

# Address
NEW_ADDRESS = "3rd Floor, Elegance Tower, Non Hierarchical Commercial Centre, Plot No.8, Jasola District Centre, New Delhi – 110076"

REPLACEMENTS = {
    # Name
    r"Swayampaak Kitchen": "Swad Pickle",
    r"Swayampaak": "Swad Pickle", 
    
    # URL/Email (Specifics first to avoid space issues if possible, but we have a fix script too)
    r"swayampaak\.com": "swadpickle.com",
    r"https://swayampaak\.com/": "https://www.swadpickle.com/",
    r"swayampaak@gmail\.com": "info@swadpickle.com",
    
    # Locations
    r"Nagpur": "New Delhi",
    r"Maharashtra": "Delhi", # Assuming Maharashtra mentions usually go with Nagpur
    
    # Specific logo file replacements in src
    r"wp-content/uploads/2024/02/swayampaak-logo-e1711807510428\.png": NEW_LOGO_PATH,
    r"assets/swayampaak_logo_e1711807510428_5424\.png": NEW_LOGO_PATH,
    r"swayampaak-logo": "Swad Pickles Logo", # Alt tags
    
    # Socials
    r"instagram\.com/swayampaak": "instagram.com/swadpickle",
    r"facebook\.com/swayampaak": "facebook.com/swadpickle",
    r"@swayampaak": "@swadpickle",
}

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
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
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".php")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
