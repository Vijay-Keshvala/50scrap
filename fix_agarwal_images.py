import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/ksbakers.com"

# Regex to find agarwalbakery.com followed by resource paths
# We want to revert these to ksbakers.com
# Resource paths identified: wp-content, wp-includes, wp-json, index.php?rest_route=
# Also checking for direct image extensions if they are strictly on the domain root (unlikely for WP)
# The pattern basically looks for https://agarwalbakery.com/... where ... starts with specific WP paths.

RESOURCE_REGEX = r"https?://(www\.)?agarwalbakery\.com/(wp-content|wp-includes|wp-json|feed|comments)"

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Function to replace the domain back to ksbakers.com for the matched group
        def restore_domain(match):
            # match.group(0) is the full match e.g. https://agarwalbakery.com/wp-content
            # match.group(2) is the path part e.g. wp-content
            # We want https://ksbakers.com/wp-content
            return f"https://ksbakers.com/{match.group(2)}"

        new_content = re.sub(RESOURCE_REGEX, restore_domain, content)
        
        if new_content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed resources in: {filepath}")
            
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
