import os
import re

TARGET_DIR = '/Users/vijaykeshvala/Documents/scraped_data/glamrisdermacare.com'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Restore asset URLs (escaped and non-escaped)
    content = content.replace("excelcosmetics.in/wp-content", "glamrisdermacare.com/wp-content")
    content = content.replace("excelcosmetics.in/wp-includes", "glamrisdermacare.com/wp-includes")
    content = content.replace("excelcosmetics.in/uploads", "glamrisdermacare.com/uploads")
    
    # Handle escaped slashes in JS
    content = content.replace("excelcosmetics.in\\/wp-content", "glamrisdermacare.com\\/wp-content")
    content = content.replace("excelcosmetics.in\\/wp-includes", "glamrisdermacare.com\\/wp-includes")
    content = content.replace("excelcosmetics.in\\/uploads", "glamrisdermacare.com\\/uploads")

    # 2. Fix root-relative links that were broken
    content = content.replace('src="/wp-content/', 'src="https://www.glamrisdermacare.com/wp-content/')
    content = content.replace('href="/wp-content/', 'href="https://www.glamrisdermacare.com/wp-content/')
    content = content.replace('src="/wp-includes/', 'src="https://www.glamrisdermacare.com/wp-includes/')
    content = content.replace('href="/wp-includes/', 'href="https://www.glamrisdermacare.com/wp-includes/')
    content = content.replace('url(&quot;/wp-content/', 'url(&quot;https://www.glamrisdermacare.com/wp-content/')
    content = content.replace('url("/wp-content/', 'url("https://www.glamrisdermacare.com/wp-content/')
    content = content.replace('url(\'/wp-content/', 'url(\'https://www.glamrisdermacare.com/wp-content/')

    # 3. Fix the name replacement with tricky HTML tags
    content = content.replace("Glamris <span style=\"font-weight:normal;\">Dermacare</span>", "Excel <span style=\"font-weight:normal;\">Cosmetics</span>")
    content = content.replace("Glamris <span style=\"font-weight:normal;\">Dermacare’</span>", "Excel <span style=\"font-weight:normal;\">Cosmetics’</span>")
    content = content.replace("‘Glamris <span style=\"font-weight:normal;\">Dermacare’</span>", "‘Excel <span style=\"font-weight:normal;\">Cosmetics’</span>")
    content = content.replace("Glamris <span style=\"font-weight:normal;\">dermacare</span>", "Excel <span style=\"font-weight:normal;\">cosmetics</span>")
    content = content.replace("<b>‘Glamris <span style=\"font-weight:normal;\">Dermacare’</span></b>", "<b>‘Excel <span style=\"font-weight:normal;\">Cosmetics’</span></b>")
    
    # 4. Footer credit fix
    content = content.replace('<b style="color: #a62c92;">Glamris</b><b style="color: #a62c92;">Dermacare</b>', '<b style="color: #a62c92;">Excel</b><b style="color: #a62c92;">Cosmetics</b>')
    content = content.replace('<b style="color: #a62c92;">glamris</b><b style="color: #a62c92;">dermacare</b>', '<b style="color: #a62c92;">excel</b><b style="color: #a62c92;">cosmetics</b>')

    # 5. Schema fix
    content = content.replace('"alternateName":"Glamris"', '"alternateName":"Excel"')
    
    # 6. Meta tags and general text cleanup
    content = content.replace("alt=\"Glamris Dermacare\"", "alt=\"Excel Cosmetics\"")
    content = content.replace("title=\"Glamris Dermacare\"", "title=\"Excel Cosmetics\"")
    content = content.replace("Glamris Dermacare Care", "Excel Cosmetics Care")
    content = content.replace("Best Dermatology Company For Pharma Businesss - Glamris Dermacare", "Best Dermatology Company For Pharma Businesss - Excel Cosmetics")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Fixing {file_path}...")
                process_file(file_path)

if __name__ == "__main__":
    process_directory(TARGET_DIR)
    print("Fixing complete.")
