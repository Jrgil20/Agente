import pandas as pd
from typing import List

REQUIRED_FIELDS = ["tweet_id", "username", "text", "created_at"]
OPTIONAL_FIELDS = ["retweets", "likes"]


def load_csv(file_path: str) -> pd.DataFrame:
    """Carga datos desde un archivo CSV y valida los campos requeridos."""
    df = pd.read_csv(file_path)
    validate_fields(df)
    return df


def load_json(file_path: str) -> pd.DataFrame:
    """Carga datos desde un archivo JSON y valida los campos requeridos."""
    df = pd.read_json(file_path)
    validate_fields(df)
    return df


def load_txt(file_path: str) -> pd.DataFrame:
    """Carga datos desde un archivo de texto plano (un comentario por línea)."""
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    df = pd.DataFrame({"text": [line.strip() for line in lines]})
    # Generar campos mínimos
    df["tweet_id"] = df.index.astype(str)
    df["username"] = "anon"
    df["created_at"] = None
    return df


def validate_fields(df: pd.DataFrame):
    """Valida que el DataFrame tenga los campos requeridos."""
    for field in REQUIRED_FIELDS:
        if field not in df.columns:
            raise ValueError(f"Falta el campo requerido: {field}") 