import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.collectors.uber_pdf.import_checker import import_already_exists

hash_teste = "da13511d5915b47c445bba38c708c59d8c0e3ab863e3378bf55d7df05ffa9b3b"

print(import_already_exists(hash_teste))
