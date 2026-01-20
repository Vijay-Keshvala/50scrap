import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/girani.in"
NEW_LOGO_PATH = "assets/images/Kalpana_Masala.png"

# Files identified from directory listing that look like the logo variants
LOGO_PATTERNS = [
    r"assets/Group_2030386_8799\.webp",
    r"assets/Group_2030386_0692\.png",
    r"assets/Group_2030386_1536\.webp",
    r"assets/Group_2030386_1762\.png",
    r"assets/Group 30386\.png", # specific one seen in favicon
]

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        
        # Replace specific logo files
        for pattern in LOGO_PATTERNS:
            # Use regex to replace ensuring we catch quotes/context if needed, but simple string sub is safer if exact match
            # content = new_content.replace(pattern, NEW_LOGO_PATH) # String replace might miss regex chars
            new_content = re.sub(pattern, NEW_LOGO_PATH, new_content, flags=re.IGNORECASE)

        # Also generic "logo.png" if it points to old location and wasn't fixed
        # But be careful not to break other things.
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated logo in: {filepath}")
            
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
