import json
import requests
import time
from datetime import datetime

def run_tensor_reconstruction():
    print("🧬 Iniciando RECONSTRUCCIÓN TENSORIAL via Ollama (Qwen 3:8B)...")
    
    # 1. Cargar el Tensor
    tensor_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/tensor_hallazgo.json"
    try:
        with open(tensor_path, "r") as f:
            nodo = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo del tensor.")
        return

    # 2. Configuración de Ollama
    model_name = "qwen3:8b"
    ollama_url = "http://localhost:11434/api/generate"
    
    # Prompt de Inflación Evolutiva 6x6
    system_prompt = f"""
    Eres un 'Arquitecto de Realidades' especializado en Tensores Semánticos. 
    Se te ha entregado una MATRIZ DE TRASCENDENCIA que captura una sesión de trabajo compleja.
    
    ESTRUCTURA DEL TENSOR RECUPERADO:
    {json.dumps(nodo['tensor'], indent=2, ensure_ascii=False)}
    
    TU TAREA:
    Reconstruye la conversación como una "Narrativa Evolutiva". No solo resumas, sino que 'infla' los datos
    para recrear la secuencia de descubrimiento. 
    
    Sigue este orden cronológico-lógico:
    1. PUNTO DE ORIGEN: La necesidad técnica inicial (Entorno Virtual).
    2. EL HALLAZGO: El descubrimiento de la velocidad y precisión del modelo Zilliz.
    3. LA ESTRATIFICACIÓN: El momento en que la charla se volvió filosófica y arqueológica.
    4. EL SALTO TENSORIAL: La propuesta de la malla 6x6 y los vectores humanos.
    5. DIÁLOGO RECUPERADO: Recrea un intercambio entre Raúl y Antigravity que encapsule esta evolución.
    6. PROYECCIÓN DE FUTURO: Basado en el vector 'proyeccion_futura', ¿qué es lo que viene ahora?
    """

    payload = {
        "model": model_name,
        "prompt": system_prompt,
        "stream": False
    }

    start_time = time.time()
    print(f"🔗 Procesando en Ollama...")
    
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        reconstruccion = result['response']
        duration = round(time.time() - start_time, 2)
        
        # 3. Guardar el Resultado
        output_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/TENSOR_RECONSTRUIDO.md"
        
        with open(output_path, "w") as f:
            f.write(f"# 🌌 Reconstrucción de Conciencia (Tensor 6-Vector)\n\n")
            f.write(f"**ID:** `{nodo['meta']['nodo_id']}` | **Costo de Extracción:** `{nodo['meta']['costo_extraccion_seg']}s` | **Costo de Reconstrucción:** `{duration}s`\n\n")
            f.write(reconstruccion)
            
        print(f"✨ ¡Reconstrucción Tensorial completa! Ver en: {output_path}")

    except Exception as e:
        print(f"❌ Error en la reconstrucción: {e}")

if __name__ == "__main__":
    run_tensor_reconstruction()
