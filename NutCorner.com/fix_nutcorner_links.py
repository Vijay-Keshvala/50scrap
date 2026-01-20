import os
import re

# Definte the target directory
TARGET_DIR = '.'

# Mapping for specific files that might not follow the standard pattern
# Start with known special cases
custom_mapping = {
    'index.html': 'index_html.html',
    '/': 'index_html.html',
    'https://www.nutcorner.com/': 'index_html.html',
    'https://www.nutcorner.com': 'index_html.html',
}

def get_local_path(url):
    # Remove query params and hash
    clean_url = url.split('?')[0].split('#')[0]
    
    # Check custom mapping first
    if clean_url in custom_mapping:
        return custom_mapping[clean_url]
    
    # Handle absolute URLs to the domain
    if clean_url.startswith('https://www.nutcorner.com'):
        path = clean_url.replace('https://www.nutcorner.com', '')
        if path == '' or path == '/':
            return 'index_html.html'
        # Remove leading slash
        path = path.lstrip('/')
    elif clean_url.startswith('/'):
        path = clean_url.lstrip('/')
    else:
        path = clean_url

    # Check if it ends with .html
    if path.endswith('.html'):
        # Try to find a corresponding _html.html file
        candidate = path.replace('.html', '_html.html')
        if os.path.exists(os.path.join(TARGET_DIR, candidate)):
            return candidate
        
        # Check if the file itself exists locally (unlikely based on listing, but good check)
        if os.path.exists(os.path.join(TARGET_DIR, path)):
            return path
            
    return url

def fix_links(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Regex to find href="..." and src="..."
    # We focus on href for navigation
    def replacement(match):
        full_match = match.group(0)
        quote = full_match[0] # The quote used (href='...' or href="...") -> actually regex includes href=
        # Let's parse properly.
        # Group 1: attribute name (href)
        # Group 2: quote
        # Group 3: url
        # But simple regex substitution is cleaner if we just capture the URL.
        
        # Regex: (href=["'])(.*?)(["'])
        attr = match.group(1) # href=" or href='
        url = match.group(2)
        closing_quote = match.group(3)
        
        # Skip empty links, anchors, or javascript
        if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('tel:') or url.startswith('mailto:'):
            return full_match

        new_url = get_local_path(url)
        
        if new_url != url:
            print(f'Replacing {url} -> {new_url} in {os.path.basename(file_path)}')
            return f'{attr}{new_url}{closing_quote}'
        return full_match

    # Pattern to match href="URL" or href='URL'
    # strict matching to avoid messing up other attributes
    pattern = re.compile(r'(href=["\'])(.*?)(["\'])')
    
    new_content = pattern.sub(replacement, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    print("Starting link fix for NutCorner.com...")
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith('.html')]
    print(f"Found {len(files)} HTML files.")
    
    for filename in files:
        fix_links(os.path.join(TARGET_DIR, filename))
    print("Done.")

if __name__ == "__main__":
    main()
