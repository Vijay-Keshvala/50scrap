import os

SKYBLUE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/skyblue.in"

def restore_assets(directory):
    print(f"Restoring assets in: {directory}")
    
    files_processed = 0
    files_updated = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                files_processed += 1
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Revert classioffice.com -> skyblue.in
                    # This fixes the assets (src="//classioffice.com/cdn/...")
                    # It also reverts any text mentions of the domain, which is safer for now.
                    if "classioffice.com" in content:
                        new_content = content.replace("classioffice.com", "skyblue.in")
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Restored assets in: {path}")
                        files_updated += 1
                    else:
                        print(f"No changes needed: {path}")
                        
                except Exception as e:
                    print(f"Error processing {path}: {e}")

    print(f"Restoration Complete. Processed {files_processed} files. Updated {files_updated} files.")

if __name__ == "__main__":
    restore_assets(SKYBLUE_DIR)
