import os
import re
import shutil

# Configuration
BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data"
TARGET_DIR = os.path.join(BASE_DIR, "choconnuts.in")
ASSETS_DIR = os.path.join(TARGET_DIR, "assets")
IMAGES_DIR = os.path.join(TARGET_DIR, "images")
SOURCE_LOGO = os.path.join(BASE_DIR, "images", "Candy Berries.png")

NEW_DETAILS = {
    "name": "Candy Berries",
    "address": "304/405, Kaji Nazrul Islam Sarani, VIP Road, Raghunathpur, Kolkata – 700059, West Bengal",
    "email": "info@candyberries.com",
    "url": "www.candyberries.com",
    "url_clean": "candyberries.com"
}

OLD_DETAILS_REGEX = [
    r"Choco[\s-]*n[\s-]*Nuts",
    r"info@choconnuts\.in",
    r"choconnuts\.in",
    r"A 404, Western Courtyard, Opposite JK Hospital, Kolar Road, Bhopal" # Approximate old address
]

def setup_images():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    
    target_logo = os.path.join(IMAGES_DIR, "Candy Berries.png")
    if os.path.exists(SOURCE_LOGO):
        shutil.copy2(SOURCE_LOGO, target_logo)
        print(f"Copied logo to {target_logo}")
    else:
        print(f"Warning: Source logo not found at {SOURCE_LOGO}")

def map_assets():
    """
    Creates a mapping from 'original filename' (found in URL) to 'local asset filename'.
    The scraper seems to append `_<hashtail>` or similar to filenames in assets/.
    """
    if not os.path.exists(ASSETS_DIR):
        return {}

    asset_map = {}
    local_assets = os.listdir(ASSETS_DIR)
    
    # Heuristic: Match base filenames. 
    # Remote: wp-content/plugins/.../style.min.css?ver=1.2.3 -> base: style.min.css
    # Local: style_min_0352.css
    
    for local_file in local_assets:
        # Simplify local filename to try and match remote base
        # heuristic: replace underscores with dots? No, usually scraper replaces special chars with _.
        # Let's try to match by significant parts.
        pass

    return local_assets

def find_local_match(remote_url, local_assets):
    """
    Tries to find a matching local file for a remote URL.
    """
    if not remote_url or "choconnuts.in" not in remote_url:
        return None
        
    # Extract filename from URL
    # e.g. https://choconnuts.in/wp-content/themes/siteorigin-corp/style.min.css?ver=1.2.3
    base_name = remote_url.split('?')[0].split('/')[-1] # style.min.css
    
    if not base_name:
        return None

    name_no_ext = os.path.splitext(base_name)[0] # style.min
    ext = os.path.splitext(base_name)[1] # .css
    
    # Normalize for matching: style.min -> style_min
    normalized_base = name_no_ext.replace('.', '_').replace('-', '_')
    
    # Try to find a file in local_assets that starts with this normalized base
    # Local files often have extra suffixes like _0352.css
    
    potential_matches = []
    for asset in local_assets:
        if asset.endswith(ext):
            # Check if asset starts with the normalized base
            # Be careful not to match 'style_min' with 'style_min_extended' if both exist, but usually unique enough
            # Strict check: asset starts with normalized_base
            if asset.startswith(normalized_base):
                potential_matches.append(asset)
    
    # If multiple matches, maybe picking one is fine?
    if potential_matches:
        # Pick the shortest or first?
        # scraper usually appends hash at end.
        return os.path.join("assets", potential_matches[0])
    
    return None

def process_file(file_path, local_assets):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    original_content = content

    # 1. Fix Asset Links
    # Regex to find https://choconnuts.in URLs in src or href
    # We want to capture the full URL
    url_pattern = re.compile(r'(src|href)=["\'](https?://choconnuts\.in/[^"\']+)["\']')
    
    def replace_url(match):
        attr = match.group(1)
        url = match.group(2)
        
        local_path = find_local_match(url, local_assets)
        if local_path:
            print(f"  Fixed link: {os.path.basename(url)} -> {local_path}")
            return f'{attr}="{local_path}"'
        else:
            # If no local match, return original (or we could try to just comment it out?)
            # For now, keep original to avoid breaking layout completely if missing
            return match.group(0)

    content = url_pattern.sub(replace_url, content)

    # 2. Rebrand Text
    # Name
    content = re.sub(r"Choco-n-Nuts", NEW_DETAILS["name"], content, flags=re.IGNORECASE)
    content = re.sub(r"Choco n Nuts", NEW_DETAILS["name"], content, flags=re.IGNORECASE)
    content = re.sub(r"Choco-N-Nuts", NEW_DETAILS["name"], content, flags=re.IGNORECASE)
    
    # Email
    content = re.sub(r"info@choconnuts\.in", NEW_DETAILS["email"], content, flags=re.IGNORECASE)
    
    # URL Text
    content = re.sub(r"choconnuts\.in", NEW_DETAILS["url_clean"], content, flags=re.IGNORECASE)
    
    # Address (Searching for parts of the old address to be safe)
    # The old address might be split across lines or tags, so simple regex might fail.
    # We'll try a specific replacement if we know the exact string, otherwise specific substitutions.
    # Inspecting index.html earlier showed: "A 404, Western Courtyard, Opposite JK Hospital, Kolar Road, Bhopal"
    # We will try to replace "Bhopal" related address text if found in a specific context, 
    # but a simple replace of the known string is safest.
    content = content.replace("A 404, Western Courtyard, Opposite JK Hospital, Kolar Road, Bhopal", NEW_DETAILS["address"])
    
    # 3. Logo Update
    # Find img with old logo src. 
    # We'll look for the specific filename we saw in the assets list or in the index.html content
    # "Logo-Choco-n-nuts-e1596041877265.png" or similar.
    # Or just replace any image that looks like a logo? Safer to check alt text or filename.
    
    # Heuristic: Replace ANY image that has 'Logo' in its filename (from choconnuts) with new logo
    # Regex for src="...Logo...png"
    logo_pattern = re.compile(r'src=["\'][^"\']*Logo[^"\']*\.png["\']', re.IGNORECASE)
    
    def replace_logo(match):
        print("  Updating logo...")
        return f'src="images/Candy Berries.png" style="max-width: 200px; height: auto;"'
    
    content = logo_pattern.sub(replace_logo, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved changes to {file_path}")
    else:
        print(f"  No changes made to {file_path}")

def main():
    setup_images()
    local_assets = map_assets()
    
    # Process index.html
    index_path = os.path.join(TARGET_DIR, "index.html")
    if os.path.exists(index_path):
        process_file(index_path, local_assets)
    
    # Process other HTML files
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".html") and filename != "index.html":
            process_file(os.path.join(TARGET_DIR, filename), local_assets)

if __name__ == "__main__":
    main()
