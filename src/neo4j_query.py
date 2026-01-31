from neo4j import GraphDatabase
import json
import requests
import time

class MemoryQuerier:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_time_lapse(self, source="Memoria_Persistente"):
        with self.driver.session() as session:
            print(f"📊 Recuperando Progresión de Eventos (Source: {source})...")
            result = session.run("""
                MATCH (p:TranscendentNode {source: $source})
                WITH p ORDER BY p.seq_id ASC
                MATCH path = (p)-[:NEXT_EVENT*0..]->(next)
                WITH p, count(path) as event_order
                RETURN p.seq_id as id, p.timestamp as time, p.content as content
                ORDER BY p.seq_id ASC
            """, source=source)
            
            return [dict(record) for record in result]

    def get_high_impact_nodes(self, threshold=0.6):
        with self.driver.session() as session:
            print(f"🔥 Buscando Nodos de Alto Impacto (Identidad/Visión > {threshold})...")
            result = session.run("""
                MATCH (n:TranscendentNode)
                WHERE n.w_id > $threshold OR n.w_proj > $threshold
                RETURN n.seq_id as id, n.w_id as identity_weight, n.w_proj as projection_weight, n.content as content
                ORDER BY n.seq_id ASC
            """, threshold=threshold)
            return [dict(record) for record in result]

def inflate_with_ollama(nodes_data):
    model_name = "qwen3:8b"
    ollama_url = "http://localhost:11434/api/generate"
    
    context_text = "\n---\n".join([f"EVENTO {n['id']} [{n['time']}]: {n['content']}" for n in nodes_data])
    
    system_prompt = f"""
    Eres un 'Reconstructor Galáctico de Memoria'. 
    Has recuperado una secuencia de fragmentos de una base de datos de grafos (Neo4j).
    
    SECUENCIA RECUPERADA:
    {context_text}
    
    TU TAREA:
    1. Reconstruye la narrativa completa de esta "sesión de trabajo".
    2. Explica cómo la charla evolucionó desde la infraestructura básica hasta la metafísica de los tensores.
    3. Identifica el clímax de la conversación.
    4. Usa un tono que refleje la importancia de este legado arqueológico.
    """

    print(f"🧬 'Inflando' la secuencia con {model_name}...")
    try:
        response = requests.post(ollama_url, json={
            "model": model_name,
            "prompt": system_prompt,
            "stream": False
        })
        return response.json()['response']
    except Exception as e:
        return f"Error en Ollama: {e}"

if __name__ == "__main__":
    querier = MemoryQuerier()
    try:
        # 1. Recuperar secuencia cronológica
        lapse = querier.get_time_lapse()
        
        # 2. Guardar resultados
        output_path = "../docs/RECUPERACION_GRAFO.md"
        
        with open(output_path, "w") as f:
            f.write("# 📡 Recuperación de Malla Neo4j\n\n")
            f.write("## 1. Progresión Temporal (Time-Lapse)\n")
            for node in lapse:
                f.write(f"### Nodo {node['id']} ({node['time']})\n")
                f.write(f"{node['content']}\n\n")
        
        print(f"✨ Secuencia recuperada en: {output_path}")
        
        # 3. Inflar la narrativa
        narrativa = inflate_with_ollama(lapse)
        
        with open("../docs/RECONSTRUCCION_GRAFO_FINAL.md", "w") as f:
            f.write("# 🌌 Reconstrucción Final desde el Grafo\n\n")
            f.write(narrativa)
            
        print("✨ Narrativa inflada con éxito.")
        
    finally:
        querier.close()
