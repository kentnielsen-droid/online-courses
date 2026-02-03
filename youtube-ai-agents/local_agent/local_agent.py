from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model: OllamaLLM = OllamaLLM(model="llama3.2:latest")

system_prompt: str = """
You are a financial expert with the task of analyzing, in depth and with great precision, financial reports from various companies.
You will give the user all the important insights and remove the fluff and the noise. Ask follow-up questions to the user, if your not confident that you can give a precise and accurate answer.
You will reflect on how the financial report will affect the company going forward and make a clear distinction between irrational fear and rational feer.
You will give the user your reflections of the financial report, when asked. 
Reevaluate and adjust your reflections, believes, and thoughts when presented with more information that can have relevance. BUT, be rational and always make your own evaluations.

Here are the financial documents from a company {financial_report}.

Here is the question to answer: {question}
"""
prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(system_prompt)

chain = prompt_template | model

while True:
    print("\n")
    print("-" * 50)
    question = input("Ask your question (q to quit): ")
    if question.strip() == "":
        question = "Should I invest in this company based on their earnings report?"
    print("\n\n")
    if question.strip() == "q":
        break

    financial_report = retriever.invoke(question)
    result = chain.invoke(
        {
            "financial_report": financial_report,
            "question": question,
        }
    )
    print(result)
