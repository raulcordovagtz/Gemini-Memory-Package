# 🧠 Gemini Memory Package (GMP)

> **Persistent Memory System for AI Agents based on Cognitive Archaeology**

This package implements a multi-dimensional semantic memory system that allows an AI agent to maintain, compress, and reconstruct long-term context using the "Cognitive Archaeology" approach.

## 📁 Project Structure

- `src/`: Core archaeological scripts.
  - `archeologist_v2.py`: Intelligent text segmentation and tensor extraction (6D).
  - `neo4j_ingest.py`: Graph database synchronization.
  - `neo4j_query.py`: Pattern retrieval and narrative inflation.
  - `ollama_reconstructor.py`: Narrative legacy generator.
- `data/`: Sample JSON tensors and granular nodes.
- `docs/`: Evaluation reports, field notebooks, and reconstructed narratives.
- `config/`: LSP and environment configurations.
- `requirements.txt`: Minimal dependencies for replicability.

## 🚀 Quick Start (Replication)

### 1. Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

Ensure **Neo4j** is running (e.g., via Homebrew) and set the user/password.
Default used in this package: `user: neo4j`, `password: G-Obsidian-Vault`.

### 3. Execution Pipeline

1. **Excavation**: Use `archeologist_v2.py` to process a text file.
2. **Ingestion**: Run `neo4j_ingest.py` to save nodes into the graph.
3. **Reconstruction**: Use `neo4j_query.py` to inflate the narrative using local LLMs (Ollama).

## 🧪 Technical Specifications

- **Embedding Model**: `zilliz/semantic-highlight-bilingual-v1` (Quantized/Fast).
- **Inference Latency**: ~319 sentences/sec on Apple Silicon (MPS).
- **Tensor Dimensions**: Infrastructure, AI Technique, Architecture, Metaphor, Identity, Projection.

---
**Maintained by**: Gemini / Antigravity Agent  
**Status**: V1.0 Stable - Validated (9.8/10 Integrity Score)
