# Generator integration notes

The original `classify_clause()` orchestrator in `generator.py` remains the
single entry point. The improvements in this repo are designed to be
drop-in:

1. **Preprocessing** – call `preprocess_clause()` from
   `text_preprocessor.py` on the raw clause *before* embedding and before
   building the prompt:

   ```python
   from .text_preprocessor import preprocess_clause

   clause_text = preprocess_clause(raw_clause_text)
   ```

2. **Prompt** – replace the import of `build_prompt` with the improved
   version in this directory. Signature is unchanged.

3. **Config** – `TOP_K` default is now 10 and `OLLAMA_MODEL` defaults to
   `qwen2.5:7b`. Existing environment variables still override both.

4. **Candidate constraint** – the improved prompt already restricts the
   model to the labels present in the retrieved Top-K (or
   `NO_APPLICABLE_LABEL`). Combined with the existing
   `parse_prediction_result` validation this eliminates most invented
   labels observed with the 1.5B model.

5. **Abstention** – keep the existing `MIN_RETRIEVAL_CONFIDENCE` gate so
   low-evidence retrievals do not force a category.

No breaking API changes are required. After pulling these files into the
original tree, re-run the fixed-10 diagnostic (or the new eval harness)
with `OLLAMA_MODEL=qwen2.5:7b` to measure the lift.
