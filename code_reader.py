from llama_index.core.tools import FunctionTool
import os

# Define the code reader tool using the FunctionTool module. This allows to wrap a function into a tool that is then passed to the LLM

def code_reader_func(file_name):
  path = os.path.join("data", file_name)
  try:
    with open(path, "r") as f:
      content = f.read()
      return {"file_content": content}
  except Exception as e:
    return {"error": str(e)}
  
code_reader = FunctionTool.from_defaults(
  fn = code_reader_func,
  name = "code_reader",
  description = """This tool can read the content of code files and return their result. Use this when you need to read the contents of a file"""
)