# import dependencies

from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from prompts import context
from prompts import code_parser_template
from code_reader import code_reader
from dotenv import load_dotenv
import os
import ast

load_dotenv()

# Instantiate the Ollama Mistral model

llm = Ollama(model= "mistral", request_timeout= 30.0)

# Create a document parser for processing pdf files (LlamaParse) and load the processed files into LlamaIndex (SimpleDirectoryReader)

parser = LlamaParse(api_key = os.environ.get("LLAMA_CLOUD_API_KEY"),result_type = "markdown")
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader("./data", file_extractor= file_extractor).load_data()

# Create a vector store index where to store the embeddings of the processed pdf files(VectorStoreIndex) and a query engine that is linked to the Ollama model

embed_model = resolve_embed_model("local:BAAI/bge-m3")
vector_index = VectorStoreIndex.from_documents(documents, embed_model = embed_model)
query_engine = vector_index.as_query_engine(llm=llm)


# Define tools for the agent: one for querying API documentation (from the previously created vector store) and another for analyzing code.

tools = [
  QueryEngineTool(
    query_engine = query_engine,
    metadata = ToolMetadata(
      name = "api_documentation",
      description = "This gives documentation about code for an API. Use this for reading docs for the API"
    ),
  ),
  code_reader,
]



# Initialize the ReActAgent with code-optimized LLM and tools for reasoning and tool invocation.

code_llm = Ollama(model = "codellama", request_timeout= 45.0 )
agent = ReActAgent.from_tools(tools, llm = code_llm, verbose = True, context = context)





# Define the expected structure of the LLM output (PydanticOutputParser), configure a prompt template (PrompTemplate), and set up a query pipeline for structured output generation (QueryPipeline).

class CodeOutPut(BaseModel):
  code: str
  description : str
  filename : str

parser = PydanticOutputParser(CodeOutPut)
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str)
output_pipeline = QueryPipeline(chain=[json_prompt_tmpl, llm])





# Process user prompts in a loop, query the agent with retries, display the output, and save the generated code to a file.

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    retries = 0

    while retries < 3:
        try:
            result = agent.query(prompt)
            next_result = output_pipeline.run(response=result)
            cleaned_json = ast.literal_eval(str(next_result).replace("assistant:  ", ""))
            break
        except Exception as e:
            retries += 1
            print(f"Error occured, retry #{retries}:", e)

    if retries >= 3:
        print("Unable to process request, try again...")
        continue

    print("Code generated")
    print(cleaned_json["code"])
    print("\n\nDescription:", cleaned_json["description"])

    filename = cleaned_json["filename"]

    try:
        with open(os.path.join("output", filename), "w") as f:
            f.write(cleaned_json["code"])
        print("Saved file", filename)
    except:
        print("Error saving file...")

