import argparse
from ingestion import load_csv, load_json, load_txt
from sentiment import get_chat_client, get_sentiment_score, get_agent_client
from export import export_to_json, export_to_csv
from utils import clean_text, extract_hashtags, extract_keywords
from config import MODEL_DEPLOYMENT

KEYWORDS = ["golazo", "falta", "penal", "vinotinto", "mundial2026"]


def main():
    parser = argparse.ArgumentParser(description="Agente de análisis de sentimiento para la Vinotinto")
    parser.add_argument("--input", required=True, help="Archivo de entrada (CSV, JSON o TXT)")
    parser.add_argument("--output", required=True, help="Archivo de salida (JSON o CSV)")
    parser.add_argument("--force-openai", action="store_true", help="Forzar uso de OpenAI en lugar del agente")
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

    # Selección automática: si existe PROJECT_CONNECTION usa el agente, si no usa OpenAI directo
    if not args.force_openai:
        try:
            agent_client = get_agent_client()
            use_agent = True
        except Exception as e:
            print(f"Warning: No se pudo inicializar el agente ({str(e)}), usando OpenAI")
            chat_client = get_chat_client()
            use_agent = False
    else:
        chat_client = get_chat_client()
        use_agent = False

    resultados = []

    for _, row in df.iterrows():
        text = clean_text(row["text"])
        hashtags = extract_hashtags(text)
        keywords = extract_keywords(text, KEYWORDS)
        if use_agent:
            result = get_sentiment_score(text, agent_client)
        else:
            result = get_sentiment_score(text, chat_client, MODEL_DEPLOYMENT)
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