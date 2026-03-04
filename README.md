# SOAP Evaluation

## Context
Deepscribe's LLM should be - reliable, capture critical information, and avoid hallucination. This Evaluation Framework should identify problems such as:

- **Missing critical findings** - facts from the transcript that were omitted from the generated note.
- **Hallucinated or unsupported facts** - information in the note that isn’t grounded in the transcript.
- **Clinical accuracy issues** - medically incorrect or misleading statements

## Vision
Each time an entry is added to the database, call the main evaluation function that returns a list of scores. For hte POC, we can have a streamlit UI with 2 inputs, transcript and notes. Once the user clicks 'submit' the scores are displayed.

## Future scope
- Add an api call for the main function
- Add a dashboard that populates results in dB

