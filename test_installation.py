#!/usr/bin/env python3
"""
Script de prueba para verificar la instalación de dependencias
"""

def test_imports():
    """Prueba que todas las dependencias se puedan importar correctamente"""
    try:
        print("Probando importaciones...")
        
        # Azure dependencies
        import azure.mgmt.resource
        print("✓ azure-mgmt-resource")
        
        import azure.identity
        print("✓ azure-identity")
        
        import azure.ai.ml
        print("✓ azure-ai-ml")
        
        # OpenAI
        import openai
        print("✓ openai")
        
        # Python dotenv
        import dotenv
        print("✓ python-dotenv")
        
        # Standard libraries
        import pandas
        print("✓ pandas")
        
        print("\n✅ Todas las dependencias se importaron correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando dependencia: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_basic_functionality():
    """Prueba funcionalidad básica del proyecto"""
    try:
        print("\nProbando funcionalidad básica...")
        
        # Test config
        from src.config import MODEL_DEPLOYMENT
        print("✓ Configuración cargada")
        
        # Test utils
        from src.utils import clean_text, extract_hashtags
        test_text = "¡Qué golazo de la #Vinotinto! https://t.co/example"
        cleaned = clean_text(test_text)
        hashtags = extract_hashtags(test_text)
        print(f"✓ Utils funcionando: texto limpio = '{cleaned}', hashtags = {hashtags}")
        
        # Test ingestion
        from src.ingestion import load_csv
        print("✓ Módulo de ingesta disponible")
        
        # Test export
        from src.export import export_to_json
        print("✓ Módulo de exportación disponible")
        
        print("✅ Funcionalidad básica verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

if __name__ == "__main__":
    print("=== Prueba de Instalación del Proyecto ===\n")
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    if imports_ok and functionality_ok:
        print("\n🎉 ¡Instalación completada exitosamente!")
        print("\nPróximos pasos:")
        print("1. Copia env.example a .env")
        print("2. Configura tus credenciales de Azure en .env")
        print("3. Ejecuta: python src/chat_app.py --input tweets.csv --output results.json")
    else:
        print("\n❌ Hay problemas con la instalación. Revisa los errores arriba.") 