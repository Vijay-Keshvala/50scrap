import os
import re

SOURCE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com"

TEXT_REPLACEMENTS = {
    "Prakash Namkeen": "Arora Namkeen",
    "PRAKASH NAMKEEN": "ARORA NAMKEEN",
    "Prakesh Namkeen": "Arora Namkeen", # Typo seen in footer copyright
    "www.prakashnamkeen.com": "www.aroranamkeen.com",
    "prakashnamkeen.com": "aroranamkeen.com", # Be careful with this one, might break CDN
    "Indore": "Aligarh", # Careful with this too? User said Aligarh.
}

# Specific address replacement to be safe
OLD_ADDRESS_REGEX = r"33-B, Laxmibai Nagar, Industrial Area,<br>\s*Fort Road, Indore – 452007"
NEW_ADDRESS = "5/2, Kanhaiya Building, Masoodabad, Holi Chowk,<br>Aligarh – 202001, Uttar Pradesh"

LOGO_REPLACEMENT = {
    # Replace the full CDN URL with the local asset path. 
    # Regex to capture the CDN prefix and query parameters.
    # Note: previous run might have already changed the filename to "Arora Namkeen.png", so we catch that too.
    r"//prakashnamkeen\.com/cdn/shop/files/(PRAKASH_NAMKEEN_LOGO1|Arora Namkeen|Arora_Namkeen)\.png(\?v=\d+)?": "assets/Arora_Namkeen.png",
    "PRAKASH_NAMKEEN_LOGO1.png": "Arora_Namkeen.png", # Fallback
    "assets/Arora Namkeen.png": "assets/Arora_Namkeen.png" # Fix previous replacement containing spaces
}

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    original_content = content
    
    # 1. Logo Replacement
    for old_logo_pattern, new_logo in LOGO_REPLACEMENT.items():
        if "cdn" in old_logo_pattern:
             content = re.sub(old_logo_pattern, new_logo, content)
        else:
             content = content.replace(old_logo_pattern, new_logo)

    # 2. Address Replacement (Regex for potential whitespace diffs)
    content = re.sub(OLD_ADDRESS_REGEX, NEW_ADDRESS, content, flags=re.IGNORECASE)

    # 3. Text Replacements
    for old_text, new_text in TEXT_REPLACEMENTS.items():
        if old_text == "prakashnamkeen.com":
             # Avoid breaking CDN links like //prakashnamkeen.com/cdn/...
             # We only want to replace it if it's NOT followed by /cdn/
             # Using negative lookahead regex
             pattern = r"prakashnamkeen\.com(?!/cdn/)"
             content = re.sub(pattern, new_text, content)
        else:
            content = content.replace(old_text, new_text)
            
    # 4. Email Replacement
    # No specific old email found in quick scan, but user mentioned ceo@aroranamkeen.com
    # I'll look for any mailto: or common email patterns if I knew them, 
    # but for now I'll just rely on the brand name replacement mostly covering it 
    # if the email was info@prakashnamkeen.com -> info@aroranamkeen.com
    # User said "ceo@aroranamkeen.com", replaces what?
    # I'll replace any email found with prakashnamkeen.com domain if found?
    # Or just hardcode if I find the specific email.
    # In footer: "Sign up for Email" form exists.
    
    # 4. Clean up invalid query parameters on local assets
    # Previous replacements might have left &width=... without a ? or just appended to the local path.
    # We want to remove anything starting with & or ? after the .png for local assets.
    # Example: assets/Arora_Namkeen.png&width=138 -> assets/Arora_Namkeen.png
    content = re.sub(r"(assets/Arora_Namkeen\.png)(&amp;|&)(width|v)=[^\"'\s]*", r"\1", content)

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    count = 0
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))
                count += 1
    print(f"Processed {count} files in {SOURCE_DIR}")

if __name__ == "__main__":
    main()
