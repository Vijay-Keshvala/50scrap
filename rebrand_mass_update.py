import os
import re

# Configuration
SKYBLUE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/skyblue.in"
ASHYANI_DIR = "/Users/vijaykeshvala/Documents/scraped_data/ashyani.com"

# Skyblue Replacements
def rebrand_skyblue(content):
    # 1. Logo Replacement (Generalizing regex to capture various attributes)
    #    Target: <img ... src="...skyblue_small_logo.svg"...>
    #    Replace with: <img src="assets/Classi_Office_Logo.png" alt="Classi Office" ... style="max-height: 80px; width: auto;">
    
    # Regex to find the logo image tag. It captures the surrounding tag structure.
    # We look for 'skyblue_small_logo' in the src, allowing for suffixes like '_7339'.
    logo_pattern = re.compile(r'<img[^>]*src="[^"]*skyblue_small_logo[^"]*"[^>]*>', re.IGNORECASE)
    
    # We will replace it with a standard Classi Office logo tag.
    # Note: We need to respect relative paths if possible, but for scraped sites, 'assets/' at root might be common.
    # A safer bet is to use the absolute path from the root or assume the assets folder is in the same relative location properly.
    # However, since we are doing mass replace, let's stick to the one that worked for index.html but be mindful of subdirectory depth?
    # Actually, for scraped sites, index.html is root. Subpages might be in subfolders. 
    # If subpages are in subfolders, 'assets/...' might break. 
    # 'assets/' works for root. For others it might need '../assets/'.
    # A simple fix: Use absolute path if the server supports it, or check file depth.
    # For now, let's assume flat structure or 'assets/' works (often scraped sites flatten or keep structure).
    # Let's check file paths from the 'find' command output later. Assuming flat or relative correctness for now.
    
    new_logo_tag = '<img src="assets/Classi_Office_Logo.png" alt="Classi Office" style="max-height: 80px; width: auto;">'
    content = logo_pattern.sub(new_logo_tag, content)

    # 2. Text Replacements
    content = content.replace("Skyblue Stationery Mart", "Classi Office")
    content = content.replace("Skyblue Stationery", "Classi Office")
    content = content.replace("skyblue.in", "classioffice.com")
    
    # 3. Footer Address (Specific Pattern?)
    #    We can just replace the specific address string if it exists.
    old_address_part = "175, N Ambazari Road" # This was Ashyani. Wait, Skyblue address?
    #    Skyblue address was "Parth Complex, ... Ahmedabad".
    #    Let's rely on the text replacement unless we need specific HTML block replacement.
    
    return content

# Ashyani Replacements
def rebrand_ashyani(content):
    # 1. Logo Replacement
    #    Target: Complex span with two images (desktop/transparent)
    #    The regex needs to be robust. 
    #    The index.html had a structure like <span class="site-logo-img">...</span>
    #    Let's try to replace the inner <a> or <img> tags if regex allows, or the whole block.
    #    Warning: Spanning multiple lines makes regex harder.
    
    # Simplified approach: Look for the specific image filenames and replace the IMG tag.
    # Old logos: 'cropped_PhotoRoom_...' (transparent) and 'cropped_cropped_wp_...' (desktop)
    
    new_logo_tag = '<img src="assets/Sporttiva_Logo.png" class="custom-logo" alt="Sporttiva" decoding="async" style="max-width: 250px; width: auto; height: auto;">'
    
    # Regex for Logo 1 (Transparent)
    content = re.sub(r'<img[^>]*src="[^"]*cropped_PhotoRoom_[^"]*"[^>]*>', new_logo_tag, content)
    
    # Regex for Logo 2 (Desktop)
    content = re.sub(r'<img[^>]*src="[^"]*cropped_cropped_wp_[^"]*"[^>]*>', new_logo_tag, content)

    # 2. Text Replacements
    content = re.sub(r'Ashyani\.com', 'Sporttiva.com', content, flags=re.IGNORECASE)
    content = re.sub(r'Ashyani Sports', 'Sporttiva', content, flags=re.IGNORECASE)
    content = content.replace("Welcome To Ashyani", "Welcome To Sporttiva")
    
    # 3. Address Injection (Footer)
    #    The specific "Footer Widget 3" replacement we did in index.html might not exist on all pages 
    #    or be harder to find. However, the footer text itself might be consistent.
    #    Let's text-replace the old address if found?
    #    Old address: "179, N Ambazari Road..." 
    #    Wait, Ashyani *is* the one with Ambazari road. 
    #    The goal is to Inject the NEW address if it's missing or replace the old.
    #    If the footer was empty (as in index.html), we need to find the container.
    #    Container: <div class="wp-block-column is-vertically-aligned-center ... style="flex-basis:100%"></div>
    
    #    Regex to find empty footer column:
    #    <div class="[^"]*wp-block-column[^"]*"[^>]*style="flex-basis:100%"></div>
    footer_regex = re.compile(r'(<div class="[^"]*wp-block-column[^"]*"[^>]*style="flex-basis:100%">)(</div>)', re.IGNORECASE)
    
    new_address_block = '''
    <p><strong>Sporttiva</strong><br>
    179, N Ambazari Road, Ramdaspeth, Nagpur, Maharashtra — 440010<br>
    Email: <a href="mailto:business@sporttiva.com">business@sporttiva.com</a></p>
    '''
    
    # Only replace if we haven't already (check for Sporttiva string)
    if "179, N Ambazari Road" not in content and "Sporttiva" not in content:
         content = footer_regex.sub(r'\1' + new_address_block + r'\2', content)

    return content


def process_directory(directory, rebrand_func):
    print(f"Processing directory: {directory}")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                # Skip index.html since we already did it? 
                # Or just re-run it (idempotency checks inside func would be good).
                # User said "change it in all the pages", implies including index if not perfectly done, 
                # but we know index is done. Let's process all to be safe and ensure consistency.
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    new_content = rebrand_func(original_content)
                    
                    if new_content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {path}")
                    else:
                        print(f"No changes: {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    print("Starting Mass Rebrand...")
    process_directory(SKYBLUE_DIR, rebrand_skyblue)
    process_directory(ASHYANI_DIR, rebrand_ashyani)
    print("Mass Rebrand Complete.")
