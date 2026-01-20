import os
import re

BASE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com/assets"

def search_css():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".css"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Find .et_pb_section_1 block
                    # Pattern: .et_pb_section_1{[^}]*}
                    matches = re.findall(r'(\.et_pb_section_1\s*\{[^}]*\})', content)
                    if matches:
                        print(f"Found in {file}:")
                        for m in matches:
                            print(m)
                            
                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    search_css()
