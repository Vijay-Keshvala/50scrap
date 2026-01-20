import os
import re
from urllib.parse import urlparse

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/sahnibakery.com'

# Mapping rules based on observed file naming convention
# / -> index.html
# /collections/name -> collections_name.html
# /products/name -> products_name.html
# /pages/name -> pages_name.html
# /account/login -> account_login.html
# /account/register -> account_register.html
# /cart -> cart.html

def get_local_path(url):
    # Remove domain
    if 'sahnibakery.com' in url:
        parsed = urlparse(url)
        path = parsed.path
    elif url.startswith('/'):
        path = url
    else:
        return url # Return as is if it doesn't look like a path we want to fix
        
    if path == '/' or path == '':
        return 'index.html'
    
    # Handle specific known paths
    if path == '/account/login':
        return 'account_login.html'
    if path == '/account/register':
        return 'account_register.html'
    if path == '/cart':
        return 'cart.html'
        
    # Handle patterns
    parts = path.strip('/').split('/')
    if len(parts) >= 2:
        if parts[0] == 'collections':
            return f"collections_{parts[1]}.html"
        if parts[0] == 'products':
            return f"products_{parts[1]}.html"
        if parts[0] == 'pages':
            return f"pages_{parts[1]}.html"
            
    # Fallback: simple replace / with _ + .html? 
    # But checking if file exists is better.
    # For now, let's use the pattern matching which fits the scraper output.
    
    return url

def fix_links(content):
    # Regex to find hrefs
    # Match href="https://sahnibakery.com..." or href="//sahnibakery.com..." or href="/..."
    # We need to be careful not to match local anchors or existing relative links too strictly if they are already correct, but usually they are absolute in scraped code.
    
    # Pattern 1: Domain based
    # href=["'](https?:)?//(www\.)?sahnibakery\.com([^"']*)["']
    
    def replacement(match):
        full_match = match.group(0) # e.g. href="https://sahnibakery.com/collections/cakes"
        quote = full_match[5] # " or '
        url = match.group(2) # /collections/cakes
        
        # If url is empty or just /, it's index
        local_link = get_local_path(url)
        
        # Check if it was converted
        if local_link != url:
            return f'href={quote}{local_link}{quote}'
        return full_match

    # Replace domain links
    content = re.sub(r'href=(["\'])(?:https?:)?(?://)?(?:www\.)?sahnibakery\.com([^"\']*)["\']', replacement, content)
    
    # Replace absolute root links href="/..." (excluding //)
    # We need to distinguish href="/" from href="//cdn..."
    # A safe bet is looking for href="/something" but check that the char after / is not /
    
    def root_replacement(match):
        full_match = match.group(0)
        quote = full_match[5]
        url = match.group(2)
        
        # Skip if it behaves like protocol relative url //...
        if url.startswith('//'):
            return full_match
            
        local_link = get_local_path(url)
        if local_link != url:
             return f'href={quote}{local_link}{quote}'
        return full_match

    # Regex for href="/..."
    # This might match things that are not links to pages (e.g. assets). 
    # But get_local_path filters only specific patterns (collections, products, pages).
    content = re.sub(r'href=(["\'])(/([^"\']*))["\']', root_replacement, content)
    
    return content

def main():
    print(f"Scanning directory: {TARGET_DIR}")
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    new_content = fix_links(original_content)
                    
                    if new_content != original_content:
                        count += 1
                        # print(f"Fixing links in {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    print(f"Complete. Fixed links in {count} files.")

if __name__ == "__main__":
    main()
