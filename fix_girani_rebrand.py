import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/girani.in"

FIXES = {
    # Fix spaces in URL/Domain
    r"Kalpana Masala\.in": "kalpanamasala.com",
    r"Kalpana Masala\.com": "kalpanamasala.com",
    r"www\.Kalpana Masala\.com": "www.kalpanamasala.com",
    r"https://Kalpana Masala\.in/": "https://www.kalpanamasala.com/",
    
    # Fix social handles and package names
    r"Kalpana Masala_mill": "kalpanamasala",
    r"com\.Kalpana Masala\.user": "com.kalpanamasala.user",
    
    # Email fixes
    r"feedback@Kalpana Masala\.com": "feedback@kalpanamasala.com",
    r"info@Kalpana Masala\.com": "feedback@kalpanamasala.com",
    
    # Fix any remaining spaces in protocols or paths
    r"https://Kalpana Masala": "https://kalpanamasala",
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
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".php")): 
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
