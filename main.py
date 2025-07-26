#!/usr/bin/env python3
"""
AgentMesh - Cooperative Multi-Agent Generative AI System
A CLI application for collaborative software development using LLM-powered agents.
"""

import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from coordinator import AgentCoordinator
import json


def load_environment():
    """Load environment variables"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        console = Console()
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in environment variables.")
        console.print("Please set your OpenAI API key in a .env file or environment variable.")
        console.print("Example .env file content:")
        console.print("OPENAI_API_KEY=your_openai_api_key_here")
        return False
    return True


def display_banner():
    """Display the application banner"""
    console = Console()
    
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    AgentMesh v1.0                            ║
    ║              Cooperative Multi-Agent System                   ║
    ║                                                              ║
    ║  🤖 Planner Agent  →  💻 Coder Agent  →  🐛 Debugger Agent  ║
    ║                                                              ║
    ║                    ↓                                        ║
    ║                📋 Reviewer Agent                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel(banner, style="cyan"))


def display_help():
    """Display help information"""
    console = Console()
    
    help_text = """
    [bold]AgentMesh - Cooperative Multi-Agent System[/bold]
    
    This system uses multiple AI agents to collaboratively develop software:
    
    [blue]🤖 Planner Agent:[/blue] Breaks down user tasks into subtasks
    [green]💻 Coder Agent:[/green] Writes Python code for each subtask  
    [yellow]🐛 Debugger Agent:[/yellow] Reviews and suggests fixes to code
    [purple]📋 Reviewer Agent:[/purple] Final review and validation
    
    [bold]Usage Examples:[/bold]
    • "Create a basic calculator app"
    • "Build a web scraper for news articles"
    • "Develop a simple file manager"
    • "Create a password generator"
    
    [bold]Features:[/bold]
    • Modular agent architecture
    • Rich CLI interface with colored output
    • Comprehensive logging
    • Error handling and recovery
    • Conversation history tracking
    """
    
    console.print(Panel(help_text, title="[bold]Help[/bold]", border_style="blue"))


def interactive_mode():
    """Run the application in interactive mode"""
    console = Console()
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    console.print("\n[bold green]Welcome to AgentMesh Interactive Mode![/bold green]")
    console.print("Type 'help' for usage information, 'quit' to exit.\n")
    
    while True:
        try:
            # Get user input
            task = Prompt.ask("[cyan]Enter your software development task[/cyan]")
            
            if task.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif task.lower() == 'help':
                display_help()
                continue
            elif not task.strip():
                console.print("[red]Please enter a valid task.[/red]")
                continue
            
            # Run the development pipeline
            results = coordinator.run_development_pipeline(task)
            
            # Ask if user wants to save results
            save_results = Prompt.ask(
                "\n[cyan]Would you like to save the results to a file?[/cyan]",
                choices=["y", "n"],
                default="n"
            )
            
            if save_results.lower() == 'y':
                filename = Prompt.ask(
                    "[cyan]Enter filename[/cyan]",
                    default=f"agent_mesh_results_{len(coordinator.conversation_history)}.json"
                )
                
                # Save results (excluding conversation history for brevity)
                save_data = {
                    "original_task": results["original_task"],
                    "planner_output": results["planner_output"],
                    "final_code": results["final_code"],
                    "reviewer_output": results["reviewer_output"]
                }
                
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=2, default=str)
                
                console.print(f"[green]Results saved to {filename}[/green]")
            
            # Ask if user wants to continue
            continue_choice = Prompt.ask(
                "\n[cyan]Would you like to try another task?[/cyan]",
                choices=["y", "n"],
                default="y"
            )
            
            if continue_choice.lower() != 'y':
                console.print("[yellow]Goodbye![/yellow]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


def run_single_task(task: str, output_file: str = None):
    """Run a single task and optionally save results"""
    console = Console()
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    # Run the development pipeline
    results = coordinator.run_development_pipeline(task)
    
    # Save results if requested
    if output_file:
        save_data = {
            "original_task": results["original_task"],
            "planner_output": results["planner_output"],
            "final_code": results["final_code"],
            "reviewer_output": results["reviewer_output"]
        }
        
        with open(output_file, 'w') as f:
            json.dump(save_data, f, indent=2, default=str)
        
        console.print(f"[green]Results saved to {output_file}[/green]")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AgentMesh - Cooperative Multi-Agent Generative AI System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive
  python main.py --task "Create a calculator app" --output results.json
  python main.py --help
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--task", "-t",
        type=str,
        help="Single task to execute"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file for results (JSON format)"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="gpt-4",
        help="LLM model to use (default: gpt-4)"
    )
    
    args = parser.parse_args()
    
    # Load environment
    if not load_environment():
        sys.exit(1)
    
    # Display banner
    display_banner()
    
    # Check arguments
    if args.interactive:
        interactive_mode()
    elif args.task:
        run_single_task(args.task, args.output)
    else:
        # Default to interactive mode if no arguments provided
        console = Console()
        console.print("[yellow]No arguments provided. Starting interactive mode...[/yellow]")
        interactive_mode()


if __name__ == "__main__":
    main() 