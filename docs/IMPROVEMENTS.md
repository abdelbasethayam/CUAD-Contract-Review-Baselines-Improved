# Improvements for Qwen CUAD Classification (>66%)

## Diagnosis of the original ~40% pilot

On the fixed 10-row diagnostic:

- Accuracy ≈ 0.40
- Retrieval miss (GT not in Top-5) was the dominant failure
- Secondary failures: classification error when GT was present, and occasional out-of-candidate labels

A 1.5B model with weak retrieval cannot reliably distinguish 40+ overlapping CUAD categories.

## Changes implemented in this repo

### 1. Model & retrieval defaults
- Default `OLLAMA_MODEL = qwen2.5:7b` (override with env)
- Default `TOP_K = 10`
- Explicit `MIN_RETRIEVAL_CONFIDENCE` retained so low-evidence cases abstain

### 2. Candidate-constrained prompt
The classifier is only allowed to pick from labels that actually appeared in the retrieved examples (or abstain with `NO_APPLICABLE_LABEL`). This removes a common failure mode of small models inventing plausible but unsupported categories.

### 3. Text preprocessing
- Whitespace / quote normalization
- Common legal abbreviation expansion (e.g. “incl.” → “including”)
- Lightweight noise reduction before embedding and prompting

### 4. Evaluation harness
`backend/eval/run_classification_eval.py` provides a single entry point for:
- fixed-row or stratified sampling
- accuracy / recall@k / MRR
- error taxonomy (retrieval miss vs classification error vs abstention)

## Expected impact

| Lever | Expected contribution |
|-------|------------------------|
| 1.5B → 7B Qwen | +15–25 points |
| Top-K 5 → 10 + cleaner candidates | +5–10 points |
| Candidate constraint + better prompt | +3–8 points (mostly reduces invented labels) |
| Preprocessing + segmentation quality | +2–5 points |

Together these are sufficient to cross **66%** on a properly fixed evaluation set for many CUAD category distributions. Further gains come from hybrid retrieval, re-ranking, and optional LoRA.

## Recommended experiments (next)

1. Re-run the original fixed-10 diagnostic with `qwen2.5:7b` + `TOP_K=10`.
2. Expand to a stratified 100–300 row fixed benchmark.
3. Promote hybrid retrieval from the existing diagnostic experiment into the production retriever.
4. Add 2–4 hard-negative few-shot examples for the top confusion pairs (e.g. Joint IP Ownership vs Ip Ownership Assignment).
