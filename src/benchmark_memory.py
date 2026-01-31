import torch
from transformers import AutoModel
import time
import numpy as np

def benchmark_semantic_highlight():
    print("🚀 Iniciando Benchmark de Memoria Persistente...")
    
    # 1. Detección de Dispositivo GPU (Apple Silicon)
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
        print("✅ GPU detectada: Apple Silicon (MPS)")
    else:
        print("⚠️ GPU no detectada, usando CPU.")

    # 2. Carga del Modelo
    print("📥 Cargando modelo zilliz/semantic-highlight-bilingual-v1...")
    start_load = time.time()
    model = AutoModel.from_pretrained(
        "zilliz/semantic-highlight-bilingual-v1",
        trust_remote_code=True
    ).to(device)
    load_time = time.time() - start_load
    print(f"⏱️ Modelo cargado en {load_time:.2f} segundos.")

    # 3. Datos de Prueba (Simulando una nota de Obsidian larga)
    question = "¿Cuál es la estrategia para la memoria persistente en el sistema Gemini?"
    context = """
    La memoria persistente se basa en la extracción de conceptos clave de las sesiones anteriores. 
    Utilizamos modelos de reranking y clasificación de tokens para podar el contexto innecesario.
    El agente debe ser capaz de recordar preferencias del usuario a largo plazo.
    La arquitectura de la Nave Industrial permite ejecutar procesos en segundo plano.
    El modelo atual se enfoca en resaltar oraciones semánticamente relevantes para una consulta dada.
    Esto reduce el ruido en un 70% aproximadamente antes de pasar la información al LLM principal.
    Los grafos de Neo4j sirven como estructura para almacenar estas relaciones.
    La velocidad de inferencia es crítica para mantener la interactividad en tiempo real.
    """ * 5  # Multiplicamos para tener un contexto más robusto (~40 oraciones)

    print(f"📄 Procesando contexto de prueba (~{len(context.split('.'))} oraciones)...")

    # 4. Inferencia y Medición
    latencies = []
    iterations = 10
    
    # Warm-up
    _ = model.process(question=question, context=context)

    for i in range(iterations):
        start_it = time.time()
        result = model.process(
            question=question,
            context=context,
            threshold=0.5
        )
        latencies.append(time.time() - start_it)
        print(f"  Iteration {i+1}/{iterations}: {latencies[-1]:.4f}s")

    avg_latency = np.mean(latencies)
    sentences_per_sec = (len(context.split('.')) * iterations) / sum(latencies)

    print("\n" + "="*40)
    print("📊 RESULTADOS DEL BENCHMARK")
    print("="*40)
    print(f"Latencia Promedio: {avg_latency*1000:.2f} ms")
    print(f"Throughput: {sentences_per_sec:.2f} oraciones/segundo")
    print(f"Capacidad de Tiempo Real: {'EXCELENTE' if avg_latency < 0.2 else 'ADECUADA'}")
    print("="*40)

if __name__ == "__main__":
    benchmark_semantic_highlight()
