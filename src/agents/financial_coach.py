from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.core.config import get_settings

settings = get_settings()

llm = ChatOpenAI(
    openai_api_key=settings.openai_api_key,
    model="gpt-4o",
    temperature=0.3
)

async def ask_financial_question(user_id: str, question: str) -> str:
    # In a real app, retrieve user context (spending data) to inject into prompt
    template = """You are an AI Personal Financial Coach embedded in the SOL banking app.
Use the context below to answer financial questions helpfully, accurately, and securely.
Never advise on specific stocks, only general financial health rules.

Question: {question}
Answer:"""
    prompt = PromptTemplate(input_variables=["question"], template=template)
    
    chain = prompt | llm
    result = await chain.ainvoke({"question": question})
    
    return result.content
