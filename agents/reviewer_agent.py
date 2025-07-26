from typing import Dict, Any, List
from .base_agent import BaseAgent, Message
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os


class ReviewerAgent(BaseAgent):
    """Agent responsible for final review and validation of completed code"""
    
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__("Reviewer", model_name)
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def get_system_prompt(self) -> str:
        return """You are a Software Development Reviewer Agent. Your role is to:

1. Conduct final review of completed software development tasks
2. Verify that all requirements have been met
3. Assess overall code quality and completeness
4. Check for integration issues between components
5. Validate that the solution is production-ready
6. Provide final recommendations and approval status

When reviewing completed work, evaluate:
- Functional completeness (does it solve the original problem?)
- Code quality and maintainability
- Performance and efficiency
- Security and reliability
- Documentation and usability
- Integration with other components
- Test coverage and edge case handling

Provide a final assessment with:
1. Overall completion status (Complete/Partial/Incomplete)
2. Quality score (1-10 scale)
3. Key strengths of the implementation
4. Critical issues that need addressing
5. Recommendations for production deployment
6. Final approval status"""

    def process_message(self, message: Message) -> Message:
        """Process completed work and provide final review"""
        self.log_message(message)
        
        # Create the prompt for the LLM
        system_prompt = self.get_system_prompt()
        user_prompt = f"""Please conduct a final review of the completed software development work:

{message.content}

Provide a comprehensive final assessment including completion status, quality score, and approval status."""

        # Get response from LLM
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        return self.send_message(
            recipient=message.sender,
            content=response.content,
            metadata={"task_type": "review", "final_assessment": True}
        ) 