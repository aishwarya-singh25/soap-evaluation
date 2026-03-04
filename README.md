# SOAP Evaluation — demo

Small Streamlit demo for computing ROUGE and DeepEval on generated SOAP notes and continuing the workflow with a simple OpenAI-backed chat assistant.

## Prerequisites
- Python 3.8+
- An OpenAI API key

## Set up system
1. Create and activate a virtual environment (recommended):
2. Install Python dependencies:
3. Create a `.env` file in the project root with:

```text
OPENAI_API_KEY=sk-...
```

The app uses python-dotenv to load the `.env` file automatically.

## Run the demo

Start the Streamlit app from the project root:

```bash
streamlit run main.py
```

Open the URL printed by Streamlit (usually http://localhost:8501).

## Using the app
1. Paste a patient conversation in the "Patient conversation" field.
2. Paste a generated SOAP note in the "Generated SOAP note" field.
3. Click "Submit" to compute ROUGE and DeepEval. Results will appear on the page.
4. After a successful evaluation, a "Chat about this evaluation" section appears.
5. **[Not working yet]** Use the text input to ask follow-up questions about the evaluation. Click "Send" to query the assistant. Click "End chat" to clear the conversation.

## Demo Screenshot
<img width="915" height="816" alt="image" src="https://github.com/user-attachments/assets/b739696e-da48-4c92-b1fd-b6601c4a1895" />
