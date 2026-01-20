import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # We need to revert "Organic Spire" back to "OrganicSiri" 
        # ONLY inside image paths (src, href, url, srcset)
        # BUT NOT if it is "OrganicSpire.png" (our new logo)
        
        def revert_path(match):
            full_match = match.group(0)
            if "OrganicSpire.png" in full_match:
                return full_match
            
            # Revert "Organic Spire" -> "OrganicSiri"
            # Revert "organicspire" -> "organicsiri"
            reverted = full_match.replace("Organic Spire", "OrganicSiri").replace("organicspire", "organicsiri")
            return reverted

        # Patterns to check
        content = re.sub(r'src="[^"]*organicspire[^"]*"', revert_path, content, flags=re.IGNORECASE)
        content = re.sub(r'src="[^"]*Organic Spire[^"]*"', revert_path, content, flags=re.IGNORECASE)
        
        def revert_asset_link(match):
            full_match = match.group(0)
            if any(ext in full_match for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.css', '.js', '.woff', '.woff2']):
                # It's an asset, revert formatting
                if "OrganicSpire.png" in full_match: return full_match
                return full_match.replace("Organic Spire", "OrganicSiri").replace("organicspire", "organicsiri")
            return full_match 
        
        content = re.sub(r'href="[^"]+"', revert_asset_link, content)
        content = re.sub(r'srcset="[^"]+"', revert_asset_link, content)
        content = re.sub(r'url\([^)]+\)', revert_asset_link, content)
        
        # Cleanup "Organic Spire" specific artifacts
        # social links: twitter.com/Organic Spire -> twitter.com/OrganicSpire
        content = content.replace("twitter.com/Organic Spire", "twitter.com/OrganicSpire")
        content = content.replace("facebook.com/Organic Spire", "facebook.com/OrganicSpire")
        content = content.replace("instagram.com/Organic Spire", "instagram.com/OrganicSpire")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed images/links in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.css', '.js')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
