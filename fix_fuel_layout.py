import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/camywafer.com"

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        
        # 1. Fix Logo Style
        # Target the logo tag. It currently looks like: <img src="img/Fuel_Snax.png" class="img-responsive" alt="Primefp">
        # We want: <img src="img/Fuel_Snax.png" class="img-responsive" alt="Fuel Snax" style="max-width: 200px; margin-top: -10px;">
        
        logo_pattern = r'<img src="img/Fuel_Snax\.png" class="img-responsive" alt="[^"]*">'
        logo_replacement = '<img src="img/Fuel_Snax.png" class="img-responsive" alt="Fuel Snax" style="max-width: 200px; margin-top: -10px;">'
        
        if '<a class="navbar-brand' in content: # Only apply in header context if possible, but global replace is probably safe for this specific logo
             new_content = re.sub(logo_pattern, logo_replacement, new_content)

        # 2. Hide Broken Welcome Images
        # Target:
        # <div class="col-md-5 col-sm-12  mt-50">
        #   <img src="img/img-2.png" alt="welcome" class="img-responsive">
        #   <img src="img/img-1.png" alt="welcome" class="img-responsive">
        # </div>
        
        # We will comment out the imgs.
        # Regex to handle whitespace variations
        
        img_block_pattern = r'(<div class="col-md-5 col-sm-12\s+mt-50">\s*)(<img src="img/img-2\.png"[^>]*>\s*<img src="img/img-1\.png"[^>]*>)'
        
        def comment_imgs(match):
            return f'{match.group(1)}<!-- {match.group(2)} -->'

        new_content = re.sub(img_block_pattern, comment_imgs, new_content, flags=re.DOTALL)
        
        # Also handle cases where they might be individual or slightly different in other files if strictly matching failed
        # Just simple string replace for the individual lines if they exist and aren't commented
        
        if '<img src="img/img-2.png"' in new_content and '<!-- <img src="img/img-2.png"' not in new_content:
             new_content = new_content.replace('<img src="img/img-2.png"', '<!-- <img src="img/img-2.png"')
             new_content = new_content.replace('alt="welcome" class="img-responsive">', 'alt="welcome" class="img-responsive"> -->')

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed layout in: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Base Directory not found: {BASE_DIR}")
        return

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith((".html", ".htm")):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()
