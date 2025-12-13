from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

load_dotenv()

llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation", pipeline_kwargs=dict(temperature=0.7, max_new_tokens=10))

model = ChatHuggingFace(llm = llm)

messages = [
    SystemMessage(content="You are a helpful assistant."),
]

while True:
    user_input = input("You: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input.lower() == 'exit':
        break
    response = model.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    print("AI: ", response.content)

print(chat_history)