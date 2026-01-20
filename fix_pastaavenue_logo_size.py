import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/jiwa.in'

def update_logo_size(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content

    # Find and replace the logo styling - increase from 60px to 85px
    # Pattern: style="max-height: 60px; width: auto;"
    content = re.sub(
        r'style="max-height:\s*60px;\s*width:\s*auto;?"',
        'style="max-height: 85px; width: auto;"',
        content
    )
    
    # Also handle cases where there might be additional styles
    content = re.sub(
        r'(style="[^"]*?)max-height:\s*60px;',
        r'\1max-height: 85px;',
        content
    )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated logo size in: {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                update_logo_size(os.path.join(root, file))

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("\nLogo size increased from 60px to 85px!")
