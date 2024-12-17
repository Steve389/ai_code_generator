# Code Conductor: A Multi-LLM Code Interpreter

## 🚀 Description
Code Conductor is a locally running multi-llm agent application that combines the power of advanced language models and intelligent tool integrations to interpret user prompts, generate executable code, and document API interactions seamlessly. Leveraging tools like LlamaIndex, ReActAgent, and PydanticOutputParser, this app is optimized for structured code generation and robust query handling, making it a useful tool for developers working with APIs and dynamic code requirements.

## 🛠️ Tech Stack
The application integrates state-of-the-art technologies to ensure high efficiency and flexibility:

- **Ollama**: For powering LLMs like Mistral and CodeLlama (locally and free!!)
- **LlamaIndex**: For embedding, storing, and querying document information.
- **LlamaParse**: To parse and process structured data like PDF files.
- **ReActAgent**: An intelligent agent capable of reasoning and tool invocation.
- **PydanticOutputParser**: For transforming LLM outputs into structured objects.
- **QueryPipeline**: To chain prompt templates and LLMs for customized workflows.
- **FunctionTool**: For wrapping user-defined functions into tools accessible by the agent.

## What Happens When a Prompt is Entered?
### 1. Prompt Input
"Generate a Python function to fetch data from an API."
### 2. Agent Invocation
The ReActAgent interprets the prompt and determines whether the task involves querying the API documentation  or analyzing/generating code. In this phase, the agent has the "awareness" to choose which tool (and as a consequence which LLM) is best to answer the prompt.
### 3. Query Handling
- If the prompt relates to API documentation:
The agent uses the **QueryEngineTool** to query the Vector Store Index, which holds embeddings of pre-processed API documentation.
A relevant response is retrieved and returned to the agent for further reasoning.
- If the task involves code generation or analysis:
The agent leverages its reasoning abilities and the **code_reader** tool to produce code snippets or analyze provided files.
### 4. Output Structuring
The raw response from the agent is passed through the **QueryPipeline**.
**PydanticOutputParser** structures the response into a defined format, including:
- code: The generated or extracted code.
- description: A summary of the code's purpose or functionality.
- filename: A suggested filename for the output.
This structured output ensures clarity and consistency for downstream tasks.
### 5. Output Saving
The generated code and description are displayed in the console.
The filename is used to save the code locally in the output directory.

## ✨ My favorite tools/modules

- **FunctionTool**: This LlamaIndex module allows to wrap Python functions as tools accessible to the agent. I believe this is pretty cool! 😎
- **LlamaParse**: This is another LlamaIndex tool that takes document parsing to the next level!
- **PydanticOutputParser**: This module allows to transform LLM responses into structured pydantic objects. 
- **Ollama**: The entire application runs locally, ensuring privacy and control over sensitive data. 
