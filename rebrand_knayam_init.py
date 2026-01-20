import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/knayamfoods.com"
NEW_LOGO_PATH = "assets/PulsePlate.png"
NEW_BRAND_NAME = "The Pulse Plate"
NEW_URL = "www.thepulseplate.com"
NEW_EMAIL = "support@thepulseplate.com"
NEW_ADDRESS = "IV-1/48, Gopinath Bazzar, Delhi Cantonment, New Delhi – 110010"
NEW_PHONE = "+91 - 99 66 66 02 30"

REPLACEMENTS = {
    # Text/Names
    r"Knayam Foods": NEW_BRAND_NAME,
    r"knayamfoods": "thepulseplate", # generic lowercase replacement
    r"KnayamFoods": "ThePulsePlate",
    r"KNAYAM FOODS PIONEER PRIVATE LIMITED": "THE PULSE PLATE PRIVATE LIMITED",
    
    # URL/Email
    r"knayamfoods\.com": "thepulseplate.com",
    r"www\.knayamfoods\.com": "www.thepulseplate.com",
    r"info@knayamfoods\.com": NEW_EMAIL,
    
    # Address & Phone
    r"Plot No\. A-3/16, Industrial Area, Site – 5, Greater Noida, GBN, Uttar Pradesh, India": NEW_ADDRESS,
    r"Greater Noida, UP, INDIA": "New Delhi, India",
    r"\+91-9193386500": NEW_PHONE,
    r"\+91-9315412619": "", # Remove secondary phone if we only have one new one, or can leave it.
    
    # Titles
    r"Contact – knayamfoods": f"Contact – {NEW_BRAND_NAME}",
    
    # Logos (Specific file names found in index.html)
    # cropped_logo__1_1303.png seems to be the main logo
    r"assets/cropped_logo__1_1303\.png": NEW_LOGO_PATH,
    r"https://knayamfoods\.com/wp-content/uploads/2025/07/cropped-favicon-32x32\.png": "assets/favicon.png", # If we have one, otherwise ignore or point to logo
    
    
    # Socials
    r"facebook\.com/knayamfoods": "facebook.com/thepulseplate",
    r"instagram\.com/knayamfoods": "instagram.com/thepulseplate",
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
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
