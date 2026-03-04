# SOAP Evaluation — demo

Small Streamlit demo for computing ROUGE and DeepEval on generated SOAP notes and continuing the workflow with a simple OpenAI-backed chat assistant.

## Prerequisites
- Python 3.8+
- An OpenAI API key

## Install
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configure OpenAI API key
Create a `.env` file in the project root with:

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
4. After a successful evaluation a "Chat about this evaluation" section appears. Use the text input to ask follow-up questions about the evaluation. Click "Send" to query the assistant. Click "End chat" to clear the conversation.


## Development / Troubleshooting
- If Streamlit raises "st.session_state.<key> cannot be modified after the widget with key <key> is instantiated", avoid directly setting the corresponding session key after creating a widget with the same key. The demo includes handling to prevent that, but if you change code be mindful of Streamlit widget/session rules.
- Check the terminal where Streamlit runs for exception tracebacks.

If you'd like more features (streaming responses, chat transcript download, PHI redaction toggle), open an issue or request an enhancement.
