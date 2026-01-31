import torch
from transformers import AutoModel
import time

def semantic_quality_check():
    print("🧠 Iniciando Prueba de Calidad Semántica: Alicia en el País de las Maravillas")
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    
    print("📥 Cargando modelo...")
    model = AutoModel.from_pretrained(
        "zilliz/semantic-highlight-bilingual-v1",
        trust_remote_code=True
    ).to(device)

    # --- CASO 1: INGLÉS (Nativo del modelo) ---
    question_en = "Why was the Rabbit in a hurry and what did he take out of his pocket?"
    context_en = """
    Alice was beginning to get very tired of sitting by her sister on the bank.
    Suddenly a White Rabbit with pink eyes ran close by her.
    There was nothing so VERY remarkable in that; nor did Alice think it so VERY much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!'
    But when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT-POCKET, and looked at it, and then hurried on, Alice started to her feet.
    It flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it.
    Burning with curiosity, she ran across the field after it.
    She was just in time to see it pop down a large rabbit-hole under the hedge.
    """

    # --- CASO 2: ESPAÑOL (Prueba de fuego) ---
    question_es = "¿Por qué tenía prisa el conejo y qué sacó de su bolsillo?"
    context_es = """
    Alicia empezaba a cansarse de estar sentada con su hermana a la orilla del río.
    De repente, un Conejo Blanco de ojos rosados pasó corriendo cerca de ella.
    No había nada de MUY notable en ello; ni Alicia pensó que fuera MUY fuera de lo común oír al Conejo decirse a sí mismo: '¡Ay Dios! ¡Ay Dios! ¡Voy a llegar tarde!'
    Pero cuando el Conejo realmente SACÓ UN RELOJ DE SU BOLSILLO DEL CHALECO, lo miró y luego siguió apresurado, Alicia se puso en pie de un salto.
    Cruzó por su mente que nunca antes había visto a un conejo con un bolsillo en el chaleco, ni un reloj para sacar de él.
    Ardiendo de curiosidad, corrió por el campo tras él.
    Llegó justo a tiempo para verlo bajar por una madriguera bajo el seto.
    """

    def test_language(name, q, c):
        print(f"\n--- PRUEBA: {name} ---")
        print(f"Pregunta: {q}")
        result = model.process(question=q, context=c, threshold=0.3)
        highlighted = result["highlighted_sentences"]
        
        print(f"Resultados encontrados ({len(highlighted)} oraciones):")
        for i, sent in enumerate(highlighted, 1):
            print(f"  {i}. {sent.strip()}")
        
        # Análisis de "Mínimo Semántico"
        compression = result.get("compression_rate", 0)
        print(f"Tasa de Compresión: {compression:.2%}")

    # Ejecutar pruebas
    test_language("INGLÉS", question_en, context_en)
    test_language("ESPAÑOL", question_es, context_es)

if __name__ == "__main__":
    semantic_quality_check()
