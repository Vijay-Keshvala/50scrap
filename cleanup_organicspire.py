import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'

NEW_ADDRESS = "48,  Block A, 1st Floor, Itinda Road, Near SBI Building, Basirhat – 743411, West Bengal"
NEW_EMAIL = "business@organicspire.com"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # 1. Replace "Hyderabad" with "Basirhat" / "West Bengal" in specific contexts
        # "Organic Vegetables... Hyderabad" -> "... Basirhat"
        content = content.replace("Organic Vegetables Fruits Staples Hyderabad", "Organic Vegetables Fruits Staples Basirhat")
        content = content.replace("we deliver in Hyderabad", "we deliver in Basirhat")
        content = content.replace("organic food in Hyderabad", "organic food in Basirhat")
        content = content.replace("distributed in Hyderabad", "distributed in Basirhat")
        
        # 2. Replace Email if found (we grep'd mailto and likely found nothing or generic)
        # If 'siri@organicsiri.com' was already replaced by rebrand script, we might be good.
        # But grep for new email failed? 
        # "siri@organicsiri.com" -> "business@organicspire.com" (Rebrand script did this).
        # Maybe grep failed because I made a typo in grep or the file wasn't updated?
        # I'll re-apply email replacement just in case.
        content = content.replace("siri@organicsiri.com", NEW_EMAIL)
        content = content.replace("siri@organicspire.com", NEW_EMAIL) # Artifact?
        content = content.replace("franchise@oragnicsiri.com", NEW_EMAIL)
        
        # 3. Address Replacement
        # I'll try to find the street address if it exists. 
        # Searching for typical address markers from previous knowledge or general patterns.
        # "Miyapur" or "Kukatpally" are common Hyderabad areas.
        # But if I can't find it, I'll stick to the "Hyderabad" -> "Basirhat" swaps which cover the visible text.
        
        # 4. Text artifacts
        content = content.replace("OrganicSiri", "Organic Spire")
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned up: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.json')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
