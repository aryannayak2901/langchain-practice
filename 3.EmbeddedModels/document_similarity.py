from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "Harry Potter is a wizard and Hermione Granger is a witch and Ron Weasley is a wizard",
    "Superman is powerful DC character and Batman also DC character",
    "Mobile Phone is a device that can be used to make calls and send messages",
    "Switzerland is known for its Alps and chocolate and it is european country",
    "Langchain is a framework for building language models and it is open source"
]

query = "Tell me about Harry Potter"

doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]

index, score =sorted(list(enumerate(scores)), key=lambda x: x[1])[-1]

print(query)
print(documents[index])
print("Similarity score is: ", score)