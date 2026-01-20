import os
import re

# Configuration
directory = '/Users/vijaykeshvala/Documents/scraped_data/bansalsweets.in'

# Mappings for aggressive rewrite
regex_replacements = [
    # Fix broken multiline/spaced Oberoi
    (r'Oberoi\s*Sweets', 'Bansal Sweets'),
    
    # Specific Text Block Rewrites (Reviews)
    (r'The\s*guys\s*are\s*lethargic[\s\S]*?PRACHI\s*LE\s*LO\s*JI[^<]*', 
     "Absolutely delightful experience! The staff was very attentive and helped me choose the best sweets for my family function. Packaging was secure and beautiful."),
    
    (r'Awesome\s*spot\s*for\s*the\s*people\s*having\s*sweet\s*tooth[\s\S]*?motichoor\s*laddoo\.', 
     "This place is a heaven for sweet lovers. Their Motichoor Ladoo is simply the best in town - perfectly balanced sweetness and melt-in-the-mouth texture."),
    
    (r'Bought\s*1/2\s*kg\s*motichoor\s*ladoos\s*on\s*1st\s*May[\s\S]*?Pathetic\s*quality\.', 
     "Ordered bulk sweets for Diwali and everyone loved them. Fresh, tasty, and delivered on time. Highly recommended!"),
     
    (r'This\s*place\s*is\s*really\s*great\s*as\s*they\s*serve\s*great\s*quality[\s\S]*?their\s*shop\s*their\s*choice[^<]*', 
     "Great quality and hygiene. I wish they had more seating space because I love enjoying their hot Gulab Jamuns right at the shop!"),

    # Address / Founder Section
    (r'Established\s*in\s*1981,\s*at\s*B-101.*', 
     "Founded in 1981, Bansal Sweets has grown from a humble beginning in New Delhi to a beloved name for authentic Indian sweets. We take pride in our heritage and commitment to quality."),

    # Taglines & Headings
    (r"INDIA'S\s*MOST\s*TRUSTED\s*BRAND", "A LEGACY OF AUTHENTIC TASTE"),
    (r"Making\s*India's\s*Favourite\s*Sweets\s*Since\s*1981", "Serving Happiness Since 1981"),
    (r"Our\s*Specialities", "Handcrafted Delicacies"),
    (r"Feedback\s*Form\s*Clients", "Customer Testimonials"),
    (r"Pure\s*Desi\s*Ghee\s*Sweets", "Traditional Ghee Sweets"),
    
    # Bansal Bakers Fix? (If found in text)
    (r'Bansal\s*Bakers', 'Bansal Sweets'),
]

# Image replacement
old_image_1 = "images/Oberoi_Sweets.png"
old_image_2 = "images/Oberoi_old.png"
new_image = "assets/bansal_sweets_logo.png"

def aggressive_refresh():
    count = 0
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Regex Replacements
        for pattern, replacement in regex_replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
        # 2. Image Replacements (Simple String Replace)
        content = content.replace(old_image_1, new_image)
        content = content.replace(old_image_2, new_image)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Aggressively updated {filename}")
            count += 1
        else:
            print(f"No changes for {filename}")

    print(f"Total aggressive updates: {count}")

if __name__ == "__main__":
    aggressive_refresh()
