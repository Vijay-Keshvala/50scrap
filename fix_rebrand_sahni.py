import os

SOURCE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/sahnibakery.com"

# 1. Revert the domain breakages to fix images
REVERT_REPLACEMENTS = {
    "crispycrum.com": "sahnibakery.com", # Restoration of CDN links
    "contact@sahnibakery.com": "contact@crispycrum.com", # Re-fix email if it gets reverted
}

# 2. Apply Text/Logo Rebranding (Safer)
# matches text content primarily
TEXT_REPLACEMENTS = {
    "Sahni Bakery": "Crispy Crum",
    "SahniBakery": "Crispy Crum",
    # "sahnibakery.com": "crispycrum.com", # DO NOT REPLACE DOMAIN GLOBALLY
    "info@sahnibakery.com": "contact@crispycrum.com",
}

# Specific exact string replacements for the address to avoid messing up other things
OLD_ADDRESS_STRINGS = [
    "Circular Road, Near Ripudaman College, Nabha, Punjab",
    "Kanika Garden, Rajpura, Punjab",
    "Bakery in Punjab"
]
NEW_ADDRESS = "YMCA Building, Ground & 4th Floor, Quarter Gate, Rastapeth, Pune – 411011, Maharashtra"

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    original_content = content
    
    # 1. Revert domains first
    for old, new in REVERT_REPLACEMENTS.items():
        content = content.replace(old, new)
        
    # 2. Re-apply Email (since revert might have broken it)
    content = content.replace("contact@sahnibakery.com", "contact@crispycrum.com")
    
    # 3. Apply Text Replacements (Logo was likely handled correctly by previous script if it just targeted the filename string)
    # But let's verify logo src just in case.
    # The previous script replaced 'sahni_logo_png_1_600x_0920.png' with 'Crispy Crum.png'. 
    # That should still be fine as it's a local filename, not a domain.
    # However, if I revert domain, I should ensure I don't revert the logo filename if it contained 'sahnibakery'.
    # Fortunately 'sahnibakery' isn't in 'Crispy Crum.png'.
    
    for old, new in TEXT_REPLACEMENTS.items():
        content = content.replace(old, new)
        
    # 4. Address Fixes
    for addr in OLD_ADDRESS_STRINGS:
        content = content.replace(addr, NEW_ADDRESS)

    # 5. Fix displayed URL text specifically (look for contexts)
    # Replaces "sahnibakery.com" only when it appears as visible text (heuristic)
    # regex for >sahnibakery.com<
    import re
    content = re.sub(r">sahnibakery\.com<", ">www.crispycrum.com<", content)
    content = re.sub(r">www\.sahnibakery\.com<", ">www.crispycrum.com<", content)

    # 6. Ensure Logo is correct
    # The previous script replaced the src. Let's make sure it points to the right local asset.
    # If the src was "assets/Crispy Crum.png", it should stay that way.
    
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed: {filepath}")

def process_directory(directory):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                fix_file(os.path.join(root, file))
                count += 1
    print(f"Processed {count} HTML files in {directory}")

if __name__ == "__main__":
    process_directory(SOURCE_DIR)
