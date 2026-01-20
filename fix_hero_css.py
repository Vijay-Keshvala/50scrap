import os

CSS_FILE = "/Users/vijaykeshvala/Documents/scraped_data/balvvardhak.com/assets/6c1bc6452790409d328f7bf87ea88b78_2480.css"

def fix_hero_css():
    try:
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Replace broken image references with a valid fallback image
        # Fallback: dadi_ma_feeding_child_8810.webp
        
        BAD_IMAGES = [
            "balvvardhak-banner-header.webp",
            "balvvardhak-header-mobile.jpg",
            "https://www.balvvardhak.com/wp-content/uploads/2024/12/balvvardhak-banner-header.webp",
            "https://whysocialnetwork.com/balvvardhak.com/wp-content/uploads/2024/10/balvvardhak-header-mobile.jpg"
        ]
        
        FALLBACK_IMAGE = "dadi_ma_feeding_child_8810.webp"
        
        for bad_img in BAD_IMAGES:
            if bad_img in content:
                print(f"Replacing {bad_img} with {FALLBACK_IMAGE}")
                content = content.replace(bad_img, FALLBACK_IMAGE)
        
        if content != original_content:
            with open(CSS_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated hero CSS in {CSS_FILE}")
        else:
            print("No changes made to hero CSS (URLs not found or already fixed)")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_hero_css()
