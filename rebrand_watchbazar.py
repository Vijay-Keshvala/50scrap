import os
import re

def rebrand_watchbazar():
    target_dir = "/Users/vijaykeshvala/Documents/scraped_data/skyline-1.ueniweb.com"
    old_name = "Skyline"
    new_name = "Watch Bazar"
    old_url = "skyline-1.ueniweb.com"
    new_url = "watchbazar.in"
    new_email = "sales@watchbazar.in"
    new_address = "418, Times Trade Centre, Opp.Bplaris, Brts Cenal Road, Surat, Gujarat, 395006, INDIA"
    new_phone = "+918200981921"
    new_logo_path = "assets/watchbazar_logo.png"

    html_files = [f for f in os.listdir(target_dir) if f.endswith(".html")]

    for filename in html_files:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Name
        content = content.replace(old_name, new_name)
        
        # Update URL
        content = content.replace(old_url, new_url)
        content = content.replace("www." + old_url, "www." + new_url)

        # Update Email (common patterns)
        content = re.sub(r'[a-zA-Z0-9._%+-]+@' + re.escape(old_url), new_email, content)
        
        # Update Address (This is specific based on previous grep)
        # Old address: "418, Times Trade Centre, Opp.Bplaris, Brts Cenal Road, Surat, Gujarat, 395006, INDIA"
        # It seems the address is already what the user wants or very similar. 
        # I will ensure it matches the target address exactly if it appears.
        
        # Update Logo
        # Search for typical logo patterns in UENI sites
        # Often it's a <img> with a specific class or containing "logo" in src
        content = re.sub(r'src="[^"]*logo[^"]*"', f'src="{new_logo_path}"', content)
        # Also try to catch larger patterns
        content = re.sub(r'<img[^>]+src="[^"]+"[^>]*class="[^"]*logo[^"]*"[^>]*>', f'<img src="{new_logo_path}" class="logo" style="max-width: 200px;">', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Rebranded {len(html_files)} files to {new_name}.")

if __name__ == "__main__":
    rebrand_watchbazar()
