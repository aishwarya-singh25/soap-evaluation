import streamlit as st
from src.helper import preprocess_text, compute_rouge, compute_deepeval, chat_with_openai


def main_evaluate(patient_convo: str, soap_notes: str) -> dict:
	"""Preprocess inputs and compute ROUGE and DeepEval scores.

	Returns a dict with rouge and deepeval results.
	"""
	# basic validation
	if not patient_convo or not soap_notes:
		return {"error": "Both inputs must be non-empty strings."}

	ref = preprocess_text(patient_convo)
	cand = preprocess_text(soap_notes)

	rouge_res = compute_rouge(ref, cand)
	deepeval_res = compute_deepeval(ref, cand)

	return {
		"rouge": rouge_res,
		"deepeval": deepeval_res,
	}


def run_streamlit_app():
	st.set_page_config(page_title="SOAP Evaluation", layout="centered")
	st.title("SOAP Notes Evaluation")

	st.markdown("Enter the patient conversation and the generated SOAP note. Click Submit to compute ROUGE metrics and DeepEval.")

	patient_convo = st.text_area("Patient conversation", height=200, placeholder="Paste patient conversation here...", key="patient_convo")
	soap_notes = st.text_area("Generated SOAP note", height=200, placeholder="Paste generated SOAP note here...", key="soap_notes")

	if st.button("Submit"):
		with st.spinner("Evaluating..."):
			results = main_evaluate(patient_convo, soap_notes)

		if "error" in results:
			st.error(results["error"])
			return

		st.subheader("ROUGE")
		for k, v in results["rouge"].items():
			st.write(f"{k}: \n  precision: {v['precision']:.4f}, recall: {v['recall']:.4f}, fmeasure: {v['fmeasure']:.4f}")

		st.subheader("DeepEval (deepeval library)")
		deepeval = results.get("deepeval")
		if not deepeval:
			st.write("No DeepEval result returned.")
		elif "error" in deepeval:
			st.warning(deepeval["error"])
		else:
			# show the score and the LLM reason returned by deepeval
			st.write(f"Score: {deepeval.get('score')}")
			st.write("Reason:")
			st.text(deepeval.get("reason"))
		# persist results and show chat UI on subsequent reruns
		st.session_state.last_results = results
		st.session_state.show_chat = True
		if "chat_history" not in st.session_state:
			st.session_state.chat_history = []

	# If a chat session has been started (after a successful evaluation), render the chat UI.
	if st.session_state.get("show_chat"):
		results = st.session_state.get("last_results", {})

		# Ensure there's a system starter message summarizing the last results
		if "chat_history" not in st.session_state:
			st.session_state.chat_history = []

		if not any(m.get("role") == "system" for m in st.session_state.chat_history):
			summary_lines = []
			try:
				rouge = results.get("rouge", {})
				rouge_summary = ", ".join([f"{k}: f={v['fmeasure']:.3f}" for k, v in rouge.items()])
				summary_lines.append(f"ROUGE summary: {rouge_summary}")
			except Exception:
				pass

			try:
				deepeval = results.get("deepeval")
				if deepeval and "score" in deepeval:
					summary_lines.append(f"DeepEval score: {deepeval.get('score')}")
			except Exception:
				pass

			if summary_lines:
				system_msg = {"role": "system", "content": "The following evaluation was just produced for a generated SOAP note: " + " | ".join(summary_lines)}
			else:
				system_msg = {"role": "system", "content": "The following evaluation was just produced for a generated SOAP note."}

			st.session_state.chat_history.insert(0, system_msg)

		# render chat UI
		st.markdown("---")
		st.subheader("Chat about this evaluation")

		chat_container = st.container()

		with chat_container:
			for msg in st.session_state.chat_history:
				role = msg.get("role", "user")
				content = msg.get("content", "")
				if role == "system":
					st.info(content)
				elif role == "user":
					st.markdown(f"**You:** {content}")
				else:
					st.markdown(f"**Assistant:** {content}")

			user_input = st.text_input("Ask a question about the evaluation:", key="chat_input")
			col1, col2 = st.columns([1, 1])
			with col1:
				# give the buttons explicit keys so they persist reliably between reruns
				if st.button("Send", key="send_btn") and user_input:
					st.session_state.chat_history.append({"role": "user", "content": user_input})
					messages = st.session_state.chat_history.copy()
					with st.spinner("Getting assistant response..."):
						resp = chat_with_openai(messages)

					if "error" in resp:
						st.error(resp["error"])
					else:
						reply = resp.get("reply", "")
						st.session_state.chat_history.append({"role": "assistant", "content": reply})
						
			with col2:
				if st.button("End chat", key="end_chat_btn"):
					st.session_state.chat_history = []
        

if __name__ == "__main__":
	run_streamlit_app()

## main function to take input from streamlit, preprocess, return bertscore