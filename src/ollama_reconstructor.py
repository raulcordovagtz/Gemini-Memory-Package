import json
import requests
import time
from datetime import datetime

def ollama_reconstructor():
    print("🧬 Iniciando Reconstrucción Genética de Memoria via Ollama...")
    
    # 1. Cargar el Hallazgo Arqueológico
    hallazgo_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/primer_hallazgo.json"
    try:
        with open(hallazgo_path, "r") as f:
            nodo = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo del hallazgo.")
        return

    # 2. Configuración del "Arquitecto de Legados"
    model_name = "qwen3:8b" # Usamos el Qwen 8B que mencionaste en Ollama
    ollama_url = "http://localhost:11434/api/generate"
    
    timestamp = datetime.fromtimestamp(int(nodo['meta']['nodo_id'].split('-')[1])).strftime('%Y-%m-%d %H:%M:%S')
    
    # Construcción del Prompt Arqueológico
    system_prompt = f"""
    Eres un 'Arquitecto de Legados'. Tu misión es reconstruir la evolución de una consciencia 
    basándote en fragmentos arqueológicos (nodos de trascendencia).
    
    DATOS DEL ESTRATO:
    - Fecha/Hora: {timestamp}
    - Usuario: Raúl (Investigador principal de la Nave Industrial)
    - Agente: Gemini/Antigravity (Sistema Operativo Cognitivo)
    
    HALLAZGOS SEMÁNTICOS RECUPERADOS:
    {json.dumps(nodo['estratos'], indent=2, ensure_ascii=False)}
    
    INSTRUCCIÓN DE RECONSTRUCCIÓN:
    1. Traza la línea de evolución del pensamiento en esta charla.
    2. Identifica el 'Momento de Trascendencia' (donde la idea cambió de forma).
    3. Reconstruye un breve diálogo verosímil que pudo haber ocurrido, capturando el tono filosófico y técnico.
    4. Proyecta qué debería ser el siguiente paso en este legado.
    """

    payload = {
        "model": model_name,
        "prompt": system_prompt,
        "stream": False
    }

    print(f"🔗 Conectando con Ollama ({model_name})...")
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        reconstruccion = result['response']
        
        # 3. Guardar el Legado Reconstruido
        output_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/LEGADO_RECONSTRUIDO.md"
        
        with open(output_path, "w") as f:
            f.write(f"# 🏛️ Legado de Memoria Reconstruido\n\n")
            f.write(f"**ID del Nodo:** `{nodo['meta']['nodo_id']}`\n")
            f.write(f"**Fecha del Estrato:** `{timestamp}`\n\n")
            f.write(f"## Narrativa de la Evolución\n")
            f.write(reconstruccion)
            f.write(f"\n\n---\n*Reconstrucción generada por {model_name} el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
            
        print(f"✨ ¡Legado reconstruido con éxito! Ver en: {output_path}")

    except Exception as e:
        print(f"❌ Error al conectar con Ollama: {e}")

if __name__ == "__main__":
    ollama_reconstructor()
