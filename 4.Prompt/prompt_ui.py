from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation", pipeline_kwargs=dict(
    temperature=0.7,
    max_new_tokens=100,
))

model = ChatHuggingFace(llm=llm)

st.header("Reasearch Tool")

paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All you Need", "GPT: A Language Model API", "Deep Residual Learning for Image Recognition", "Knowledge Distillation of Neural Networks", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Recurrent Neural Network", "Transformer: A Novel Architecture for Neural Machine Translation", "Universal Language Model Capability with Deep Residual Learning"])

style_input = st.selectbox("Select Explanation Style", ["Academic", "Informal", "Technical", "Non-Technical"])

length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-4 paragraphs)", "Long (5-6 paragraphs)"])

if st.button("Summarize"):
    result = model.invoke(user_input)
    st.text(result.content)