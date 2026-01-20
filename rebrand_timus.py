import os
import re

TIMUS_DIR = "/Users/vijaykeshvala/Documents/scraped_data/timus.in"

OLD_LOGO_FILENAME = "timus-logo-black" # Part of the filename to match
NEW_LOGO_TAG = '<img src="assets/RoveBag_Logo.png" alt="Rove Bag" style="max-height: 80px; width: auto;" class="header__heading-logo">'

NEW_ADDRESS = """
<div class="footer__content-bottom-wrapper">
<p style="text-align: center; color: rgba(var(--color-foreground), 0.75); font-size: 1.4rem;">
    Rove Bag<br>
    Classic Business Centre, Khasra No.546, Niranjanpur Pargana, Dehradun, Uttarakhand — 248001<br>
    <a href="mailto:sales@rovebag.com" style="color: inherit; text-decoration: underline;">sales@rovebag.com</a><br>
    <a href="https://www.rovebag.com" style="color: inherit; text-decoration: underline;">www.rovebag.com</a>
</p>
</div>
"""

def rebrand_timus(directory):
    print(f"Rebranding Timus to Rove Bag in: {directory}")
    
    files_processed = 0
    files_updated = 0
    
    # Regex for logo: matches 'timus-logo-black' (hyphens) or 'timus_logo_black' (underscores)
    # Also handles potential 'assets/' prefix or other variations.
    logo_pattern = re.compile(r'<img[^>]*src="[^"]*timus[-_]logo[-_]black[^"]*"[^>]*>', re.IGNORECASE | re.DOTALL)
    
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
                    if logo_pattern.search(content):
                        content = logo_pattern.sub(NEW_LOGO_TAG, content)
                    
                    # 2. Text Replacement (Safe ones)
                    # Avoid replacing "timus.in" in src="//timus.in/..."
                    # We can replace ">Timus<" or "Timus Lifestyle"
                    
                    content = content.replace("Timus Lifestyle", "Rove Bag")
                    content = content.replace("TIMUS", "Rove Bag")
                    content = content.replace("Timus", "Rove Bag")
                    
                    # Replace href="...timus.in..." but NOT src="...timus.in..."?
                    # Actually, let's just replace specific emails or external links if found.
                    content = content.replace("media@timus.in", "sales@rovebag.com")
                    content = content.replace("preeti@timus.in", "sales@rovebag.com")
                    content = content.replace("hr@timuslifestyle.com", "careers@rovebag.com")
                    
                    # 3. Footer Injection
                    # We'll append the address to the copyright section or footer bottom
                    if "footer__content-bottom-wrapper" in content:
                         if "Classic Business Centre" not in content:
                             # Insert before the closing div of footer__copyright or nearby
                             # Let's try to append it after the copyright div
                             content = content.replace('<div class="footer__copyright caption">', '<div class="footer__copyright caption">' + NEW_ADDRESS)
                    
                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        # print(f"Updated: {path}") # Reduce noise
                        files_updated += 1
                        
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Rebrand Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    rebrand_timus(TIMUS_DIR)
