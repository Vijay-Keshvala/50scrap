import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/swayampaak.com"

FIXES = {
    # Fix spaces in URL/Email caused by replacements
    r"Swad Pickle\.com": "swadpickle.com",
    r"www\.Swad Pickle\.com": "www.swadpickle.com",
    r"info@Swad Pickle\.com": "info@swadpickle.com",
    r"info@swad pickle\.com": "info@swadpickle.com",
    
    # Socials
    r"facebook\.com/Swad Pickle": "facebook.com/swadpickle",
    r"instagram\.com/Swad Pickle": "instagram.com/swadpickle",
    r"@Swad Pickle": "@swadpickle",
    
    # Ensure full address visibility if needed (placeholder for now)
    
    # Cleanup any double dots or weird urls
    r"https://www\.Swad Pickle\.com": "https://www.swadpickle.com",
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
            print(f"Fixed collisions in: {filepath}")

    except Exception as e:
        print(f"Error fixed {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css")):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
