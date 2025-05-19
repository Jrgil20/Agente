import pandas as pd
from typing import List, Dict


def export_to_json(data: List[Dict], file_path: str):
    """Exporta los resultados a un archivo JSON."""
    df = pd.DataFrame(data)
    df.to_json(file_path, orient="records", force_ascii=False, indent=2)


def export_to_csv(data: List[Dict], file_path: str):
    """Exporta los resultados a un archivo CSV."""
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding="utf-8") 