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
    
    has_hash_column = '| #' in lines[0]
    
    for i, line in enumerate(lines):
        # Header row
        if i == 0:
            if not has_hash_column:
                new_lines.append('| # |' + line[1:])
            else:
                new_lines.append(line)
        # Separator row
        elif i == 1:
            if not has_hash_column:
                new_lines.append('| :--- |' + line[1:])
            else:
                new_lines.append(line)
        # Data rows
        else:
            if not has_hash_column:
                new_lines.append(f'| {i-1} |' + line[1:])
            else:
                # Replace the first column value with the correct number
                parts = line.split('|')
                if len(parts) > 2:
                    parts[1] = f' {i-1} '
                    new_lines.append('|'.join(parts))
                else:
                    new_lines.append(line)
            
    new_table_text = '\n'.join(new_lines) + '\n'
    
    if new_table_text != table_text + '\n' and new_table_text != table_text:
        new_content = content.replace(table_text, new_table_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully re-numbered the table in README.md")
    else:
        print("Table is already correctly numbered.")

if __name__ == "__main__":
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    process_readme(readme_path)
