import os

# Configuration
ROOT_DIR = "."
OUTPUT_FILE = "index.html"
EXCLUDE_DIRS = {".git", ".gemini", "__pycache__", ".vscode", ".idea"}

def generate_index():
    # Get all subdirectories
    sites = [
        d for d in os.listdir(ROOT_DIR)
        if os.path.isdir(os.path.join(ROOT_DIR, d)) and d not in EXCLUDE_DIRS and not d.startswith(".")
    ]
    sites.sort()

    # Base HTML template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Websites Index</title>
    
<style>
    :root {{ --primary: #2563eb; --bg: #f8fafc; --card: #ffffff; --text: #1e293b; }}
    body {{ font-family: -apple-system, system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; max-width: 1200px; margin: 0 auto; }}
    h1 {{ text-align: center; color: var(--primary); margin-bottom: 2rem; }}
    .search-box {{ display: block; width: 100%; max-width: 600px; margin: 0 auto 3rem; padding: 1rem; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 1.1rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
    .card {{ background: var(--card); padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); transition: transform 0.2s; text-decoration: none; color: inherit; border: 1px solid #e2e8f0; display: block; }}
    .card:hover {{ transform: translateY(-4px); border-color: var(--primary); }}
    .card h3 {{ margin: 0 0 0.5rem 0; font-size: 1.1rem; color: var(--primary); overflow-wrap: break-word; }}
    .card p {{ margin: 0; font-size: 0.9rem; color: #64748b; }}
    .tag {{ display: inline-block; padding: 0.25rem 0.5rem; background: #e0f2fe; color: #0369a1; border-radius: 999px; font-size: 0.8rem; margin-top: 0.75rem; }}
    .count {{ color: #64748b; font-size: 0.9rem; margin-left: 0.5rem; }}
</style>

</head>
<body>
    <h1>Scraped Websites Index ({len(sites)} Sites)</h1>
    <input type="text" class="search-box" placeholder="Search websites...">
    
    <div class="grid">
"""

    for site in sites:
        html_content += f"""    
        <a href="./{site}/index.html" class="card" target="_blank">
            <h3>{site}</h3>
            <p>Scraped content</p>
            <span class="tag">View Site &rarr;</span>
        </a>
        """

    html_content += """
    </div>
    
<script>
    document.querySelector('.search-box').addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(term) ? 'block' : 'none';
        });
    });
</script>

</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Index generated with {len(sites)} sites.")

if __name__ == "__main__":
    generate_index()
