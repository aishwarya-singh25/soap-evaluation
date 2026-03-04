# SOAP Evaluation — demo

Small Streamlit demo for computing ROUGE and DeepEval on generated SOAP notes and continuing the workflow with a simple OpenAI-backed chat assistant.

## Approach

The two goals were to - Move fast and understand production quality. I tried several deterministic aproaches including Bert score, rouge and cosine similarity, but the values were misleading and not intuitive. I decided to go ahead with an LLM as a judge and used DeepEvalu to score the summarizations. In addition to the score, a reasoning is provided by the model. 

I observed that having the additional reasoning helped me understand the reasoning and identify what information was missed. Using this knowledge, the medical professional can make a decision on whether the notes need to be updated or if they are sufficient.

The next step was to implement a chatbot into this interface so the medical professional can ask questions like "List down details that were missed" or  "Explain this score and reasoning in more detail". This feature is not working at the moment.

## Structure
- main.py: Consists of the stremlit code for UI; consists of the main block to run backend code
- src/helper.py: Consists of the backend helper functions
- src/data_analysis.py: Can be ignored. Initial data analysis done on Google Colab.

The next steps would be to add more logs to understand what errors I am running into. And also restructure the code.

# How to run the demo

### Prerequisites
- Python 3.8+
- An OpenAI API key

### Set up system
1. Create and activate a virtual environment (recommended):
2. Install Python dependencies:
3. Create a `.env` file in the project root with:

```text
OPENAI_API_KEY=sk-...
```

The app uses python-dotenv to load the `.env` file automatically.

### Run the demo

Start the Streamlit app from the project root:

```bash
streamlit run main.py
```

Open the URL printed by Streamlit (usually http://localhost:8501).

### Using the app
1. Paste a patient conversation in the "Patient conversation" field.
2. Paste a generated SOAP note in the "Generated SOAP note" field.
3. Click "Submit" to compute ROUGE and DeepEval. Results will appear on the page.
4. After a successful evaluation, a "Chat about this evaluation" section appears.
5. **[Not working yet]** Use the text input to ask follow-up questions about the evaluation. Click "Send" to query the assistant. Click "End chat" to clear the conversation.

### Demo Screenshot
<img width="915" height="816" alt="image" src="https://github.com/user-attachments/assets/b739696e-da48-4c92-b1fd-b6601c4a1895" />
