import os
import re

# Configuration
directory = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'
logo_replacement_header = '''<picture class="hdt-logo-default">
    <img src="assets/Arora_Namkeen.png" alt="Arora Namkeen" class="hdt-logo-img">
    </picture>
    
    <picture class="hdt-logo-sticky">
      <img src="assets/Arora_Namkeen.png" alt="Arora Namkeen" class="hdt-logo-img">
    </picture>'''

logo_replacement_footer = '''<img src="assets/Arora_Namkeen.png" alt="Arora Namkeen" class="hdt-image-sm" loading="lazy" style="width: auto; max-height: 80px;">'''

css_injection = '''<style>
    /* Fix footer visibility and text color */
    .hdt-footer, .hdt-footer .hdt-footer-menu_item, .hdt-footer p, .hdt-footer h6, .hdt-footer span, .hdt-footer li, .hdt-footer a {
       color: #000 !important;
       opacity: 1 !important;
       visibility: visible !important;
    }
    .hdt-footer .hdt-s-text2 {
       color: #333 !important;
    }
    /* Ensure footer itself is visible */
    .hdt-footer {
        opacity: 1 !important;
        visibility: visible !important;
    }
  </style>
</head>'''

def propagate_fixes():
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".html") and filename != "index.html":
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. Fix Logo in Header
            # Regex for Header Logo (Default)
            pattern_header_default = r'<picture class="hdt-logo-default">.*?</picture>'
            content = re.sub(pattern_header_default, '<picture class="hdt-logo-default"><img src="assets/Arora_Namkeen.png" alt="Arora Namkeen" class="hdt-logo-img"></picture>', content, flags=re.DOTALL)
            
            # Regex for Header Logo (Sticky)
            pattern_header_sticky = r'<picture class="hdt-logo-sticky">.*?</picture>'
            content = re.sub(pattern_header_sticky, '<picture class="hdt-logo-sticky"><img src="assets/Arora_Namkeen.png" alt="Arora Namkeen" class="hdt-logo-img"></picture>', content, flags=re.DOTALL)

            # 2. Fix Logo in Footer
            # Searching for the specific old logo filename
            pattern_footer_logo = r'<img src="[^"]*PRAKASH_NAMKEEN_LOGO1\.png[^"]*"[^>]*>'
            content = re.sub(pattern_footer_logo, logo_replacement_footer, content)

            # 3. Fix Footer Visibility
            # Remove 'hdt-reveal--offscreen' class
            content = content.replace('hdt-reveal--offscreen', '')
            # Remove 'hdt-reveal="fade-in"' attribute
            content = content.replace('hdt-reveal="fade-in"', '')

            # 4. Inject CSS
            if '/* Fix footer visibility and text color */' not in content:
                content = content.replace('</head>', css_injection)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {filename}")
                count += 1
            else:
                print(f"No changes needed for {filename}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    propagate_fixes()
