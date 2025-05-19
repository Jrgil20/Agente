import argparse
from ingestion import load_csv, load_json, load_txt
from sentiment import get_chat_client, get_sentiment_score
from export import export_to_json, export_to_csv
from utils import clean_text, extract_hashtags, extract_keywords
from config import MODEL_DEPLOYMENT

KEYWORDS = ["golazo", "falta", "penal", "vinotinto", "mundial2026"]


def main():
    parser = argparse.ArgumentParser(description="Agente de análisis de sentimiento para la Vinotinto")
    parser.add_argument("--input", required=True, help="Archivo de entrada (CSV, JSON o TXT)")
    parser.add_argument("--output", required=True, help="Archivo de salida (JSON o CSV)")
    args = parser.parse_args()

    # Ingesta de datos
    if args.input.endswith(".csv"):
        df = load_csv(args.input)
    elif args.input.endswith(".json"):
        df = load_json(args.input)
    elif args.input.endswith(".txt"):
        df = load_txt(args.input)
    else:
        raise ValueError("Formato de archivo no soportado")

    chat_client = get_chat_client()
    resultados = []

    for _, row in df.iterrows():
        text = clean_text(row["text"])
        hashtags = extract_hashtags(text)
        keywords = extract_keywords(text, KEYWORDS)
        # Llamada al modelo generativo
        result = get_sentiment_score(text, chat_client, MODEL_DEPLOYMENT)
        # Aquí se asume que el modelo devuelve un JSON con score, label, etc.
        salida = {
            "tweet_id": row.get("tweet_id", ""),
            "username": row.get("username", ""),
            "text": row["text"],
            "created_at": row.get("created_at", ""),
            "score": result.get("score", 0),
            "label": result.get("label", "neutral"),
            "hashtags": hashtags,
            "keywords": keywords,
            "retweets": row.get("retweets", 0),
            "likes": row.get("likes", 0)
        }
        resultados.append(salida)

    if args.output.endswith(".json"):
        export_to_json(resultados, args.output)
    elif args.output.endswith(".csv"):
        export_to_csv(resultados, args.output)
    else:
        raise ValueError("Formato de salida no soportado")

    print(f"Exportación completada: {args.output}")


if __name__ == "__main__":
    main() 