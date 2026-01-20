import os

# Configuration
directory = '/Users/vijaykeshvala/Documents/scraped_data/bansalsweets.in'

def revert_logo():
    count = 0
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Revert the specific image replacement
        # Replaces the new logo path back to the old one
        content = content.replace('src="assets/bansal_sweets_logo.png"', 'src="images/Oberoi_Sweets.png"')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Reverted logo in {filename}")
            count += 1
        else:
            print(f"No logo change needed for {filename}")

    print(f"Total files reverted: {count}")

if __name__ == "__main__":
    revert_logo()
