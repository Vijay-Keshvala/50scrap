import os
import re

TARGET_DIR = "/Users/vijaykeshvala/Documents/scraped_data/1ststep.com"

# Logo Configuration
# Matches: <img src="assets/logo_150x_4269.png" alt="1st Step">
LOGO_FILENAME_PART = "logo_150x_4269.png"
OLD_LOGO_PATTERN = re.compile(r'<img[^>]*src="[^"]*logo_150x_4269\.png"[^>]*>', re.IGNORECASE)
NEW_LOGO_TAG = '<img src="assets/Kidonix_Logo.png" alt="Kidonix" style="max-width: 200px; width: auto; height: auto;">'

# Footer Replacement
# Matches: <h4 class="footer-title">About Us.</h4><p>Since 2000, 1st Step has been dedicated...</p>
OLD_FOOTER_START = "Since 2000, 1st Step has been dedicated"
NEW_FOOTER_CONTENT = """<h4 class="footer-title">Contact Us.</h4><p><strong>Kidonix</strong><br>
2nd Floor, Bhikaji Cama Place, Safdarjung Enclave, New Delhi, 110066<br>
Email: management@kidonix.com<br>
Website: www.kidonix.com</p>"""

def rebrand_kidonix(directory):
    print(f"Rebranding 1ststep to Kidonix in: {directory}")
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
                    if LOGO_FILENAME_PART in content:
                        content = OLD_LOGO_PATTERN.sub(NEW_LOGO_TAG, content)

                    # 2. Text Replacement
                    # Replace "1st Step" (Title Case) -> "Kidonix"
                    # This handles Page Titles, Meta Descriptions, Alt tags that might not have been caught by logo replace, etc.
                    content = content.replace("1st Step", "Kidonix")
                    content = content.replace("1stStep", "Kidonix") # Just in case
                    
                    # Replace "1ststep.com" in visible text contexts
                    # Avoid replacing it in asset URLs like "//1ststep.com/cdn/..."
                    # We look for " at 1ststep.com" (common in titles) or ">1ststep.com<"
                    content = content.replace(" at 1ststep.com", " at www.kidonix.com")
                    content = content.replace(">1ststep.com<", ">www.kidonix.com<")

                    
                    # 3. Footer Replacement
                    # Note: "1st Step" has already been replaced by "Kidonix" in step 2.
                    # So we search for "Since 2000, Kidonix"
                    if "Since 2000, Kidonix" in content:
                        footer_pattern = re.compile(r'<h4 class="footer-title">About Us\.?</h4>\s*<p>Since 2000, Kidonix.*?</p>', re.DOTALL | re.IGNORECASE)
                        content = footer_pattern.sub(NEW_FOOTER_CONTENT, content)
                    elif "Since 2000, 1st Step" in content:
                        # Fallback if text replacement didn't happen for some reason
                         footer_pattern = re.compile(r'<h4 class="footer-title">About Us\.?</h4>\s*<p>Since 2000, 1st Step.*?</p>', re.DOTALL | re.IGNORECASE)
                         content = footer_pattern.sub(NEW_FOOTER_CONTENT, content)

                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_updated += 1

                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Rebrand Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    rebrand_kidonix(TARGET_DIR)
