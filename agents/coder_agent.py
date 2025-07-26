from typing import Dict, Any, List
from .base_agent import BaseAgent, Message
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os


class CoderAgent(BaseAgent):
    """Agent responsible for writing Python code based on subtasks"""
    
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__("Coder", model_name)
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def get_system_prompt(self) -> str:
        return """You are a Software Development Coder Agent. Your role is to:

1. Write clean, well-documented Python code based on provided subtasks
2. Follow Python best practices and PEP 8 style guidelines
3. Include proper error handling and input validation
4. Write comprehensive docstrings and comments
5. Ensure code is modular and reusable
6. Include necessary imports and dependencies

When writing code:
- Always include a main function or entry point
- Add proper type hints where appropriate
- Include example usage in docstrings
- Handle edge cases and errors gracefully
- Make the code production-ready

Respond with the complete Python code file, including all necessary imports and a main section for testing."""

    def process_message(self, message: Message) -> Message:
        """Process subtask and generate Python code"""
        self.log_message(message)
        
        # Create the prompt for the LLM
        system_prompt = self.get_system_prompt()
        user_prompt = f"""Please write Python code for the following subtask:

{message.content}

Provide complete, runnable Python code that implements this functionality."""

        # Get response from LLM
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        return self.send_message(
            recipient=message.sender,
            content=response.content,
            metadata={"task_type": "code", "subtask": message.content}
        ) 