from langchain_core.prompts.loading import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

st.header("Reasearch Tool")

paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All you Need", "GPT: A Language Model API", "Deep Residual Learning for Image Recognition", "Knowledge Distillation of Neural Networks", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Recurrent Neural Network", "Transformer: A Novel Architecture for Neural Machine Translation", "Universal Language Model Capability with Deep Residual Learning"])

style_input = st.selectbox("Select Explanation Style", ["Academic", "Informal", "Technical", "Non-Technical"])

length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-4 paragraphs)", "Long (5-6 paragraphs)"])

template = load_prompt("template.json")



if st.button("Summarize"):
    chain = template | model
    result = chain.invoke({"paper_input": paper_input, "style_input": style_input, "length_input": length_input})
    st.write(result.content)