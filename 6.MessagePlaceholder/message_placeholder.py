from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

# chat template

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs=dict(temperature=0.7, max_new_tokens=50)
)

model = ChatHuggingFace(llm=llm)

chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful assistant'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{query}'),
])

# load chat history

chat_history = []
with open('chat_history.txt') as f:
   chat_history.extend(f.readlines())

print(chat_history)

# create prompt

user_input = input("You: ")

prompt = chat_template.invoke({
    "chat_history": chat_history,
    "query": user_input
})

print(prompt)

result = model.invoke(prompt)

print(result.content)
