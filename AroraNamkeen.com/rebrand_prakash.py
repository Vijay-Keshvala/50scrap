import os
import re

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def rebrand_content(content):
    # Text replacements (Case sensitive mostly, but handling variations)
    
    # 1. Text display: "Prakash Namkeen" -> "Arora Namkeen"
    # match case insensitive for the text, but replace with Title Case
    content = re.sub(r'Prakash\s+Namkeen', 'Arora Namkeen', content, flags=re.IGNORECASE)
    
    # 2. URLs: "prakashnamkeen.com" -> "Aroranamkeen.com"
    content = content.replace('prakashnamkeen.com', 'Aroranamkeen.com')
    
    # 3. Handle "prakash-namkeen" (often in shopify URLs) -> "Arora-namkeen"
    content = content.replace('prakash-namkeen', 'Arora-namkeen')
    
    # 4. Generic "Prakash" -> "Arora" in text content, BUT careful about filenames.
    # Strategy: Replace "Prakash" only if not followed by common file extensions or inside an image src path roughly.
    # It's safer to rely on the specific replacements above, but user asked for "change the name from prakash to arora everywhere".
    # Let's try a regex that avoids specific asset contexts.
    
    # Regex lookahead to ensure we don't match if it's inside a filename extension like .jpg, .png, .css, .js
    # And lookbehind to ensure it's not preceded by a slash or underscore which indicates a file path usually.
    # However, HTML attributes make this hard.
    
    # Safer approach: Iterate specific known patterns first.
    # "By Prakash" -> "By Arora"
    content = re.sub(r'By\s+Prakash', 'By Arora', content, flags=re.IGNORECASE)
    # "Prakash" at start of title or sentence?
    
    # Let's try a global replacement of "Prakash" to "Arora" but then REVERT it for likely file paths.
    # This is a bit "aggressive revert" strategy.
    
    # Actually, simpler: Use a regex that matches "Prakash" but VALIDATES it's not part of a src="..." or href="..." ending in an image ext.
    # But files can be anywhere.
    
    # Alternative strategy based on User Request: "if its the name of image or something then dont change it"
    # We can match "Prakash" and check if it's surrounded by typical path characters.
    
    def replacer(match):
        text = match.group(0)
        # Context checks could be done here if we had more context, but with simple regex it's hard.
        return "Arora"

    # We will do a targeted text replacement for "Prakash" when it looks like a name.
    # 1. Inside title tags, alt tags (if not filename), text nodes.
    # This is complex to parse perfectly with regex.
    
    # Let's stick to the specific domain and full name replacements first, as those cover 80% with 0 risk.
    # Then generic "Prakash" not followed by characters like . _ - might work?
    # No, "Prakash" might be followed by space.
    
    # Let's replace "Prakash" with "Arora" ONLY if it is Capitalized and NOT followed by .png, .jpg, .jpeg, .gif, .webp, .css, .js
    # AND not preceded by / (which suggests a path) or - (which suggests a slug, though slugs might need updating too? User updated slugs: prakash-namkeen -> Arora-namkeen)
    
    # Pattern: Not preceded by [a-zA-Z0-9/_] (path chars) and not followed by [._] (extension/separator)
    # This handles "Prakash" as a standalone word.
    
    # Regex: (?<![a-zA-Z0-9/_.-])Prakash(?![a-zA-Z0-9/_.-]) -> Arora
    # This matches "Prakash" surrounded by spaces, quotes, brackets, etc.
    # It excludes "images/Prakash.png" (preceded by /)
    # It excludes "Prakash_logo.png" (followed by _)
    
    content = re.sub(r'(?<![a-zA-Z0-9/_.-])Prakash(?![a-zA-Z0-9/_.-])', 'Arora', content)
    
    # Also handle lowercase "prakash" if it stands alone? "prakash namkeen"
    # content = re.sub(r'(?<![a-zA-Z0-9/_.-])prakash(?![a-zA-Z0-9/_.-])', 'arora', content)
    # User user manual edits showed "Arora Namkeen" (Project Case).
    
    return content

def main():
    print(f"Scanning directory: {TARGET_DIR}")
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                # optional: skip index.html if we want to trust user's edits, but safer to re-process generally unless it undoes something specific.
                # User's manual edit was good, my script should just reinforce it.
                
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    new_content = rebrand_content(original_content)
                    
                    if new_content != original_content:
                        print(f"Updating {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    main()
