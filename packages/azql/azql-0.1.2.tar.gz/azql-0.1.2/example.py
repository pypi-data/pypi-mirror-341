from pathlib import Path

import azql

fp = Path("data")
script = azql.convert(fp, output_dir="tmp", schema="stage")
print(script)
