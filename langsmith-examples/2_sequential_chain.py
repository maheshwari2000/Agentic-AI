from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()
os.environ['LANGSMITH_PROJECT'] = 'Sequential Chain'

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatGroq(model="llama3-8b-8192", verbose=True)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

config = {
    'run_name':'sequential chain',
    'tags':['sequential','llm'],
    'metadata':{'provider':'Groq','model':'llama3-8b-8192'}
}

result = chain.invoke({'topic': 'Unemployment in India'},config=config)

print(result)
