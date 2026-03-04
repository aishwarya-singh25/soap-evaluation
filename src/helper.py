import os
from dotenv import load_dotenv
import openai
from typing import List, Tuple, Dict

import re
import nltk
from nltk.corpus import stopwords

from bert_score import score
from rouge_score import rouge_scorer

from deepeval import evaluate
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase

try:
    _ = stopwords.words("english")
except Exception:
    nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

# load env early so OpenAI key is available if present
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def preprocess_text(text: str) -> str:
    """Lowercase, remove extra whitespace, punctuation, and stopwords.

    Returns a cleaned string.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    # remove punctuation (keep alphanumerics and spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # collapse whitespace
    tokens = [t for t in text.split() if t and t not in STOPWORDS]
    return " ".join(tokens)


def compute_bertscore(cands: List[str], refs: List[str], lang: str = "en") -> Tuple[float, float, float]:
    """Compute BERTScore between lists of candidate and reference texts.

    Returns (precision, recall, f1) averaged across examples.
    """

    P, R, F1 = score(cands, refs, lang=lang, rescale_with_baseline=True)
    # P, R, F1 are tensors; return averages as floats
    p = float(P.mean().item())
    r = float(R.mean().item())
    f = float(F1.mean().item())
    return p, r, f


def compute_rouge(ref: str, cand: str) -> Dict[str, Dict[str, float]]:
    """Compute ROUGE-1, ROUGE-2 and ROUGE-L between reference and candidate.

    Returns a dict mapping metric -> {precision, recall, fmeasure}.
    """

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(ref, cand)

    out = {}
    for k, v in scores.items():
        out[k] = {"precision": v.precision, "recall": v.recall, "fmeasure": v.fmeasure}

    return out


def compute_deepeval(ref: str, cand: str) -> Dict[str, object]:
    """Evaluate candidate against reference using the deepeval library.

    Returns a dict with key "deepeval" mapping to a serializable result or
    an inner dict with "error" on failure.
    """
    try:
        metric = SummarizationMetric(threshold=0.7, model="gpt-4o")
        test_case = LLMTestCase(input=ref, actual_output=cand)

        metric.measure(test_case)
        # return both the numeric score and the LLM-provided reason/explanation
        return {"score": metric.score, "reason": metric.reason}

    except Exception as e:
        return {"error": f"deepeval.evaluate failed: {type(e).__name__}: {e}"}


def chat_with_openai(messages: list, model: str = "gpt-4o") -> Dict[str, object]:
    """Send a chat-style request to OpenAI and return the assistant reply.

    messages should be a list of dicts like [{"role": "system|user|assistant", "content": "..."}, ...]

    Returns a dict: {"reply": str} or {"error": str} on failure.
    """
    if not OPENAI_API_KEY:
        return {"error": "OpenAI API key not found. Set OPENAI_API_KEY in the environment."}

    try:
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=600,
            temperature=0.2,
        )

        # get assistant message
        assistant_msg = resp.choices[0].message.content
        return {"reply": assistant_msg}

    except Exception as e:
        return {"error": f"OpenAI API call failed: {type(e).__name__}: {e}"}



