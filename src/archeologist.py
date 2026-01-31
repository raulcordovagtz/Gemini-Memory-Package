import torch
from transformers import AutoModel
import time
import json
from pathlib import Path

def run_archeologist():
    print("🏺 Iniciando Proceso de Excavación Arqueológica Cognitiva...")
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # 1. Carga del "Filtro de Precisión"
    model = AutoModel.from_pretrained(
        "zilliz/semantic-highlight-bilingual-v1",
        trust_remote_code=True
    ).to(device)

    # 2. El Sitio de Excavación (La Conversación)
    chat_path = "/Users/crotalo/Downloads/Virtual Environment Check.md"
    with open(chat_path, "r") as f:
        full_chat = f.read()

    # 3. Estratificación por Capas (Preguntas de Poda)
    estratos = {
        "hallazgo_tecnico": "¿Qué entorno virtual y modelos de IA se instalaron o probaron?",
        "intencion_estrategica": "¿Cuál es el objetivo final de usar el modelo de Zilliz en la memoria persistente?",
        "vector_humano": "¿Qué analogías o conceptos filosóficos (como arqueología) se usaron para describir el sistema?"
    }

    nodos_de_trascendencia = {}

    print(f"⛏️  Extrayendo estratos semánticos...")
    for capa, query in estratos.items():
        result = model.process(question=query, context=full_chat, threshold=0.4)
        nodos_de_trascendencia[capa] = result["highlighted_sentences"]

    # 4. Creación del Nodo Arqueológico (JSON de Trascendencia)
    nodo_final = {
        "meta": {
            "nodo_id": f"ARK-{int(time.time())}",
            "fecha": "2026-01-30",
            "sitio_original": chat_path
        },
        "estratos": nodos_de_trascendencia,
        "anclajes_clave": [
            "Zilliz Semantic Highlight",
            "Arqueología Cognitiva",
            "Nave Industrial",
            "Mínimo Semántico Reconstruible"
        ]
    }

    output_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/primer_hallazgo.json"
    with open(output_path, "w") as f:
        json.dump(nodo_final, f, indent=4, ensure_ascii=False)

    print(f"✅ Excavación terminada. Fragmento preservado en: {output_path}")
    
    # 5. Preparar el Prompt para el Reconstructor (Qwen 80B / 8B)
    prompt_reconstructor = f"""
    SISTEMA DE RECONSTRUCCIÓN ARQUEOLÓGICA
    --------------------------------------
    Eres un Reconstructor Cognitivo. Se te ha entregado un "Fragmento Semántico" (mínimo denominador).
    Tu tarea es reconstruir la narrativa completa de la charla original basándote en este fragmento
    y en tu vasto conocimiento sobre arquitectura de IA y flujos de trabajo de Gemini.

    FRAGMENTO EXTRAÍDO:
    {json.dumps(nodo_final['estratos'], indent=2, ensure_ascii=False)}

    INSTRUCCIÓN:
    Reconstruye la intención del usuario y los hitos técnicos logrados en esta sesión.
    Se verosímil y expande los conceptos de 'Arqueología Cognitiva'.
    """
    
    prompt_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/prompt_reconstruccion.txt"
    with open(prompt_path, "w") as f:
        f.write(prompt_reconstructor)
    
    print(f"📝 Prompt para Qwen generado en: {prompt_path}")

if __name__ == "__main__":
    run_archeologist()
