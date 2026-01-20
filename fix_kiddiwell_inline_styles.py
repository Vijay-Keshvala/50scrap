import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com"

# Common attributes that might contain image paths
ATTRS_TO_FIX = [
    'srcset', 'data-src', 'data-src-rs-ref', 'data-thumb', 'data-lazy', 'href'
]

def fix_inline_styles_and_attrs(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # 1. Fix inline styles: style="... url('...Kiddi Well...') ..."
        # Pattern: look for url(...) inside style attributes or just generally in HTML 
        # (since we are replacing specific broken text, global replacement of the path part is safer if specific)
        
        # Strategy: Find any occurrence of "Kiddi Well" inside a path-like string
        # We look for /...Kiddi Well.../ patterns commonly found in assets
        
        # Matches: assets/Kiddi Well_something.ext OR wp-content/.../Kiddi Well...
        # We want to replace "Kiddi Well" -> "balvvardhak" IN THESE PATHS ONLY.
        
        # Regex to find paths containing "Kiddi Well" that are likely assets
        # It looks for: (assets/ OR wp-content/) ... Kiddi Well ...
        # and captures the whole match to replace the "Kiddi Well" part.
        
        def replace_match(match):
            full_match = match.group(0)
            # Don't replace the main logo or existing valid files if any
            if "assets/Kiddiwell.png" in full_match:
                return full_match
                
            # Heuristic replacement
            # "Kiddi Well" -> "balvvardhak" (lowercase usually for these files based on previous ls)
            # OR "Kiddi Well" -> "Balvvardhak" (if original was capitalized)
            
            # Based on previous ls, most team files were like: balvvardhak_foods_team_...
            # So "Kiddi Well_foods_team" -> "balvvardhak_foods_team"
            # It seems "Kiddi Well" replaced "Balvvardhak" (case insensitive match in first script?)
            # or "Balvvardhak Foods" -> "Kiddi Well"
            
            # Let's try replacing "Kiddi Well" with "balvvardhak" first
            fixed = full_match.replace("Kiddi Well", "balvvardhak")
            
            # Check if this fixed path exists (if it's local assets/)
            if "assets/" in fixed:
                local_path = fixed.split("assets/")[-1] # get part after assets/
                # assets/balvvardhak...
                # actually full path relative to BASE_DIR/assets
                # But fixed is just the string in HTML.
                
                # We can't easily verify existence of every match without parsing structure.
                # But we know "Kiddi Well" is definitely wrong for these assets.
                pass
            
            return fixed

        # Pattern: (assets\/|wp-content\/)[^"'\s\)]*Kiddi Well[^"'\s\)]*
        # matches paths starting with assets/ or wp-content/ containing Kiddi Well
        path_pattern = re.compile(r'(assets\/|wp-content\/)[^"\'\s\)]*Kiddi Well[^"\'\s\)]*')
        
        content = path_pattern.sub(replace_match, content)
        
        # 2. Also fix specific "Kiddi Well" in filenames that might not start with assets/ if relative?
        # But mostly they do.
        
        # 3. Fix external URLs reverted to balvvardhak.com in HTML too (attrs)
        # e.g. href="...kiddiwell.com/wp-content..." for images
        # We only want to revert for RESOURCES, not links to homepage.
        # Resource extensions: .jpg, .png, .webp, .css, .js
        
        def revert_external_asset_domain(match):
            url = match.group(0)
            if "kiddiwell.com" in url:
                return url.replace("kiddiwell.com", "balvvardhak.com")
            return url

        # Regex for external Resource URLs
        # http...kiddiwell.com... (jpg|png|webp|css|js)
        ext_res_pattern = re.compile(r'https?:\/\/[^\s"\']*?kiddiwell\.com[^\s"\']*?\.(?:jpg|jpeg|png|webp|css|js|gif)', re.IGNORECASE)
        content = ext_res_pattern.sub(revert_external_asset_domain, content)
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm", ".css", ".js", ".json")):
                fix_inline_styles_and_attrs(os.path.join(root, file))

if __name__ == "__main__":
    main()
