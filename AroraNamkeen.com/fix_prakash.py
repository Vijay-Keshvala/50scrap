
import os
import re
from urllib.parse import urlparse

ROOT_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'
DOMAIN = 'prakashnamkeen.com'
ORIGINAL_URL = 'https://prakashnamkeen.com'

# Mapping of URL paths to local filenames
url_map = {}

def build_url_map():
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith('.html')]
    for filename in files:
        name_part = filename.replace('.html', '')
        if name_part == 'index':
            slug = '/'
        else:
            slug = '/' + name_part.replace('_', '/')
        url_map[slug] = filename
        url_map[slug.lstrip('/')] = filename
    url_map['/'] = 'index.html'

def fix_content(content, filename):
    
    # 1. Fix Protocol Relative URLs (//cdn... -> https://cdn...)
    # This might affect src and href, which is good.
    content = re.sub(r'(["\'])//', r'\1https://', content)
    
    # 2. Fix root-relative CDN paths (/cdn/... -> https://prakashnamkeen.com/cdn/...)
    content = re.sub(r'(["\'])/cdn/', f'\\1{ORIGINAL_URL}/cdn/', content)
    
    # 3. Fix Navigation Links (HTML files mainly)
    def replace_link(match):
        quote = match.group(1)
        url = match.group(2)
        
        # Preserve empty or special links
        if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:') or url.startswith('tel:'):
            return match.group(0)
            
        parsed = urlparse(url)
        
        # Check if external
        is_local_domain = False
        if not parsed.netloc:
            is_local_domain = True
        elif DOMAIN in parsed.netloc or 'localhost' in parsed.netloc:
             is_local_domain = True
             
        if not is_local_domain:
            return match.group(0)
            
        path = parsed.path
        if not path:
            path = '/'
            
        # Normalize path
        normalized_path = path
        if normalized_path != '/' and normalized_path.endswith('/'):
            normalized_path = normalized_path[:-1]
            
        # 1. Try URL Map (for HTML pages)
        if normalized_path in url_map:
            return f'href={quote}{url_map[normalized_path]}{quote}'
        
        # 2. Check for underscore-mapped file
        potential_file = normalized_path.strip('/').replace('/', '_') + '.html'
        if potential_file in url_map.values():
             return f'href={quote}{potential_file}{quote}'
             
        # 3. Check if file exists locally (e.g. assets/style.css, images/logo.png)
        # We check relative to ROOT_DIR. 
        # CAUTION: path might start with / or not.
        local_check_path = path.lstrip('/')
        if os.path.exists(os.path.join(ROOT_DIR, local_check_path)):
            # It exists! Keep it relative (or as is).
            # If original was absolute path /assets/..., we might want to keep it /assets/... if site root is correct?
            # But local file view uses file:// so /assets/... looks at HDD root.
            # Best to make it relative if possible, or just keep as is if it's distinct enough.
            # Actually, standard practice for these local sites: ensure it's relative.
            # For now, returning match.group(0) keeps it as is (e.g. "assets/foo.css" or "/assets/foo.css").
            # If it was "/assets/..." it might fail on file://.
            # Let's try to make it relative? 
            # simplest: just return what we found, assuming it was working relative path or we leave it to user to handle base tag.
            # But wait, earlier I broke it because I fell through to absolute URL replacement.
            return match.group(0)
            
        # 4. Fallback: If we can't find it locally, point to LIVE site.
        if is_local_domain and not parsed.netloc:
            # It was relative, e.g. /pages/unknown or /assets/missing.css
            return f'href={quote}{ORIGINAL_URL}{path}{quote}'
            
        return match.group(0)

    # Apply replacement to hrefs
    content = re.sub(r'href=(["\'])(.*?)\1', replace_link, content)
    
    return content

def run():
    build_url_map()
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith('.html')]
    for filename in files:
        path = os.path.join(ROOT_DIR, filename)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        new_content = fix_content(content, filename)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {filename}")

if __name__ == '__main__':
    run()
