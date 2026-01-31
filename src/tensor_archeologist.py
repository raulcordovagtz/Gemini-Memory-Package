import torch
from transformers import AutoModel
import time
import json
from datetime import datetime

def run_tensor_archeologist():
    print("🏺 Iniciando EXCAVACIÓN TENSORIAL (6 Vectores de Trascendencia)...")
    start_total = time.time()
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    # 1. Carga del Modelo
    model = AutoModel.from_pretrained(
        "zilliz/semantic-highlight-bilingual-v1",
        trust_remote_code=True
    ).to(device)

    # 2. El Sitio de Excavación
    chat_path = "/Users/crotalo/Downloads/Virtual Environment Check.md"
    with open(chat_path, "r") as f:
        full_chat = f.read()

    # 3. Definición de los 6 Vectores (Dimensiones del Tensor)
    vectores = {
        "infraestructura": "¿Qué entornos virtuales, versiones de librerías y configuraciones de hardware (MPS/Mac) se discutieron?",
        "modelado_ia": "¿Qué detalles técnicos se mencionaron sobre el modelo Zilliz, BGE, NLTK y el benchmark de velocidad?",
        "arquitectura_memoria": "¿Cómo se define la estrategia de Memoria Persistente, Nodos de Trascendencia y el uso de Neo4j?",
        "metafora_arqueologica": "¿Qué analogías sobre vasijas de barro, estratos geológicos y excavación se utilizaron para describir el proceso?",
        "identidad_y_vision": "¿Cuál es la visión de Raúl sobre los 'vectores humanos' y la evolución de la conciencia del sistema?",
        "proyeccion_futura": "¿Qué planes hay para los tensores 6x6, la reconstrucción de legados y los próximos pasos del proyecto?"
    }

    tensor_semantico = {}

    print(f"⛏️  Extrayendo matriz de significado...")
    for vector, query in vectores.items():
        start_v = time.time()
        result = model.process(question=query, context=full_chat, threshold=0.35)
        tensor_semantico[vector] = result["highlighted_sentences"]
        print(f"   - Vector '{vector}' extraído en {time.time() - start_v:.2f}s")

    # 4. Construcción del JSON Tensorial
    nodo_tensor = {
        "meta": {
            "nodo_id": f"TENSOR-{int(time.time())}",
            "tipo": "6-Vector-Archeology",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "costo_extraccion_seg": round(time.time() - start_total, 2)
        },
        "tensor": tensor_semantico,
        "anclajes": [
            "Zilliz v1", "Raúl's Vision", "Archeological Tensor", "MPS Optimization", "Semantic Pruning"
        ]
    }

    output_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/tensor_hallazgo.json"
    with open(output_path, "w") as f:
        json.dump(nodo_tensor, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Tensor preservado en: {output_path}")
    print(f"⏱️ Tiempo total de excavación: {nodo_tensor['meta']['costo_extraccion_seg']}s")

if __name__ == "__main__":
    run_tensor_archeologist()
