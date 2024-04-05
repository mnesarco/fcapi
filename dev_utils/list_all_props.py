from pathlib import Path
import re

DIR = Path(__file__).parent

with open(Path(DIR, 'Properties.html'), 'r') as file:
    n = 4
    html = file.read()
    pattern = re.compile(r'id\s*=\s*"App::Property(.*?)"', re.MULTILINE) 
    all_unique = [f"'{p}'" for p in sorted(list(set(pattern.findall(html))))]
    chunked = [all_unique[i:i + n] for i in range(0, len(all_unique), n)]
    rows = [", ".join(chunk) for chunk in chunked]
    print(",\n".join(rows))
