# CUAD Contract Review Baselines (Improved)

Improved fork focused on raising **Qwen-based CUAD clause classification** above **66% accuracy**.

Original project: [MohammedAnber/CUAD-Contract-Review-Baselines](https://github.com/MohammedAnber/CUAD-Contract-Review-Baselines)

## What changed for classification quality

| Area | Before (typical pilot) | After (this branch) |
|------|------------------------|---------------------|
| Default model | `qwen2.5:1.5b` | **`qwen2.5:7b`** (still overridable) |
| Retrieval Top-K | 5 | **10** |
| Prompt | Basic candidate list | Candidate-constrained + explicit decision rules + safe abstention |
| Preprocessing | Minimal | Normalization + legal abbreviation expansion |
| Evaluation | Ad-hoc 10-row diagnostics | Reproducible eval harness |

Pilot diagnostics on the original 10-row fixed set showed ~40% accuracy, dominated by **retrieval misses**. The changes below target that bottleneck and the small-model classification errors.

## Recommended path to >66%

1. **Use a stronger local model** (highest single impact):
   ```bash
   ollama pull qwen2.5:7b
   # or qwen2.5:14b if you have VRAM
   export OLLAMA_MODEL=qwen2.5:7b
   ```

2. **Keep candidate constraint** (already in the improved prompt):
   - Only allow labels that appear in the retrieved Top-K.
   - Prefer `NO_APPLICABLE_LABEL` over inventing a category.

3. **Raise retrieval quality**:
   - `TOP_K=10` (default here).
   - Prefer hybrid dense + sparse retrieval when available.
   - Cleaner clause segmentation before embedding.

4. **Run the evaluation harness** on a fixed stratified set (not just 10 rows):
   ```bash
   python -m backend.eval.run_classification_eval --split test --limit 200
   ```

5. **Optional next steps** (not required for the first jump past 66%):
   - Light LoRA on the retrieval-augmented format.
   - Cross-encoder re-ranker on the Top-20.
   - Few-shot exemplars injected for high-confusion pairs.

## Quick start (classification path)

```bash
# 1. Environment
cp backend/.env.example backend/.env   # set COHERE_API_KEY, OLLAMA_URL, etc.

# 2. Prefer a 7B-class Qwen
export OLLAMA_MODEL=qwen2.5:7b
export TOP_K=10

# 3. Run your existing pipeline / diagnostics
# The improved prompt + config are drop-in compatible with the original
# classify_clause() orchestrator.
```

## Key files

- `backend/app/core/config.py` – stronger defaults (`qwen2.5:7b`, `TOP_K=10`)
- `backend/app/core/rag/prompt.py` – improved candidate-constrained prompt
- `backend/app/core/rag/text_preprocessor.py` – normalization utilities
- `backend/app/core/rag/generator.py` – notes + compatibility with stricter parsing
- `backend/eval/run_classification_eval.py` – reproducible evaluation entrypoint
- `docs/IMPROVEMENTS.md` – detailed rationale and next experiments

## Safety / legal note

Output is review support only. It is **not** legal advice.

## License

Same spirit as the upstream project; CUAD data remains under its original license (CC BY 4.0).
