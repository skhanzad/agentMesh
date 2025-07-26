from typing import Dict, Any, List
from .base_agent import BaseAgent, Message
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os


class PlannerAgent(BaseAgent):
    """Agent responsible for breaking down user tasks into subtasks"""
    
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__("Planner", model_name)
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def get_system_prompt(self) -> str:
        return """You are a Software Development Planner Agent. Your role is to:

1. Analyze user requirements and break them down into clear, actionable subtasks
2. Create a logical sequence of development steps
3. Identify dependencies between subtasks
4. Estimate complexity for each subtask
5. Provide clear acceptance criteria for each subtask

For each subtask, provide:
- A clear, specific description
- Required inputs/outputs
- Dependencies on other subtasks
- Estimated complexity (Low/Medium/High)
- Acceptance criteria

Respond in JSON format with the following structure:
{
    "subtasks": [
        {
            "id": "task_1",
            "title": "Task Title",
            "description": "Detailed description",
            "dependencies": [],
            "complexity": "Low/Medium/High",
            "acceptance_criteria": ["criteria1", "criteria2"]
        }
    ],
    "overall_approach": "Brief description of the overall approach"
}"""

    def process_message(self, message: Message) -> Message:
        """Process incoming task and break it down into subtasks"""
        self.log_message(message)
        
        # Create the prompt for the LLM
        system_prompt = self.get_system_prompt()
        user_prompt = f"Please break down the following software development task into subtasks:\n\n{message.content}"
        
        # Get response from LLM
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        # Try to parse JSON response
        try:
            plan_data = json.loads(response.content)
            response_content = json.dumps(plan_data, indent=2)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw response
            response_content = response.content
            
        return self.send_message(
            recipient=message.sender,
            content=response_content,
            metadata={"task_type": "plan", "original_task": message.content}
        ) 