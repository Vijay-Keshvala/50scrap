import os
import re

# Configuration
TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/jiwa.in'
NEW_BRAND_NAME = "Pasta Avenue"
NEW_BRAND_NAME_UPPER = "PASTA AVENUE"
NEW_ADDRESS = "House No. 78, College Rd., Near State Bank of India, Baripada – 757001, Odisha"
NEW_EMAIL = "info@pastaavenue.com"
NEW_URL = "www.pastaavenue.com"
NEW_LOGO_PATH = "assets/PastaAvenue.png"

# Regex patterns
OLD_ADDRESS_PATTERN = r"119,\s*Veena\s*Beena\s*Complex,\s*Gurunanak\s*road\s*Opp\.\s*Bandra\s*Stn\.,\s*Bandra\s*\(W\),\s*Mumbai\s*400\s*050"
OLD_EMAIL_PATTERN = r"[\w\.-]+@jiwa\.in" 
OLD_URL_PATTERN = r"www\.jiwa\.in"
LOGO_IMG_PATTERN = r'<img\s+[^>]*src="assets/logo[^"]*"[^>]*>'

def rebrand_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return

    original_content = content

    # 1. URL Replacement (Do this FIRST)
    content = re.sub(OLD_URL_PATTERN, NEW_URL, content, flags=re.IGNORECASE)

    # 2. Email Replacement
    content = re.sub(OLD_EMAIL_PATTERN, NEW_EMAIL, content, flags=re.IGNORECASE)

    # 3. Address Replacement
    content = re.sub(OLD_ADDRESS_PATTERN, NEW_ADDRESS, content, flags=re.IGNORECASE)

    # 4. Text Branding Replacements
    content = content.replace("jiwas.myshopify.com", "##SHOPIFY_STORE_ID##")
    
    # Promo Codes
    content = content.replace("JIWA10", "PASTAAVENUE10")
    content = content.replace("JIWA20", "PASTAAVENUE20") # Just in case

    # Replace "Jiwa" (Capitalized)
    content = re.sub(r'\bJiwa\b', NEW_BRAND_NAME, content)
    
    # Replace "JIWA" (Upper)
    content = re.sub(r'\bJIWA\b', NEW_BRAND_NAME_UPPER, content)
    
    # Replace specific lowercase "jiwa" 
    content = re.sub(r'To reach jiwa', f'To reach {NEW_BRAND_NAME}', content)
    content = re.sub(r'content="jiwa"', f'content="{NEW_BRAND_NAME}"', content)
    
    # Restore exceptions
    content = content.replace("##SHOPIFY_STORE_ID##", "jiwas.myshopify.com")

    # 5. Logo Replacement
    def replace_logo_tag(match):
        img_tag = match.group(0)
        if "PastaAvenue.png" in img_tag:
            return img_tag
        
        new_tag = re.sub(r'src="[^"]+"', f'src="{NEW_LOGO_PATH}"', img_tag)
        new_tag = re.sub(r'srcset="[^"]+"', '', new_tag)
        new_tag = re.sub(r'sizes="[^"]+"', '', new_tag)
        new_tag = re.sub(r'width="[^"]+"', '', new_tag)
        new_tag = re.sub(r'height="[^"]+"', '', new_tag)
        
        if 'style="' in new_tag:
             new_tag = new_tag.replace('style="', 'style="max-height: 60px; width: auto; ')
        else:
             new_tag = new_tag.replace('<img ', '<img style="max-height: 60px; width: auto;" ')
             
        return new_tag

    content = re.sub(LOGO_IMG_PATTERN, replace_logo_tag, content)

    # 6. Replace og:image logo
    content = re.sub(r'content="[^"]*Jiwa_New_Logo[^"]*"', f'content="{NEW_LOGO_PATH}"', content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                rebrand_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory(TARGET_DIR)
