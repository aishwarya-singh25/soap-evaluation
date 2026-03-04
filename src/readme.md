# SOAP Evaluation

## Context
Deepscribe's LLM should be - reliable, capture critical information, and avoid hallucination. This Evaluation Framework should identify problems such as:

- **Missing critical findings** - facts from the transcript that were omitted from the generated note.
- **Hallucinated or unsupported facts** - information in the note that isn’t grounded in the transcript.
- **Clinical accuracy issues** - medically incorrect or misleading statements

## Evaluation Approaches
Consider the tradeoffs between different evaluation approaches:

1. **Reference-Based vs Non Reference-Based**: Some evals require ground truth datasets which can be expensive to curate, whereas other evals can run in an unsupervised fashion which are easier to scale.
2. **LLM-as-a-judge vs Deterministic Evals** - LLM-as-a-judge evals are very powerful, but they are also slower and costlier to run compared to deterministic metrics.

## Evaluation model goals
- Building an evaluations suite that can evaluate notes and flag issues.
- A solution, focusing on context-aware interactions with an LLM.
- Check if the SOAP notes are reliable, accurate, no hallucination.

## Strech Goals
- User-friendly chat interface