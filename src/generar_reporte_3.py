from neo4j import GraphDatabase
import json
import requests

class ArchaeologicalScanner:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_needle_path(self, needle_keyword):
        print(f"🕵️ Buscando la 'Aguja' semántica: '{needle_keyword}'...")
        with self.driver.session() as session:
            # 1. Encontrar el nodo que contiene la aguja
            search_query = """
            MATCH (n:TranscendentNode)
            WHERE toLower(n.content) CONTAINS toLower($keyword)
            RETURN n.seq_id as id, n.content as content
            LIMIT 1
            """
            needle_node = session.run(search_query, keyword=needle_keyword).single()
            
            if not needle_node:
                print("❌ Aguja no encontrada en el yacimiento.")
                return None

            needle_id = needle_node["id"]
            print(f"📍 Aguja localizada en el Nodo {needle_id}.")

            # 2. Encontrar el camino desde el origen hasta la aguja
            path_query = """
            MATCH (start:TranscendentNode {seq_id: 0}), (end:TranscendentNode {seq_id: $end_id})
            MATCH p = shortestPath((start)-[:NEXT_EVENT*]->(end))
            RETURN p
            """
            result = session.run(path_query, end_id=needle_id).single()
            
            if not result:
                print("❌ No hay una ruta lógica hacia la aguja.")
                return None

            path = result["p"]
            nodes_in_path = []
            for node in path.nodes:
                nodes_in_path.append({
                    "id": node["seq_id"],
                    "timestamp": node["timestamp"],
                    "content": node["content"]
                })
            
            return nodes_in_path

def generate_report_3(needle_path, needle_name):
    model_name = "qwen3:8b"
    ollama_url = "http://localhost:11434/api/generate"
    
    path_str = "\n".join([f"PASO {n['id']}: {n['content'][:200]}..." for n in needle_path])
    
    prompt = f"""
    Eres un 'Perceptor de Anomalías Arqueológicas'. 
    Has encontrado una 'Aguja' en el pajar de los datos: "{needle_name}".
    
    RUTA DE ACONTECIMIENTOS LÓGICOS:
    {path_str}
    
    TU TAREA:
    Describe cómo llegamos narrativamente a este punto.
    Explica la cadena de eventos y por qué este detalle (aunque parezca irrelevante)
    representa un "agujero de guion" o una curiosidad de la sesión.
    """
    
    print(f"🧬 Generando narrativa de la Aguja con {model_name}...")
    try:
        response = requests.post(ollama_url, json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    scanner = ArchaeologicalScanner()
    # Nuestra "Aguja": La mención de Alicia en el País de las Maravillas
    # Es irrelevante para la base de datos pero clave para el test de calidad.
    needle_name = "Alicia en el País de las Maravillas"
    path = scanner.find_needle_path("Alicia")
    
    if path:
        narrativa = generate_report_3(path, needle_name)
        
        output_path = "/Users/crotalo/desarrollo-local/G-Obsidian-Vault/Gemini/Memoria Persistente Gemini/REPORTES_EVALUACION/reporte_3_aguja_pajar.md"
        with open(output_path, "w") as f:
            f.write(f"# Reporte 3: La Aguja en el Pajar Semántico\n\n")
            f.write(f"**Aguja Identificada:** {needle_name}\n\n")
            f.write(f"## Narrativa de la Trayectoria\n")
            f.write(narrativa)
            
        print(f"✅ Reporte 3 generado en {output_path}")
    
    scanner.close()
