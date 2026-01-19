import os
import re

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/prakashnamkeen.com'

def remove_whatsapp_widget(content):
    # Remove the <gty-whatsapp-chat-button> tag
    # Pattern to match: <gty-whatsapp-chat-button ...></gty-whatsapp-chat-button>
    # It might have attributes, so we use .*?
    # It might vary in spacing.
    
    # Regex for the element
    content = re.sub(r'<gty-whatsapp-chat-button.*?>.*?</gty-whatsapp-chat-button>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Also purely self-closing or just the opening tag if that's how it appears sometimes? 
    # The grep showed: <gty-whatsapp-chat-button style="display: block;"></gty-whatsapp-chat-button>
    
    # Remove script tags referencing whatsapp-button.eazeapps.io
    # <script src="https://whatsapp-button.eazeapps.io...
    # or async src=...
    
    # We want to remove the whole script tag.
    # Pattern: <script [^>]*src=["\'].*?whatsapp-button\.eazeapps\.io.*?[^>]*>.*?</script>
    
    content = re.sub(r'<script[^>]*src=[\'"].*?whatsapp-button\.eazeapps\.io.*?[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
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
                    
                    new_content = remove_whatsapp_widget(original_content)
                    
                    if new_content != original_content:
                        count += 1
                        print(f"Removing WhatsApp widget from {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    print(f"Complete. Modified {count} files.")

if __name__ == "__main__":
    main()
