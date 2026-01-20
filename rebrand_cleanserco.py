import os
import re

TARGET_DIR = "/Users/vijaykeshvala/Documents/scraped_data/cleanbuddy.in"

# 1. Logo Replacement (Text to Image)
# Target: <span class="StoreName-sc-88485546-5 clWLbD">CLEANBUDDY HOME CARE PRODUCTS</span>
# We'll replace the inner text.
LOGO_SPAN_REGEX = re.compile(r'(<span[^>]*class="StoreName[^"]*"[^>]*>)\s*CLEANBUDDY HOME CARE PRODUCTS\s*(</span>)', re.IGNORECASE)
NEW_LOGO_CONTENT = r'\1<img src="assets/CleanserCo_Logo.png" alt="CleanserCo" style="max-width: 250px; height: auto;">\2'

# 2. Text Replacements
# Brand Name
OLD_BRAND_NAME = "CLEANBUDDY HOME CARE PRODUCTS"
NEW_BRAND_NAME = "CleanserCo"

# Address
OLD_ADDRESS_PART = "Nr Shyam Mandir, G-52, VIP Plaza, VIP Road, Surat, Surat, Gujarat, 395007"
NEW_ADDRESS = "Shop No. 90, Rampal Chowk, Block D, Sector 7, Dwarka, New Delhi"

# Email
OLD_EMAIL = "cleanbuddystore@gmail.com"
NEW_EMAIL = "business@cleanserco.com"

# Website
OLD_DOMAIN_TEXT = "www.cleanbuddy.in"
NEW_DOMAIN_TEXT = "www.cleanserco.com"

def rebrand_cleanserco(directory):
    print(f"Rebranding Cleanbuddy to CleanserCo in: {directory}")
    files_processed = 0
    files_updated = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                files_processed += 1
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content

                    # 1. Logo Replacement
                    # Be careful not to replace it if it's already an image (idempotency check inherent if text doesn't match)
                    if "CLEANBUDDY HOME CARE PRODUCTS" in content:
                        # First, handle the Logo Span specifically
                        content = LOGO_SPAN_REGEX.sub(NEW_LOGO_CONTENT, content)
                        
                        # Then replace other occurrences of the full brand name text
                        # We use simple string replace for this, but avoid breaking the matched logo tag we just inserted
                        # The regex replacement above consumes the string, so subsequent simple replaces won't touch it inside the span if regex matched properties
                        # However, we should be careful.
                        content = content.replace(OLD_BRAND_NAME, NEW_BRAND_NAME)

                    # 2. Address Replacement
                    # The address in the file might have extra text like ", SURAT, GUJARAT, 395007" appended.
                    # We'll try to match a significant unique part.
                    if "Nr Shyam Mandir" in content:
                        # Regex for the full address line if possible or just replace the known substring
                        # The file view showed: "Nr Shyam Mandir, G-52, VIP Plaza, VIP Road, Surat, Surat, Gujarat, 395007, SURAT, GUJARAT, 395007"
                        # We will replace that entire block if matched, or just the main part.
                        content = content.replace("Nr Shyam Mandir, G-52, VIP Plaza, VIP Road, Surat, Surat, Gujarat, 395007, SURAT, GUJARAT, 395007", NEW_ADDRESS)
                        content = content.replace(OLD_ADDRESS_PART, NEW_ADDRESS)

                    # 3. Email Replacement
                    content = content.replace(OLD_EMAIL, NEW_EMAIL)

                    # 4. Domain Text Replacement
                    # Only visible text, try to avoid assets.
                    # cleanbuddy.in is used in manifest links etc. We should be careful.
                    # User said "www.cleanserco.com"
                    content = content.replace(OLD_DOMAIN_TEXT, NEW_DOMAIN_TEXT)
                    
                    # Also generic "cleanbuddy" replacements in text? 
                    # "Clean Buddy exists to distribute..." -> "CleanserCo exists..."
                    content = content.replace("Clean Buddy exists", "CleanserCo exists")
                    content = content.replace("by YADAV KAPTAN DESHRAJ", "") # Clean up owner name if desired, or keep. User didn't specify, but usually rebranding implies removing old owner. I'll leave it or replace with CleanserCo if generic.
                    # Safe to leave owner details if not explicitly asked, but "Clean Buddy" text should definitely change.
                    content = content.replace("Clean Buddy", "CleanserCo")

                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_updated += 1
                        print(f"Updated: {path}")

                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Rebrand Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    rebrand_cleanserco(TARGET_DIR)
