import os
import re

SOURCE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/sahnibakery.com"

OLD_ADDRESS_PATTERN = r"Circular Road, Near Ripudaman College, Nabha, Punjab|Kanika Garden, Rajpura, Punjab|Bakery in Punjab"
NEW_ADDRESS = "YMCA Building, Ground & 4th Floor, Quarter Gate, Rastapeth, Pune – 411011, Maharashtra"

# Using a more specific pattern for the footer address might be needed if the above is too broad or split across tags,
# but based on grep, they seemed to be in strong tags.
# Let's try to match the known specific strings found in grep.
ADDRESS_REPLACEMENTS = {
    "Circular Road, Near Ripudaman College, Nabha, Punjab": NEW_ADDRESS,
    "Kanika Garden, Rajpura, Punjab": NEW_ADDRESS,
    "Bakery in Punjab": "Bakery in Pune", # Contextual fix
}

TEXT_REPLACEMENTS = {
    "Sahni Bakery": "Crispy Crum",
    "SahniBakery": "Crispy Crum",
    "sahnibakery.com": "crispycrum.com",
    "sahnibakery.in": "crispycrum.com",
    "info@sahnibakery.com": "contact@crispycrum.com", # Guessing old email if present
    "sahni_logo_png_1_600x_0920.png": "Crispy Crum.png", # Filename replacement for logo
}

def rebrand_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original_content = content

    # 1. Text Replacements
    for old, new in TEXT_REPLACEMENTS.items():
        content = content.replace(old, new)

    # 2. Address Replacements
    for old, new in ADDRESS_REPLACEMENTS.items():
        content = content.replace(old, new)
        
    # 3. Special Address Block Replacement (from grep: "304/405, Kaji Nazrul Islam Sarani...") 
    # Wait, that was choconnuts. Sahni had "Circular Road..."
    # We already added that to ADDRESS_REPLACEMENTS.

    # 4. Email Replacement (Regex for safety against variations)
    # content = re.sub(r"\b[A-Za-z0-9._%+-]+@sahnibakery\.com\b", "contact@crispycrum.com", content, flags=re.IGNORECASE)

    # 5. Logo src specific fix (if simple filename replace isn't enough)
    # The filename replacement above "sahni_logo_png_1_600x_0920.png" -> "Crispy Crum.png" 
    # should handle: src="assets/sahni_logo_png_1_600x_0920.png" -> src="assets/Crispy Crum.png"
    
    # 6. Title and Meta tag cleanup (Regex to ensure clean replacement)
    content = content.replace("Oldest Bakery Since 1947", "Fresh Delights Everyday")


    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def process_directory(directory):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                rebrand_file(os.path.join(root, file))
                count += 1
    print(f"Processed {count} HTML files in {directory}")

if __name__ == "__main__":
    process_directory(SOURCE_DIR)
