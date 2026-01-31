import torch
from transformers import AutoModel
import time
import json
import re
import hashlib
from datetime import datetime

class ArcheologistV2:
    def __init__(self, model_name="zilliz/semantic-highlight-bilingual-v1"):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"📡 Inicializando Escáner Semántico en {self.device}...")
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True).to(self.device)
        self.vectores = {
            "infraestructura": "¿Qué entornos, hardware y librerías?",
            "ia_tecnica": "¿Qué modelos y benchmarks?",
            "arquitectura": "¿Cómo es la lógica de memoria y grafos?",
            "metafora": "¿Qué analogías y simbolismos se usan?",
            "identidad": "¿Cuál es la visión y propósito de Raúl?",
            "proyeccion": "¿Qué viene después? ¿Qué se propone?"
        }

    def get_metrics(self, text):
        words = len(text.split())
        sentences = len(re.split(r'[.!?]+', text))
        reading_time_min = words / 200 # Promedio humano
        return {
            "palabras": words,
            "oraciones": sentences,
            "tiempo_lectura_humana_min": round(reading_time_min, 2)
        }

    def find_smart_cuts(self, text, window_sentences=20):
        """
        Divide el texto en segmentos basados en cambios de 'masa semántica'.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        segments = []
        current_segment = []
        
        print(f"⛏️  Analizando {len(sentences)} oraciones para segmentación inteligente...")
        
        # Por ahora usamos una lógica de ventana con validación de relevancia
        # Futuro: Detectar rupturas de gradiente en los pesos de los 6 vectores
        for i in range(0, len(sentences), window_sentences):
            chunk = " ".join(sentences[i:i + window_sentences])
            segments.append(chunk)
            
        return segments

    def excavate_segment(self, segment, segment_id):
        print(f"  ⚡ Excavando Segmento {segment_id}...")
        metrics = self.get_metrics(segment)
        
        tensor = {}
        for vector, query in self.vectores.items():
            result = self.model.process(question=query, context=segment, threshold=0.4)
            tensor[vector] = {
                "contenido": result["highlighted_sentences"],
                "peso": round(float(sum(result.get("sentence_probabilities", [0])) / (len(result.get("sentence_probabilities", [1])) or 1)), 3)
            }

        # Generar firma única (Hash) para deduplicación
        content_hash = hashlib.sha256(segment.encode()).hexdigest()

        # Estructura compatible con Neo4j V3.0
        return {
            "ID_Nodo": f"ARK-SEG-{segment_id}-{int(time.time())}",
            "Hash": content_hash,
            "Metadatos": {
                "estrato": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "metricas": metrics
            },
            "Tensor_Trascendencia": tensor,
            "Relaciones_Sugeridas": [k for k, v in tensor.items() if v["peso"] > 0.5]
        }

    def process_document(self, path):
        with open(path, "r") as f:
            content = f.read()
        
        segments = self.find_smart_cuts(content)
        nodos_finales = []
        
        for idx, seg in enumerate(segments):
            nodo = self.excavate_segment(seg, idx)
            nodos_finales.append(nodo)
            
        return nodos_finales

if __name__ == "__main__":
    arch = ArcheologistV2()
    site_path = "/Users/crotalo/Downloads/Package Gemini Memory System_2.md"
    
    print(f"📂 Procesando: {site_path}")
    nodos = arch.process_document(site_path)
    
    output_path = "../data/nodos_granulares.json"
    with open(output_path, "w") as f:
        json.dump(nodos, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Proceso completado. {len(nodos)} nodos granulares creados en {output_path}")
