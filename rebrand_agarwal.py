import os
import re

# Base directory
BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/ksbakers.com"
LOGO_PATH = "assets/Agarwal_Bakery.png"

# New details
NEW_NAME = "Agarwal Bakery"
NEW_ADDRESS = "Shop No.-25, ADA Market, Ramghat Road, Swarn Jayanti Nagar, Aligarh – 202001, Uttar Pradesh"
NEW_EMAIL = "report@agarwalbakery.com"
NEW_DOMAIN = "agarwalbakery.com"

# Regex for Address
# We need to match what it looks like *after* potentially some partial replacements or just be robust.
# The previous script might have already changed "KS Bakers" to "Agarwal Bakery".
# Original: "KS Bakers Pvt. Ltd., Manufacturing Unit<small>Sreeram Nagar Colony, Patancheruvu, Hyderabad, Telangana&nbsp;502319</small>"
# Current in file (likely): "Agarwal Bakery Pvt. Ltd., Manufacturing Unit<small>Sreeram Nagar Colony, Patancheruvu, Hyderabad, Telangana&nbsp;502319</small>"
ADDRESS_REGEX = r"(KS Bakers|Agarwal Bakery) Pvt\. Ltd\., Manufacturing Unit<small>Sreeram Nagar Colony, Patancheruvu, (Hyderabad|Aligarh), (Telangana|Uttar Pradesh)(&nbsp;| )502319</small>"

# Regex for Logo
# Matches the filename regardless of the domain prefix, as domain might have changed
# Filenames: KS-Bakers-logo-V1.1.png, KS-Bakers-Footer-logo-white.png
LOGO_REGEX = r"https?://(www\.)?(ksbakers\.com|agarwalbakery\.com)/wp-content/uploads/2023/11/(KS-Bakers-logo-V1\.1\.png|KS-Bakers-Footer-logo-white\.png)"


def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # 1. Fix Logo (specific regex)
        content = re.sub(LOGO_REGEX, LOGO_PATH, content)

        # 2. Fix Address (specific regex)
        # We replace the entire matched block with the new address format
        replacement_address = f"Agarwal Bakery<small>{NEW_ADDRESS}</small>"
        content = re.sub(ADDRESS_REGEX, replacement_address, content)

        # 3. Location & Text Replacements
        # We need to handle "Hyderabad" -> "Aligarh" but be careful not to break other things.
        # Given the context "cake shops in Hyderabad", "Bakery in Ameerpet", etc.
        location_replacements = {
            "Hyderabad": "Aligarh",
            "Telangana": "Uttar Pradesh",
            "Ameerpet": "Aligarh",
            "Patancheruvu": "Aligarh",
            "Sreeram Nagar Colony": "Swarn Jayanti Nagar",
             # Fix the "Best Bakery in Hyderabad" which might have become "Best Bakery in Aligarh" in my previous partial run, 
             # but let's just ensure it's correct.
            "KS Bakers": "Agarwal Bakery",
            "KSBakers": "Agarwal Bakery",
            "ksbakers.com": "agarwalbakery.com",
            "online@ksbakers.com": NEW_EMAIL,
            "online@agarwalbakery.com": NEW_EMAIL, # In case domain swap happened but user prefix didn't match
        }

        for old, new in location_replacements.items():
            content = content.replace(old, new)
            
        # 4. Clean up any "Agarwal Bakery Pvt. Ltd." if it wasn't caught by regex (e.g. copyright)
        # "Agarwal Bakery Pvt. Ltd." -> "Agarwal Bakery" (optional, or keep it if it sounds official)
        # But per requirements: Name is "Agarwal Bakery".
        
        # 5. Fix any double-replaced things or specific artifacts if needed
        # (None obvious, but good to be safe)

        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
