from typing import Dict, List, Any
from agents import PlannerAgent, CoderAgent, DebuggerAgent, ReviewerAgent
from agents.base_agent import Message
import json
import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from datetime import datetime
import os


class AgentCoordinator:
    """Coordinates the workflow between different agents"""
    
    def __init__(self, model_name: str = "gpt-4"):
        self.console = Console()
        self.model_name = model_name
        
        # Initialize agents
        self.planner = PlannerAgent(model_name)
        self.coder = CoderAgent(model_name)
        self.debugger = DebuggerAgent(model_name)
        self.reviewer = ReviewerAgent(model_name)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent_mesh.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("coordinator")
        
        # Store conversation history
        self.conversation_history: List[Message] = []
        
    def log_conversation(self, message: Message):
        """Log a message to the conversation history"""
        self.conversation_history.append(message)
        
    def display_agent_output(self, agent_name: str, content: str, message_type: str = "info"):
        """Display agent output in a formatted way"""
        color_map = {
            "planner": "blue",
            "coder": "green", 
            "debugger": "yellow",
            "reviewer": "purple",
            "user": "cyan"
        }
        
        color = color_map.get(agent_name.lower(), "white")
        
        panel = Panel(
            Text(content, style=color),
            title=f"[bold]{agent_name.upper()}[/bold]",
            border_style=color
        )
        self.console.print(panel)
        
    def run_development_pipeline(self, user_task: str) -> Dict[str, Any]:
        """Run the complete development pipeline"""
        self.console.print(f"\n[bold cyan]Starting Development Pipeline[/bold cyan]")
        self.console.print(f"[cyan]User Task:[/cyan] {user_task}\n")
        
        results = {
            "original_task": user_task,
            "planner_output": None,
            "coder_outputs": [],
            "debugger_outputs": [],
            "reviewer_output": None,
            "final_code": None,
            "conversation_history": []
        }
        
        try:
            # Step 1: Planning Phase
            self.console.print("[bold blue]Phase 1: Planning[/bold blue]")
            user_message = Message(
                sender="User",
                recipient="Planner",
                content=user_task,
                timestamp=datetime.now()
            )
            
            planner_response = self.planner.process_message(user_message)
            self.log_conversation(planner_response)
            results["planner_output"] = planner_response.content
            self.display_agent_output("Planner", planner_response.content)
            
            # Parse planner output to get subtasks
            try:
                plan_data = json.loads(planner_response.content)
                subtasks = plan_data.get("subtasks", [])
            except json.JSONDecodeError:
                # If JSON parsing fails, create a simple subtask
                subtasks = [{"id": "task_1", "title": "Implement the requested functionality", "description": user_task}]
            
            # Step 2: Coding Phase
            self.console.print("\n[bold green]Phase 2: Coding[/bold green]")
            for i, subtask in enumerate(subtasks):
                self.console.print(f"\n[green]Working on subtask {i+1}:[/green] {subtask.get('title', 'Unknown task')}")
                
                # Send subtask to coder
                coder_message = Message(
                    sender="Planner",
                    recipient="Coder", 
                    content=f"Subtask {i+1}: {subtask.get('description', subtask.get('title', ''))}",
                    timestamp=datetime.now()
                )
                
                coder_response = self.coder.process_message(coder_message)
                self.log_conversation(coder_response)
                results["coder_outputs"].append({
                    "subtask": subtask,
                    "code": coder_response.content
                })
                self.display_agent_output("Coder", coder_response.content)
                
                # Step 3: Debugging Phase
                self.console.print(f"\n[bold yellow]Phase 3: Debugging (Subtask {i+1})[/bold yellow]")
                debugger_message = Message(
                    sender="Coder",
                    recipient="Debugger",
                    content=coder_response.content,
                    timestamp=datetime.now()
                )
                
                debugger_response = self.debugger.process_message(debugger_message)
                self.log_conversation(debugger_response)
                results["debugger_outputs"].append({
                    "subtask": subtask,
                    "feedback": debugger_response.content
                })
                self.display_agent_output("Debugger", debugger_response.content)
            
            # Step 4: Final Review Phase
            self.console.print("\n[bold purple]Phase 4: Final Review[/bold purple]")
            
            # Compile all outputs for final review
            review_content = f"""
Original Task: {user_task}

Planning Output:
{results['planner_output']}

Generated Code:
"""
            for i, coder_output in enumerate(results["coder_outputs"]):
                review_content += f"\nSubtask {i+1} Code:\n{coder_output['code']}\n"
                review_content += f"\nDebugger Feedback for Subtask {i+1}:\n{results['debugger_outputs'][i]['feedback']}\n"
            
            reviewer_message = Message(
                sender="Coordinator",
                recipient="Reviewer",
                content=review_content,
                timestamp=datetime.now()
            )
            
            reviewer_response = self.reviewer.process_message(reviewer_message)
            self.log_conversation(reviewer_response)
            results["reviewer_output"] = reviewer_response.content
            self.display_agent_output("Reviewer", reviewer_response.content)
            
            # Store final code
            results["final_code"] = "\n\n".join([output["code"] for output in results["coder_outputs"]])
            results["conversation_history"] = self.conversation_history
            
            self.console.print("\n[bold green]Development Pipeline Complete![/bold green]")
            
        except Exception as e:
            self.logger.error(f"Error in development pipeline: {str(e)}")
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
            
        return results 