import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # Current style: style="max-height: 85px; width: auto;"
        # New style: style="max-height: 130px; width: auto;" (Increasing significantly as requested)
        
        content = content.replace('style="max-height: 85px; width: auto;"', 'style="max-height: 130px; width: auto;"')
        
        # Also catch case if spacing is different regex-wise, though exact replace is safer if known.
        # Just in case:
        # re.sub(r'max-height:\s*85px', 'max-height: 130px', content)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Resized logo in: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
