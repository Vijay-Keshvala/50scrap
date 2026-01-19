import os

# Files to restore (in order)
COMMON_CSS = [
    'assets/base_6224.css',
    'assets/theme_6455.css',
    'assets/style_min_6994.css' # Assuming this is common
]

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def restore_css(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine page specific CSS
    # e.g. collections_unique-pickles.html -> collections_unique-pickles_styles.css
    basename = filename.replace('.html', '')
    page_css = f"{basename}_styles.css"
    
    # Check if page_css file EXISTS
    if not os.path.exists(os.path.join(TARGET_DIR, page_css)):
        page_css = None
        
    links_to_add = []
    
    # Add common CSS if missing
    for css in COMMON_CSS:
        if css not in content:
            links_to_add.append(f'<link href="{css}" rel="stylesheet" type="text/css" media="all">')
            
    # Add page CSS if missing and exists
    if page_css and page_css not in content:
        links_to_add.append(f'<link href="{page_css}" rel="stylesheet" type="text/css" media="all">')
        
    if not links_to_add:
        return False
        
    # Insertion point: Before </head>
    if '</head>' in content:
        insertion = '\n  ' + '\n  '.join(links_to_add) + '\n'
        new_content = content.replace('</head>', insertion + '</head>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    else:
        print(f"Warning: No </head> in {filename}")
        return False

def main():
    print(f"Scanning directory: {TARGET_DIR}")
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if restore_css(filepath, file):
                    print(f"Restored CSS in {file}")
                    count += 1
    print(f"Complete. Restored CSS in {count} files.")

if __name__ == "__main__":
    main()
