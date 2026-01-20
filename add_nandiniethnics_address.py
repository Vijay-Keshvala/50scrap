import os

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/peachmode.com'
NEW_NAME = "Nandini Ethnics"
NEW_ADDRESS = "Dhatt Cansa Tivim Sircain, Bardez, North Goa – 403502, Goa"
NEW_EMAIL = "ceo@nandiniethnics.com"

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Add Address near email
    # Look for both variations in case it was already partially replaced
    patterns = [
        f"Just send us an e-mail to {NEW_EMAIL}",
        f"send us an e-mail to {NEW_EMAIL}"
    ]
    
    for pattern in patterns:
        if pattern in content and NEW_ADDRESS not in content:
            content = content.replace(pattern, f"Visit us at {NEW_ADDRESS} or {pattern}")
            break

    # 2. Add address to footer copyright area or similar if needed
    # Peachmode typically has small footer
    if NEW_ADDRESS not in content:
        # Try to find copyright area
        if f"{NEW_NAME} <span class=\"square-separator" in content:
            content = content.replace(f"{NEW_NAME} <span class=\"square-separator", f"{NEW_NAME} | {NEW_ADDRESS} <span class=\"square-separator")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Adding address to {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Address update complete.")
