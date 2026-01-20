import os
import re

SOURCE_DIR = "/Users/vijaykeshvala/Documents/scraped_data/amrnutsandhampers.com"

TEXT_REPLACEMENTS = {
    "Amr Nuts & Hampers": "Nut Corner",
    "Amr Nuts &amp; Hampers": "Nut Corner",
    "Amr Nuts And Hampers": "Nut Corner",
    "AMR signature product": "Nut Corner signature product",
    "AMR NUTS & HAMPERS": "NUT CORNER",
    "AMR NUTS &amp; HAMPERS": "NUT CORNER",
    "AMR Nuts & Hampers": "Nut Corner",
    "AMR Nuts &amp; Hampers": "Nut Corner",
    "AMR Nuts And Hampers": "Nut Corner",
    "Dry Fruits Shop in Noida": "Dry Fruits Shop in Mumbai",
    "Dry Fruits Shop & Store in Noida": "Dry Fruits Shop & Store in Mumbai",
    "Best dry fruits shop/store in Noida": "Best dry fruits shop/store in Mumbai",
    "VISIT US IN NOIDA SEC-104": "VISIT US AT OUR MUMBAI STORE",
    "at NOIDA (U.P, INDIA)": "at MUMBAI (MAHARASHTRA, INDIA)",
    "in Noida (UP, India)": "in Mumbai (Maharashtra, India)",
    "sector 104, Noida": "Goregaon (E), Mumbai",
    "sector 104 noida": "Goregaon (E), Mumbai",
    "located in sector 104": "located in Goregaon (E), Mumbai",
    "Opposite Great Value Sharnam Society": "Plot No.-10, Vijay Nagar",
    "Gate No -2, Sector 104,": "Western Express Highway, Near Virvani Estate,",
    "Noida,": "Goregaon (E), Mumbai,",
    "Uttar Pradesh 201301": "Maharashtra – 400063",
    "Dry Fruits Shop in Noida": "Dry Fruits Shop in Mumbai",
    "www.amrnutsandhampers.com": "www.nutcorner.com",
    "amrnuts@gmail.com": "sales@nutcorner.com",
    "amrnuts": "nutcorner", # be careful with this one, maybe too broad? "amrnuts" appears in email meta tag
}

# Specific address replacement
OLD_ADDRESS_PART = "Amr Nuts &amp; Hampers,\s+opposite Great Value Sharnam society,\s+Gate no -2, Sector 104, Noida,\s+Uttar Pradesh 201301"
NEW_ADDRESS = "Nut Corner, Plot No.-10, Vijay Nagar, Western Express Highway, Near Virvani Estate, Goregaon (E), Mumbai – 400063, Maharashtra, India"

LOGO_REPLACEMENT = {
    "logo_2280.png": "Nut Corner.png",
    "logo_footer_9280.png": "Nut Corner.png" 
}

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    original_content = content
    
    # Text replacements
    for old, new in TEXT_REPLACEMENTS.items():
        # Case insensitive replacement for some might be risky, stick to exact strings first
        content = content.replace(old, new)
        
    # Address replacement (handling newlines/whitespace if needed via regex)
    # The address in HTML viewed earlier had newlines
    # <a href=""><i class="fa fa-home"></i> Amr Nuts &amp; Hampers,
    #                                     opposite Great Value Sharnam society,
    #                                     Gate no -2, Sector 104, Noida,
    #                                     Uttar Pradesh 201301</a>
    
    # Regex for address
    content = re.sub(r"Amr Nuts &amp; Hampers,\s+opposite Great Value Sharnam society,\s+Gate no -2, Sector 104, Noida,\s+Uttar Pradesh 201301", NEW_ADDRESS, content, flags=re.DOTALL | re.MULTILINE)
    
    # Logo replacement
    for old, new in LOGO_REPLACEMENT.items():
        content = content.replace(old, new)
        
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    count = 0
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".html"):
                process_file(os.path.join(root, file))
                count += 1
    print(f"Processed {count} files.")

if __name__ == "__main__":
    main()
