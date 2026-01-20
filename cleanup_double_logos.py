import os
import re

SKYBLUE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/skyblue.in"

def cleanup_double_logos(directory):
    print(f"Cleaning up double logos in: {directory}")
    
    # The string we inserted (simplified for matching, beware of whitespace/newlines)
    # We inserted: <img src="assets/Classi_Office_Logo.png" alt="Classi Office" style="max-height: 80px; width: auto;">
    # It might be on separate lines.
    
    # We'll use a regex to find two of these in a row, separated by whitespace/newlines.
    # We'll escape the special chars in the tag just in case, but we constructed it ourselves.
    
    logo_tag_str = r'<img src="assets/Classi_Office_Logo.png" alt="Classi Office" style="max-height: 80px; width: auto;">'
    
    # Pattern: logo_tag + whitespace + logo_tag
    # We want to replace it with just one logo_tag.
    double_logo_pattern = re.compile(re.escape(logo_tag_str) + r'\s*' + re.escape(logo_tag_str), re.DOTALL)
    
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
                    
                    if double_logo_pattern.search(content):
                        # Replace all double occurrences with a single one (and keep the whitespace? 
                        # Actually if we replace with just one tag, we lose the whitespace in between? 
                        # Usually the whitespace in between was just indentation. We can probably just output the tag + newline if we want, 
                        # or just the tag. 
                        # Let's replace with a single tag.
                        
                        new_content = double_logo_pattern.sub(logo_tag_str, content)
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed double logo in: {path}")
                        files_updated += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Cleanup Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    cleanup_double_logos(SKYBLUE_DIR)
