import streamlit as st
from summary import Summarizer
from evaluate import Evaluate


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_model():
    s = Summarizer()
    e = Evaluate()
    return s, e


summarizer, evaluate = load_model()
st.title("Text summarization using machine learning algorithm")
full_text = st.text_area("Enter your paragraph!")
options = ["Clustering", "LSA", "TextRank"]
choice = st.selectbox("Select algorithm", options)
if st.button("Summary now"):
    if choice == options[0]:
        summary = summarizer.summarize(full_text)
    elif choice == options[1]:
        summary = summarizer.summarize(full_text, mode="lsa")
    else:
        summary = summarizer.summarize(full_text, mode="text rank")
    score = evaluate.content_based(summary[0], full_text)
    st.write(summary[0])
    st.write("-"*20)
    list_sentence_selected = list(summary[1])
    list_sentence_selected = list(map(str, list_sentence_selected))

    st.write("Sentence selected: ${}$".format(", ".join(list_sentence_selected)))
    st.write("With {:.2f}% information keep (content-based evaluation)".format(score*100))

