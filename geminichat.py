from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

n = 5

while(n>0):
    print("===================Chat with Gemini===================")
    prompt = input("Enter your prompt: ")
    result = model.invoke(prompt)
    print("===================Response===================")
    print(result.content)
    n-=1