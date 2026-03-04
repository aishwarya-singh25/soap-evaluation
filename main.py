import streamlit as st
from src.helper import preprocess_text, compute_rouge, compute_deepeval


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
        

if __name__ == "__main__":
	run_streamlit_app()

## main function to take input from streamlit, preprocess, return bertscore