import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.collectors.uber_pdf.hash_utils import calculate_file_hash

pdf_path = "data/raw/uber/relatorio.pdf"

print(calculate_file_hash(pdf_path))
