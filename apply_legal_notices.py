import os

HEADERS = {
    'python': "# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.\n# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.\n# This software is proprietary and subject to the terms of a specific License Agreement.\n\n",
    'shell': "# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.\n# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.\n# This software is proprietary and subject to the terms of a specific License Agreement.\n\n",
    'ps1': "# (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.\n# PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.\n# This software is proprietary and subject to the terms of a specific License Agreement.\n\n",
    'js': "// (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.\n// PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.\n// This software is proprietary and subject to the terms of a specific License Agreement.\n\n",
    'css': "/* (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.\n   PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.\n   This software is proprietary and subject to the terms of a specific License Agreement. */\n\n",
    'html': "<!-- (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED. -->\n<!-- PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture. -->\n<!-- This software is proprietary and subject to the terms of a specific License Agreement. -->\n\n"
}

EXT_MAP = {
    '.py': 'python',
    '.js': 'js',
    '.css': 'css',
    '.html': 'html',
    '.sh': 'shell',
    '.ps1': 'ps1'
}

EXCLUDE_DIRS = {'.git', 'node_modules', '__pycache__', '.idx', '.agent', '.github'}

def apply_header(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext not in EXT_MAP:
        return
    
    header_type = EXT_MAP[ext]
    header = HEADERS[header_type]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "Randall James Lujan. ALL RIGHTS RESERVED" in content:
            return
            
        # If the shorter version exists, replace it
        if "Randall Lujan. ALL RIGHTS RESERVED" in content:
            # We assume it looks like the header we just added
            old_text = "Randall Lujan. ALL RIGHTS RESERVED"
            new_text = "Randall James Lujan. ALL RIGHTS RESERVED"
            content = content.replace(old_text, new_text)
            new_content = content
        else:
            # Handle shebang
            if content.startswith('#!'):
                lines = content.split('\n', 1)
                new_content = lines[0] + '\n' + header + (lines[1] if len(lines) > 1 else "")
            else:
                new_content = header + content
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    root_dir = "."
    for root, dirs, files in os.walk(root_dir):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            apply_header(os.path.join(root, file))

if __name__ == "__main__":
    main()
