import re
import os

def process_readme(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the table block
    table_pattern = re.compile(r'(\|.*?\|\n\|.*?\|\n(?:\|.*?\|\n)*)')
    match = table_pattern.search(content)
    if not match:
        print("Could not find table in README.md")
        return

    table_text = match.group(1)
    lines = table_text.strip().split('\n')
    
    new_lines = []
    
    for i, line in enumerate(lines):
        # Header row
        if i == 0:
            # Check if it already has the # column
            if '| #' in line:
                print("Table already has a # column.")
                return
            new_lines.append('| # |' + line[1:])
        # Separator row
        elif i == 1:
            new_lines.append('| :--- |' + line[1:])
        # Data rows
        else:
            new_lines.append(f'| {i-1} |' + line[1:])
            
    new_table_text = '\n'.join(new_lines) + '\n'
    
    new_content = content.replace(table_text, new_table_text)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Successfully numbered the table in README.md")

if __name__ == "__main__":
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    process_readme(readme_path)
