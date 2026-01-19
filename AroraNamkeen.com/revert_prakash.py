import os
import re

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def revert_content(content):
    # Reverse the order of operations effectively, or just target the specific artifacts we created.
    
    # 1. URLs: "Aroranamkeen.com" -> "prakashnamkeen.com"
    content = content.replace('Aroranamkeen.com', 'prakashnamkeen.com')
    
    # 2. Handle "Arora-namkeen" -> "prakash-namkeen"
    content = content.replace('Arora-namkeen', 'prakash-namkeen')
    
    # 3. Text display: "Arora Namkeen" -> "Prakash Namkeen"
    # Note: Original was Case Insensitive input -> Title Case output.
    # We will just put back "Prakash Namkeen" where we see "Arora Namkeen".
    content = content.replace('Arora Namkeen', 'Prakash Namkeen')
    
    # 4. "By Arora" -> "By Prakash"
    content = re.sub(r'By\s+Arora', 'By Prakash', content, flags=re.IGNORECASE)
    
    # 5. Generic "Arora" -> "Prakash"
    # Using the same strict regex boundaries to only replace what we likely changed.
    # Original Regex: (?<![a-zA-Z0-9/_.-])Prakash(?![a-zA-Z0-9/_.-])
    # Revert Regex:   (?<![a-zA-Z0-9/_.-])Arora(?![a-zA-Z0-9/_.-])
    
    content = re.sub(r'(?<![a-zA-Z0-9/_.-])Arora(?![a-zA-Z0-9/_.-])', 'Prakash', content)
    
    return content

def main():
    print(f"Scanning directory for REVERT: {TARGET_DIR}")
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    new_content = revert_content(original_content)
                    
                    if new_content != original_content:
                        print(f"Reverting {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error reverting {file}: {e}")

if __name__ == "__main__":
    main()
