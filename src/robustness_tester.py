import hashlib
import re
import json
from neo4j import GraphDatabase

class RobustnessTester:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.existing_hashes = self._get_known_hashes()

    def _get_known_hashes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:TranscendentNode) WHERE n.hash IS NOT NULL RETURN n.hash as hash")
            return {record["hash"] for record in result}

    def close(self):
        self.driver.close()

    def analyze_file(self, file_path, window_sentences=20):
        print(f"🧐 Iniciando Auditoría de Robustez (Fase Beta)...")
        print(f"📂 Archivo Objetivo: {file_path}")
        
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return

        sentences = re.split(r'(?<=[.!?])\s+', content)
        segments = []
        for i in range(0, len(sentences), window_sentences):
            segments.append(" ".join(sentences[i:i + window_sentences]))

        print(f"🔍 Se han identificado {len(segments)} segmentos potenciales en el texto graso.")
        
        duplicates = 0
        new_segments = 0
        
        for idx, seg in enumerate(segments):
            h = hashlib.sha256(seg.encode()).hexdigest()
            if h in self.existing_hashes:
                print(f"  [OLD] Segmento {idx}: Detectado en la malla (Hash: {h[:8]}...)")
                duplicates += 1
            else:
                print(f"  [NEW] Segmento {idx}: ¡NUEVO ESTRATO! (Hash: {h[:8]}...)")
                new_segments += 1

        print("\n📊 RESULTADO DE LA AUDITORÍA:")
        print(f"✅ Nodos conocidos (Deduplicados): {duplicates}")
        print(f"🌟 Nodos nuevos (Pendientes): {new_segments}")
        
        if new_segments > 0:
            print(f"💡 El sistema está listo para inyectar los {new_segments} nuevos hallazgos sin corromper el pasado.")
        else:
            print("🛡️  Robustez Confirmada: No hay datos nuevos, la malla está íntegra.")

if __name__ == "__main__":
    target = "/Users/crotalo/Downloads/Package Gemini Memory System_2.md"
    tester = RobustnessTester()
    try:
        tester.analyze_file(target)
    finally:
        tester.close()
