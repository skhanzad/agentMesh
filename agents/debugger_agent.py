from typing import Dict, Any, List
from .base_agent import BaseAgent, Message
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os


class DebuggerAgent(BaseAgent):
    """Agent responsible for reviewing and debugging generated code"""
    
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__("Debugger", model_name)
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def get_system_prompt(self) -> str:
        return """You are a Software Development Debugger Agent. Your role is to:

1. Review Python code for potential bugs, errors, and issues
2. Identify security vulnerabilities and best practice violations
3. Suggest improvements for code quality, performance, and maintainability
4. Check for proper error handling and edge cases
5. Verify code follows Python conventions and standards
6. Provide specific, actionable feedback with code examples

When reviewing code, check for:
- Syntax errors and logical bugs
- Missing imports or dependencies
- Improper error handling
- Security issues (e.g., SQL injection, input validation)
- Performance problems
- Code style and PEP 8 compliance
- Missing documentation or unclear code
- Edge cases not handled

Respond with a structured analysis including:
1. Issues found (with severity: Critical/High/Medium/Low)
2. Suggested fixes with code examples
3. Overall code quality assessment
4. Recommendations for improvement"""

    def process_message(self, message: Message) -> Message:
        """Process code and provide debugging feedback"""
        self.log_message(message)
        
        # Create the prompt for the LLM
        system_prompt = self.get_system_prompt()
        user_prompt = f"""Please review and debug the following Python code:

{message.content}

Provide a comprehensive analysis of any issues found and suggest improvements."""

        # Get response from LLM
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        return self.send_message(
            recipient=message.sender,
            content=response.content,
            metadata={"task_type": "debug", "code_review": True}
        ) 