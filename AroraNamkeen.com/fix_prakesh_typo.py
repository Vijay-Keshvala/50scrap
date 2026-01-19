import os
import re

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def fix_typo(content):
    # Replace "Prakesh" with "Prakash", case sensitive to be safe but usually it's Title Case
    # The typo observed was "Prakesh Namkeen"
    # match "Prakesh" -> "Prakash"
    
    new_content = content.replace('Prakesh', 'Prakash')
    return new_content

def main():
    print(f"Scanning directory for typo fix: {TARGET_DIR}")
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    new_content = fix_typo(original_content)
                    
                    if new_content != original_content:
                        count += 1
                        print(f"Fixing typo in {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    print(f"Complete. Fixed typo in {count} files.")

if __name__ == "__main__":
    main()
