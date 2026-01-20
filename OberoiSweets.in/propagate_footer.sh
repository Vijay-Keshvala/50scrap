#!/bin/bash
for file in *.html; do
  if [ "$file" == "index.html" ]; then continue; fi
  
  # Find start line of footer
  start_line=$(grep -n 'class="ekit-template-content-markup ekit-template-content-footer"' "$file" | head -n 1 | cut -d: -f1)
  # Find end line (start of #wrap close comment)
  end_line=$(grep -n '<!-- #wrap -->' "$file" | head -n 1 | cut -d: -f1)
  
  if [ ! -z "$start_line" ] && [ ! -z "$end_line" ]; then
    echo "Updating $file (Footer starts line $start_line, ends before $end_line)"
    
    # Head up to start_line - 1
    head -n $((start_line - 1)) "$file" > "${file}.tmp"
    
    # Insert new footer
    cat footer.html >> "${file}.tmp"
    
    # Tail from end_line
    tail -n +$end_line "$file" >> "${file}.tmp"
    
    mv "${file}.tmp" "$file"
  else
    echo "Skipping $file (Pattern not found: Start=$start_line, End=$end_line)"
  fi
done
