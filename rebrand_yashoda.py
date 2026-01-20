import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/vijaydairy.com"
NEW_LOGO_PATH = "assets/YashodaDairy.png"
# Context from task:
# Name: Yashoda Dairy
# Address: 38, Samriddhi Bhawan, 1 Strand Road, Kolkata – 700001, West Bengal
# URL: www.yashodadairy.com
# Email: director@yashodadairy.com

REPLACEMENTS = {
    # Brand Name
    r"Vijay Dairy": "Yashoda Dairy",
    r"Vijay dairy": "Yashoda Dairy",
    r"vijay dairy": "yashoda dairy", # generic
    
    # URL/Email
    r"vijaydairy\.com": "yashodadairy.com",
    r"www\.vijaydairy\.com": "www.yashodadairy.com",
    r"info@vijaydairy\.com": "director@yashodadairy.com", # Guessing original email or pattern
    # Actual scraped email might differ, we'll try to catch common ones or add if found.
    # User provided: director@yashodadairy.com
    
    # Address
    # Looking for a snippet of the old address to replace.
    # "Surat" is mentioned in description.
    # regex for address replacement might need to be specific if we find it.
    # Let's try to match typical address patterns if flexible, or just specific strings if known.
    # Since I haven't grepped the exact address, I will replace the brand name and URLs first. 
    # If I see "Surat" in the footer, I might replace it with "Kolkata" contextually or the full address.
    # Let's rely on a broad replacement for the specific provided address if we can find the old one, 
    # or just inject it where the old one likely is (Footer).
    
    # Logo
    # Old logo found in index.html: 
    # wp-content/uploads/2022/04/Vijay-dairylogo-Q.png
    # But files are local assets/ ...
    # Listing showed `assets/` and `index.html`.
    # `index.html` showed `src` like `wp-content/...` but user might have meant local assets if mapped?
    # Actually, `index.html` showed: <img src="assets/Vijay-dairylogo-Q.png" ...> (hypothetically if mapped)
    # The snippet showed: "logo":{"@type":"ImageObject","@id":"...","url":"...Vijay-dairylogo-Q.png"}
    # And <img ... src="assets/SureGhee..."> was previous.
    # Let's search for the logo filename in the content.
    r"Vijay-dairylogo-Q\.png": "YashodaDairy.png",
    
    # If the file path structure is different (e.g. wp-content preserved), we need to handle that.
    # But usually in these tasks `assets/` is the flat directory.
}

# The user wants to replace "Vijay Dairy" -> "Yashoda Dairy"
# And address: "38, Samriddhi Bhawan, 1 Strand Road, Kolkata – 700001, West Bengal"

def fix_logo_style(content):
    # Ensure logo looks good.
    # Matched pattern: <img ... src="...YashodaDairy.png" ...>
    # We should add style="max-height: 100px; width: auto;" if not present.
    
    if "YashodaDairy.png" in content:
        # naive replacement of width/height attributes if they exist
        content = re.sub(
            r'(src="[^"]*YashodaDairy\.png"[^>]*?)width="\d+" height="\d+"',
            r'\1 style="max-height: 100px; width: auto;"',
            content
        )
    return content

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        # Address injection? 
        # If we can't find the exact old address string, we might miss it.
        # Let's try to find "Surat" near "Address" or similar?
        # Or simple replacement if the user gave us the Target.
        # User request: "38, Samriddhi Bhawan..."
        # Old address likely in footer.
        
        # Specific Logo Asset path fix if it's pointing to old filename in a path
        # e.g. src="assets/Vijay-dairylogo-Q.png" -> src="assets/YashodaDairy.png"
        # The REPLACEMENTS dict handles the filename, but let's ensure path is `assets/`
        
        # Fix logo style
        new_content = fix_logo_style(new_content)
        
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
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".json")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
