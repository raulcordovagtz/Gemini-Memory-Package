import json
from neo4j import GraphDatabase
import time

class MemoryIngestor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clean_db(self):
        with self.driver.session() as session:
            print("🧹 Limpiando base de datos (Borrando todos los nodos y relaciones)...")
            session.run("MATCH (n) DETACH DELETE n")

    def ingest_nodos(self, nodos_file):
        with open(nodos_file, "r") as f:
            nodos = json.load(f)

        with self.driver.session() as session:
            print(f"📥 Inyectando {len(nodos)} nodos en la Malla de Memoria...")
            
            # 1. Crear Nodos
            for idx, nodo in enumerate(nodos):
                query = """
                MERGE (n:TranscendentNode {hash: $hash})
                ON CREATE SET 
                    n.id = $id,
                    n.seq_id = $seq_id,
                    n.source = $source,
                    n.timestamp = $timestamp,
                    n.words = $words,
                    n.sentences = $sentences,
                    n.reading_time = $reading_time,
                    n.w_infra = $w_infra,
                    n.w_ia = $w_ia,
                    n.w_arch = $w_arch,
                    n.w_meta = $w_meta,
                    n.w_id = $w_id,
                    n.w_proj = $w_proj,
                    n.content = $content
                """
                
                # Extraer pesos del tensor
                tensor = nodo["Tensor_Trascendencia"]
                
                session.run(query, 
                    hash=nodo["Hash"],
                    id=nodo["ID_Nodo"],
                    seq_id=idx,
                    source="Memoria_Persistente",
                    timestamp=nodo["Metadatos"]["estrato"],
                    words=nodo["Metadatos"]["metricas"]["palabras"],
                    sentences=nodo["Metadatos"]["metricas"]["oraciones"],
                    reading_time=nodo["Metadatos"]["metricas"]["tiempo_lectura_humana_min"],
                    w_infra=tensor["infraestructura"]["peso"],
                    w_ia=tensor["ia_tecnica"]["peso"],
                    w_arch=tensor["arquitectura"]["peso"],
                    w_meta=tensor["metafora"]["peso"],
                    w_id=tensor["identidad"]["peso"],
                    w_proj=tensor["proyeccion"]["peso"],
                    content="\n".join(tensor["infraestructura"]["contenido"] + 
                                     tensor["ia_tecnica"]["contenido"] + 
                                     tensor["arquitectura"]["contenido"] + 
                                     tensor["metafora"]["contenido"] + 
                                     tensor["identidad"]["contenido"] + 
                                     tensor["proyeccion"]["contenido"])
                )

            # 2. Crear Relaciones de Secuencia (Siguiente Evento)
            print("🔗 Tejiendo la secuencia cronológica...")
            session.run("""
                MATCH (n1:TranscendentNode), (n2:TranscendentNode)
                WHERE n2.seq_id = n1.seq_id + 1
                CREATE (n1)-[:NEXT_EVENT]->(n2)
            """)

    def query_sequence(self):
        with self.driver.session() as session:
            print("\n🔍 Ejecutando Query de Recuperación Arqueológica...")
            result = session.run("""
                MATCH (n:TranscendentNode)
                RETURN n.seq_id as id, n.timestamp as time, n.content as content
                ORDER BY n.seq_id ASC
            """)
            
            sequence = []
            for record in result:
                # Mostrar solo una parte del contenido para validar
                clean_content = record["content"][:100].replace("\n", " ") + "..."
                print(f"[{record['id']}] {record['time']} | {clean_content}")
                sequence.append(record)
            
            return sequence

if __name__ == "__main__":
    ingestor = MemoryIngestor()
    try:
        # Para ingesta incremental, comentamos clean_db()
        # ingestor.clean_db() 
        ingestor.ingest_nodos("../data/nodos_granulares.json")
        ingestor.query_sequence()
        print("\n✅ Malla de Memoria sincronizada con éxito en Neo4j.")
    except Exception as e:
        print(f"❌ Error en la operación Neo4j: {e}")
        print("\n💡 TIP: Asegúrate de que el password sea 'G-Obsidian-Vault'. Si no lo es, usa:")
        print("   cypher-shell -u neo4j -p 'tu_password_actual' \"ALTER USER neo4j SET PASSWORD 'G-Obsidian-Vault' CHANGE NOT REQUIRED\"")
    finally:
        ingestor.close()
