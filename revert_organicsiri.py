import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/organicsiri.com'

# Revert details based on previous implementation
# New -> Old

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Revert Logo Filenames (using lookahead/context if possible for accuracy)
        # We need to do this BEFORE text replacement because "NutriCurator" text replacement might mess up filenames if not careful.
        # But actually, the filenames ARE "NutriCurator.png".
        
        # Heuristic restoration of logo sizes based on srcset widths (observed in original file)
        # NutriCurator.png 300w -> Organic_Logos-300x94.png
        content = content.replace("NutriCurator.png 300w", "Organic_Logos-300x94.png 300w")
        content = content.replace("NutriCurator.png 64w", "Organic_Logos-64x20.png 64w")
        content = content.replace("NutriCurator.png 450w", "Organic_Logos-450x141.png 450w")
        content = content.replace("NutriCurator.png 479w", "Organic_Logos.png 479w")
        
        # Default fallback for src="..." which usually points to the medium size (300x94)
        content = content.replace("NutriCurator.png", "Organic_Logos-300x94.png")

        # 2. Revert Styling
        # style="max-height: 85px; width: auto;" -> style="max-width: 100%; height: auto;"
        content = content.replace('style="max-height: 85px; width: auto;"', 'style="max-width: 100%; height: auto;"')
        
        # 3. Revert Texts
        # "Nutri Curator" -> "OrganicSiri" (General case)
        # Note: "OrganicSiri Farms" was mapped to "Nutri Curator", so "Nutri Curator" -> "OrganicSiri" is a decent approximation.
        # We can try to be smart about "Farms".
        
        content = content.replace("Nutri Curator", "OrganicSiri") 
        content = content.replace("NutriCurator", "OrganicSiri") # For social handles like facebook.com/NutriCurator
        
        # 4. Revert URLs and Emails
        content = content.replace("nutricurator.com", "organicsiri.com")
        content = content.replace("franchise@nutricurator.com", "siri@organicsiri.com")
        content = content.replace("www.nutricurator.com", "www.organicsiri.com")
        
        # 5. Fix "OrganicSiri" spacing issues if any (e.g. "OrganicSiri" vs "Organic Siri")
        # The original title was "OrganicSiri Farms". With the above replace it becomes "OrganicSiri".
        # Close enough, but let's see if we can fix "OrganicSiri Farms" specifically.
        # If we see "OrganicSiri, all rights reserved" -> It was "OrganicSiri Farms, all rights reserved"
        content = content.replace("OrganicSiri, all rights reserved", "OrganicSiri Farms, all rights reserved")
        
        # Also fix the weird "Organic Siri" spacing if it exists. 
        # Actually "OrganicSiri" (CamelCase) is the main brand.
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Reverted: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(('.html', '.js', '.css')):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
