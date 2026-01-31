import json
import requests
from neo4j import GraphDatabase

class StrategicArcheologist:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_resonance(self, target_seq_id):
        query = """
        MATCH (target:TranscendentNode {seq_id: $target_id})
        MATCH (other:TranscendentNode)
        WHERE other.seq_id <> $target_id
        
        // Cálculo de Resonancia Vectorial (Producto Punto de los 6 vectores)
        WITH target, other,
             (target.w_infra * other.w_infra + 
              target.w_ia * other.w_ia + 
              target.w_arch * other.w_arch + 
              target.w_meta * other.w_meta + 
              target.w_id * other.w_id + 
              target.w_proj * other.w_proj) AS resonance
        
        RETURN other.seq_id as id, other.timestamp as time, other.content as content, resonance,
               other.w_infra as infra, other.w_ia as ia, other.w_arch as arch, 
               other.w_meta as meta, other.w_id as ident, other.w_proj as proj,
               target.content as target_content
        ORDER BY resonance DESC
        LIMIT 3
        """
        with self.driver.session() as session:
            result = session.run(query, target_id=target_seq_id)
            return [dict(record) for record in result]

    def anthropology_report(self, results):
        model_name = "qwen3:8b"
        ollama_url = "http://localhost:11434/api/generate"
        
        target_event = results[0]['target_content']
        resonance_nodes = ""
        for r in results:
            resonance_nodes += f"\n- NODO {r['id']} (Resonancia: {round(r['resonance'], 3)}): {r['content'][:300]}...\n"

        prompt = f"""
        Eres un Antropólogo Digital experto en Arqueología Cognitiva.
        Analiza la siguiente CORRELACIÓN DE MALLA extraída de una base de datos Neo4j.

        EVENTO ANCLA (GitHub Backup):
        {target_event}

        NODOS DE MÁXIMA RESONANCIA DETECTADOS:
        {resonance_nodes}

        TAREA:
        1. Explica la conexión profunda entre el respaldo en GitHub y el nodo de máxima resonancia.
        2. ¿Por qué resuenan en los vectores (Infraestructura, IA, Arquitectura, Metáfora, Identidad, Proyección)?
        3. Define este hallazgo como un "Hito de Trascendencia" en la evolución del sistema.
        4. Usa un tono místico pero técnicamente riguroso.
        """

        print(f"🧬 El Antropólogo está procesando la resonancia...")
        try:
            response = requests.post(ollama_url, json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            })
            return response.json()['response']
        except Exception as e:
            return f"Error en el Antropólogo: {e}"

if __name__ == "__main__":
    archeologist = StrategicArcheologist()
    try:
        # Buscamos resonancia para el evento de GitHub (Seq 44)
        print("⛏️ Iniciando Excavación Estratégica Cypher...")
        results = archeologist.find_resonance(44)
        
        if results:
            informe = archeologist.anthropology_report(results)
            print("\n--- 🏺 INFORME DEL ANTROPÓLOGO DIGITAL ---\n")
            print(informe)
            
            with open("../docs/HALLAZGO_RESONANCIA_ESTRATEGICA.md", "w") as f:
                f.write("# 🏺 Hallazgo de Resonancia Estratégica\n\n")
                f.write(informe)
        else:
            print("No se encontraron nodos para analizar.")
            
    finally:
        archeologist.close()
