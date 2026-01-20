import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/gustorafoods.com'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # We need to revert "Sauce Lane" back to "Gustora" 
        # ONLY inside image paths (src, href, url, srcset)
        # BUT NOT if it is "SauceLane.png" (our new logo)
        
        def revert_path(match):
            full_match = match.group(0)
            if "SauceLane.png" in full_match:
                return full_match
            
            # Revert "Sauce Lane" -> "Gustora"
            # Revert "saucelane" -> "gustora" / "gustorafoods"
            # Since we did "Gustora" -> "Sauce Lane", we revert "Sauce Lane" -> "Gustora"
            reverted = full_match.replace("Sauce Lane", "Gustora").replace("saucelane", "gustorafoods").replace("SauceLane", "Gustora")
            return reverted

        # Patterns to check
        content = re.sub(r'src="[^"]*saucelane[^"]*"', revert_path, content, flags=re.IGNORECASE)
        content = re.sub(r'src="[^"]*Sauce Lane[^"]*"', revert_path, content, flags=re.IGNORECASE)
        
        def revert_asset_link(match):
            full_match = match.group(0)
            if any(ext in full_match for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.css', '.js', '.woff', '.woff2']):
                # It's an asset, revert formatting
                if "SauceLane.png" in full_match: return full_match
                return full_match.replace("Sauce Lane", "Gustora").replace("saucelane", "gustorafoods").replace("SauceLane", "Gustora")
            return full_match 
        
        content = re.sub(r'href="[^"]+"', revert_asset_link, content)
        content = re.sub(r'srcset="[^"]+"', revert_asset_link, content)
        content = re.sub(r'url\([^)]+\)', revert_asset_link, content)

        # Cleanup artifacts
        # social links: youtube.com/@Sauce Lane -> youtube.com/@gustora... ? 
        # User wants "design flows" kept.
        # But youtube link should ideally work? 
        # I'll leave external links if they look like they might point to the new brand (if it existed), 
        # but here they point to the old one. Rebranding changed them to "Sauce Lane".
        # youtube.com/@gustora6918 -> youtube.com/@Sauce Lane6918 ??
        # "Gustora" replaced by "Sauce Lane".
        # We should probably fix social handles back to original if valid, or just clean up spaces.
        content = content.replace("youtube.com/@Sauce Lane", "youtube.com/SauceLane")
        
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
