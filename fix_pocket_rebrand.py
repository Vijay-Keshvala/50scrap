import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/shantis.in"

# Fixes for email collisions where "Shantis" -> "PocketEat" happened before email replacement
FIXES = {
    # Fix broken emails
    r"info@PocketEat\.com": "manager@pocketeat.com",
    r"info@PocketEat\.in": "manager@pocketeat.com",
    
    # Ensure correct capitalization for domain in text if needed, though URL is usually lowercase.
    # The view showed https://www.PocketEat.in/ - maybe we want www.pocketeat.com?
    # User asked for www.pocketeat.com.
    r"https://www\.PocketEat\.in/": "https://www.pocketeat.com/",
    r"https://www\.PocketEat\.com/": "https://www.pocketeat.com/",
    
    # Fix other collisions
    r"PocketEatfoods": "pocketeatfoods", # facebook link
    r"PocketEatfood": "pocketeatfood", # instagram
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
