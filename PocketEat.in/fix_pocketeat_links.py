import os
import re

# Definte the target directory
TARGET_DIR = '.'

# Mapping for specific files that might not follow the standard pattern
custom_mapping = {
    'index.html': 'index.html',
    '/': 'index.html',
    'https://www.pocketeat.in/': 'index.html',
    'https://www.pocketeat.in': 'index.html',
    'https://pocketeat.in/': 'index.html',
    'https://pocketeat.in': 'index.html',
    'https://www.PocketEat.com/': 'index.html', # Covering variations seen in meta tags
    'https://www.PocketEat.com': 'index.html',
}

def get_local_path(url):
    # Remove query params and hash
    clean_url = url.split('?')[0].split('#')[0]
    
    # Check custom mapping first
    if clean_url in custom_mapping:
        return custom_mapping[clean_url]
    
    # Handle absolute URLs to the domain
    # We'll check for common domain variations
    domains = ['https://www.pocketeat.in', 'https://pocketeat.in', 'https://www.PocketEat.com']
    path = None
    for domain in domains:
        if clean_url.startswith(domain):
            path = clean_url.replace(domain, '')
            break
            
    if path is None:
        if clean_url.startswith('/'):
            path = clean_url
        else:
            path = clean_url # Relative path maybe

    # Remove leading slash/dots for local file check construction
    # But keep original logic for substitution
    
    # Clean path for checks
    check_path = path.lstrip('/')
    if check_path == '' or check_path == 'index.html' or check_path == 'index.php': # index.php often mapped to index.html in scrapes
        return 'index.html'

    # If it ends with .html, check if we need to append _html.html
    if check_path.endswith('.html'):
        # If it's index.html, we already handled it or it returns itself
        if check_path == 'index.html':
            return 'index.html'
            
        # Try _html.html
        candidate = check_path.replace('.html', '_html.html')
        if os.path.exists(os.path.join(TARGET_DIR, candidate)):
            return candidate
            
        # Check if the file itself exists locally
        if os.path.exists(os.path.join(TARGET_DIR, check_path)):
            return check_path
            
    # If it ends with no extension (like /about-us), try adding _html.html
    if not os.path.splitext(check_path)[1]:
        candidate = check_path + '_html.html'
        if os.path.exists(os.path.join(TARGET_DIR, candidate)):
            return candidate
            
    return url

def fix_links(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    def replacement(match):
        full_match = match.group(0)
        attr = match.group(1) # href=" or href='
        url = match.group(2)
        closing_quote = match.group(3)
        
        # Skip empty links, anchors, or javascript
        if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('tel:') or url.startswith('mailto:'):
            return full_match

        new_url = get_local_path(url)
        
        if new_url != url:
            # print(f'Replacing {url} -> {new_url} in {os.path.basename(file_path)}')
            return f'{attr}{new_url}{closing_quote}'
        return full_match

    pattern = re.compile(r'(href=["\'])(.*?)(["\'])')
    new_content = pattern.sub(replacement, content)
    
    if new_content != content:
        print(f"Updated {os.path.basename(file_path)}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    print("Starting link fix for PocketEat.in...")
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith('.html')]
    print(f"Found {len(files)} HTML files.")
    
    for filename in files:
        fix_links(os.path.join(TARGET_DIR, filename))
    print("Done.")

if __name__ == "__main__":
    main()
