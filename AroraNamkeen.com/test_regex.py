import re

test_html = '''
<head>
<link href="style.css" rel="stylesheet">
<script src="theme.js"></script>
<link href="custom.css" rel="stylesheet">
<script src="https://whatsapp-button.eazeapps.io/widget.js"></script>
</head>
'''

regex = r'<script[^>]*src=[\'"].*?whatsapp-button\.eazeapps\.io.*?[^>]*>.*?</script>'

clean_html = re.sub(regex, '', test_html, flags=re.DOTALL | re.IGNORECASE)

print("Original length:", len(test_html))
print("Clean length:", len(clean_html))
print("--- Result ---")
print(clean_html)
print("--- End Result ---")
