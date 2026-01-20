import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/shantis.in"

FIXES = {
    # Fix spaces in Email/URL caused by naive "PocketEat" -> "Kalpana Masala"
    r"manager@Kalpana Masala\.com": "feedback@kalpanamasala.com",
    r"info@Kalpana Masala\.com": "feedback@kalpanamasala.com",
    r"Kalpana Masala\.com": "kalpanamasala.com", # Fix spaces in domain
    r"www\.Kalpana Masala\.com": "www.kalpanamasala.com",
    
    # Fix Socials/Other
    r"Kalpana Masalafoods": "kalpanamasalafoods",
    r"Kalpana Masalafood": "kalpanamasalafood",
    r"twitter\.com/Kalpana Masala": "twitter.com/kalpanamasala",
    
    # Ensure email is strictly feedback@kalpanamasala.com if it's currently something else odd
    r"manager@kalpanamasala\.com": "feedback@kalpanamasala.com",
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
