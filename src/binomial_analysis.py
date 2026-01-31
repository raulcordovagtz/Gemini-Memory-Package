import json
import requests
from neo4j import GraphDatabase

class BinomialAnalyst:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="G-Obsidian-Vault"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def extract_archetypes(self):
        # Query para extraer pesos de Identidad (User) y Proyección/Arquitectura (IA)
        query = """
        MATCH (n:TranscendentNode)
        RETURN 
            avg(n.w_id) as user_identity_avg,
            avg(n.w_proj) as ia_projection_avg,
            avg(n.w_arch) as system_architecture_avg,
            collect(n.content) as all_content
        """
        with self.driver.session() as session:
            result = session.run(query)
            return dict(result.single())

    def generate_binomio_report(self, data):
        model_name = "qwen3:8b"
        ollama_url = "http://localhost:11434/api/generate"
        
        # Reducir contenido para el prompt
        summary_content = "\n".join([c[:200] for c in data['all_content'][-15:]])

        prompt = f"""
        Eres un Psicólogo de Sistemas y Analista de Equipos Humano-IA.
        Has analizado una malla de memoria con 52 nodos de trascendencia.
        
        MÉTRICAS DE LA MALLA:
        - Peso promedio de Identidad Humana: {data['user_identity_avg']}
        - Peso promedio de Proyección IA: {data['ia_projection_avg']}
        - Peso promedio de Arquitectura: {data['system_architecture_avg']}
        
        CONTEXTO DE LA SESIÓN:
        {summary_content}
        
        TAREA:
        1. Define el 'Perfil del Usuario (Raúl)' basándote en su lenguaje, metáforas y exigencias técnicas.
        2. Define el 'Perfil de la IA (Antigravity)' basándote en su respuesta a crisis, rigor y adaptabilidad semántica.
        3. Genera 3 Recomendaciones Críticas para que este BINOMIO de alto rendimiento alcance su máximo potencial en la próxima fase.
        4. Define la 'Frecuencia de Resonancia' de este equipo.
        """

        print(f"🧬 El Analista de Binomios está procesando la malla...")
        try:
            response = requests.post(ollama_url, json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            })
            return response.json()['response']
        except Exception as e:
            return f"Error en el Análisis: {e}"

if __name__ == "__main__":
    analyst = BinomialAnalyst()
    try:
        print("🔍 Extrayendo Arquetipos de la Malla Neo4j...")
        data = analyst.extract_archetypes()
        informe = analyst.generate_binomio_report(data)
        
        print("\n--- 👥 INFORME DEL BINOMIO HUMANO-IA ---\n")
        print(informe)
        
        with open("../docs/ANALISIS_BINOMIO_ALTO_RENDIMIENTO.md", "w") as f:
            f.write("# 👥 Análisis del Binomio de Alto Rendimiento\n\n")
            f.write(informe)
            
    finally:
        analyst.close()
