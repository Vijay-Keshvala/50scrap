
import os
import re
from urllib.parse import urlparse

ROOT_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def scan_files():
    files = [f for f in os.listdir(ROOT_DIR) if f.endswith('.html')]
    
    absolute_urls = set()
    protocol_relative = set()
    local_paths = set()
    
    for filename in files:
        path = os.path.join(ROOT_DIR, filename)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Find hrefs
            hrefs = re.findall(r'href=["\'](.*?)["\']', content)
            for url in hrefs:
                if url.startswith('http'):
                    absolute_urls.add(url)
                elif url.startswith('//'):
                    protocol_relative.add(url)
                elif url.startswith('/'):
                    local_paths.add(url)
                    
            # Find srcs
            srcs = re.findall(r'src=["\'](.*?)["\']', content)
            for url in srcs:
                if url.startswith('http'):
                    absolute_urls.add(url)
                elif url.startswith('//'):
                    protocol_relative.add(url)
                elif url.startswith('/'):
                    local_paths.add(url)

    print("=== Protocol Relative URLs (need https:) ===")
    for url in list(protocol_relative)[:10]:
        print(url)
        
    print("\n=== Local Absolute Paths (need mapping) ===")
    for url in list(local_paths)[:10]:
        print(url)
        
    print("\n=== External Absolute URLs (sample) ===")
    for url in list(absolute_urls)[:10]:
        print(url)

if __name__ == '__main__':
    scan_files()
