import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com"

def fix_images(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Pattern to find src attributes containing "Kiddi Well"
        # We want to capture the full filename to check if it exists or needs fixing
        # Group 1: the quote char, Group 2: the path
        pattern = r'src=(["\'])([^"\']*Kiddi Well[^"\']*?)(["\'])'
        
        matches = re.findall(pattern, content)
        
        for quote, src_path, quote_end in matches:
            # Skip the main logo if it is correct (though user said existing images shouldn't be removed, 
            # we replaced the main logo intentionally. But other assets should not be broken).
            # Our main logo is assets/Kiddiwell.png. If the path is exactly that, skip.
            if "assets/Kiddiwell.png" in src_path:
                continue
                
            # If the file doesn't exist, it's likely broken.
            full_abs_path = os.path.join(BASE_DIR, src_path)
            
            if not os.path.exists(full_abs_path):
                # Try to guess the original filename
                # Strategy: Replace "Kiddi Well" with "balvvardhak" (lower) or "Balvvardhak"
                
                # Try lowercase "balvvardhak"
                candidate_1 = src_path.replace("Kiddi Well", "balvvardhak")
                # Try lowercase "balvvardhak foods" if likely
                candidate_2 = src_path.replace("Kiddi Well", "Balvvardhak")
                
                # Check if these exist
                path_1 = os.path.join(BASE_DIR, candidate_1)
                path_2 = os.path.join(BASE_DIR, candidate_2)
                
                replacement = None
                if os.path.exists(path_1):
                    replacement = candidate_1
                elif os.path.exists(path_2):
                    replacement = candidate_2
                else:
                    # Try replacing "Kiddi Well" with "Balvvardhak" text variations
                    # The script replacer probably did "Balvvardhak Foods" -> "Kiddi Well"
                    # So maybe the original was "balvvardhak_foods" -> "Kiddi Well_foods"?
                    # Let's try replacing "Kiddi Well" with "balvvardhak" ignoring case in the match to finding file?
                    pass

                if replacement:
                    print(f"Fixing broken image: {src_path} -> {replacement}")
                    content = content.replace(src_path, replacement)
                else:
                    print(f"Could not find original file for: {src_path}")

        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def fix_css_urls(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Pattern to find url(...) in CSS
        # url( path ) or url('path') or url("path")
        # capture the content inside url()
        pattern = r'url\((["\']?)([^"\')]+)(["\']?)\)'
        
        matches = re.findall(pattern, content)
        
        for quote_start, src_path, quote_end in matches:
            new_path = src_path
            
            # Case 1: "Kiddi Well" in filename (local asset)
            if "Kiddi Well" in src_path and "assets/Kiddiwell.png" not in src_path:
                 # Try restoration logic similar to HTML
                 # Check relative to css file location? Scrapers usually put assets relative to root or same dir.
                 # Assuming simplistic check first
                 if "balvvardhak" not in src_path.lower(): # if it has Kiddi Well and not balvvardhak
                     # Try to find original file
                     # If absolute URL (http), revert domain/path part
                     if src_path.startswith("http"):
                         if "kiddiwell.com" in src_path:
                             # Revert to balvvardhak.com for asset path
                             # This assumes external host structure
                             new_path = src_path.replace("kiddiwell.com", "balvvardhak.com")
                     else:
                         # Local file potentially
                         # Try reverting "Kiddi Well" -> "balvvardhak"
                         candidate = src_path.replace("Kiddi Well", "balvvardhak")
                         # For CSS, path is relative to CSS file usually.
                         # But let's just do text replacement if it looks like the broken pattern
                         new_path = candidate
                         
            # Case 2: "kiddiwell.com" in path for external assets (likely broken if it was balvvardhak.com)
            elif "kiddiwell.com" in src_path and "http" in src_path:
                 # e.g. https://whysocialnetwork.com/kiddiwell.com/...
                 # We should revert this to balvvardhak.com if it's an asset
                 new_path = src_path.replace("kiddiwell.com", "balvvardhak.com")

            if new_path != src_path:
                print(f"Fixing CSS URL: {src_path} -> {new_path}")
                # Use simple string replace to be safe, but be careful of overlapping
                content = content.replace(src_path, new_path)

        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated CSS: {filepath}")

    except Exception as e:
        print(f"Error processing CSS {filepath}: {e}")

def process_file(filepath):
    if filepath.endswith((".html", ".htm")):
        fix_images(filepath)
    elif filepath.endswith(".css"):
        fix_css_urls(filepath)


def main():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".js", ".css", ".json")):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
