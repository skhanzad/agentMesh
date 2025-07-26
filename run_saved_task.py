#!/usr/bin/env python3
"""
AgentMesh Saved Task Runner - Execute saved tasks from JSON files
"""

import os
import sys
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax


def load_saved_task(json_file: str):
    """Load saved task from JSON file"""
    try:
        with open(json_file, 'r') as f:
            task_data = json.load(f)
        return task_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Task file '{json_file}' not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in '{json_file}'")


def display_saved_results(task_data: dict):
    """Display saved task results"""
    console = Console()
    
    # Display banner
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    AgentMesh Saved Task                      ║
    ║              Cooperative Multi-Agent System                   ║
    ║                                                              ║
    ║  🤖 Planner Agent  →  💻 Coder Agent  →  🐛 Debugger Agent  ║
    ║                                                              ║
    ║                    ↓                                        ║
    ║                📋 Reviewer Agent                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="cyan"))
    
    # Display original task
    original_task = task_data.get("original_task", "Unknown task")
    console.print(f"\n[bold cyan]Original Task:[/bold cyan] {original_task}")
    
    # Display planner output
    if "planner_output" in task_data:
        console.print("\n[bold blue]Phase 1: Planning[/bold blue]")
        try:
            planner_data = json.loads(task_data["planner_output"])
            console.print(Panel(
                Text(json.dumps(planner_data, indent=2), style="blue"),
                title="[bold]PLANNER AGENT[/bold]",
                border_style="blue"
            ))
        except json.JSONDecodeError:
            console.print(Panel(
                Text(task_data["planner_output"], style="blue"),
                title="[bold]PLANNER AGENT[/bold]",
                border_style="blue"
            ))
    
    # Display final code
    if "final_code" in task_data:
        console.print("\n[bold green]Phase 2: Generated Code[/bold green]")
        
        # Extract code blocks from the final_code
        code_content = task_data["final_code"]
        
        # Try to find Python code blocks
        if "```python" in code_content:
            # Extract all Python code blocks
            import re
            python_blocks = re.findall(r'```python\n(.*?)\n```', code_content, re.DOTALL)
            
            for i, code_block in enumerate(python_blocks, 1):
                console.print(f"\n[green]Code Block {i}:[/green]")
                syntax = Syntax(code_block, "python", theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title=f"[bold]CODER AGENT - Block {i}[/bold]", border_style="green"))
        else:
            # Display as plain text
            console.print(Panel(
                Text(code_content, style="green"),
                title="[bold]CODER AGENT[/bold]",
                border_style="green"
            ))
    
    # Display reviewer output
    if "reviewer_output" in task_data:
        console.print("\n[bold purple]Phase 3: Final Review[/bold purple]")
        console.print(Panel(
            Text(task_data["reviewer_output"], style="purple"),
            title="[bold]REVIEWER AGENT[/bold]",
            border_style="purple"
        ))
    
    # Create summary table
    console.print("\n[bold cyan]Task Summary:[/bold cyan]")
    table = Table(title="Saved Task Results")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    table.add_row("Original Task", "✅ Loaded", original_task[:50] + "..." if len(original_task) > 50 else original_task)
    
    if "planner_output" in task_data:
        table.add_row("Planning", "✅ Completed", "Task breakdown generated")
    else:
        table.add_row("Planning", "❌ Missing", "No planner output found")
    
    if "final_code" in task_data:
        code_length = len(task_data["final_code"])
        table.add_row("Code Generation", "✅ Completed", f"{code_length} characters of code generated")
    else:
        table.add_row("Code Generation", "❌ Missing", "No code generated")
    
    if "reviewer_output" in task_data:
        table.add_row("Review", "✅ Completed", "Final assessment provided")
    else:
        table.add_row("Review", "❌ Missing", "No review output found")
    
    console.print(table)
    
    # Show execution options
    console.print("\n[bold yellow]Execution Options:[/bold yellow]")
    console.print("1. [cyan]Save code to file[/cyan] - Extract and save the generated code")
    console.print("2. [cyan]Run the code[/cyan] - Execute the generated Python code")
    console.print("3. [cyan]View full results[/cyan] - See complete task data")
    
    return task_data


def save_code_to_file(task_data: dict, filename: str = None):
    """Extract and save the generated code to a file"""
    console = Console()
    
    if "final_code" not in task_data:
        console.print("[red]No code found in the saved task![/red]")
        return
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_code_{timestamp}.py"
    
    code_content = task_data["final_code"]
    
    # Try to extract Python code blocks
    import re
    python_blocks = re.findall(r'```python\n(.*?)\n```', code_content, re.DOTALL)
    
    if python_blocks:
        # Combine all Python code blocks
        combined_code = "\n\n# Generated by AgentMesh\n# Original Task: " + task_data.get("original_task", "Unknown") + "\n\n"
        combined_code += "\n\n".join(python_blocks)
        
        try:
            with open(filename, 'w') as f:
                f.write(combined_code)
            console.print(f"[green]✅ Code saved to: {filename}[/green]")
            console.print(f"[green]📝 {len(combined_code)} characters written[/green]")
        except Exception as e:
            console.print(f"[red]Error saving code: {str(e)}[/red]")
    else:
        # Save the entire content as a text file
        try:
            with open(filename, 'w') as f:
                f.write(code_content)
            console.print(f"[green]✅ Content saved to: {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving content: {str(e)}[/red]")


def run_saved_task(json_file: str):
    """Run a saved task from JSON file"""
    console = Console()
    
    try:
        # Load saved task
        console.print(f"[blue]Loading saved task from: {json_file}[/blue]")
        task_data = load_saved_task(json_file)
        
        # Display results
        display_saved_results(task_data)
        
        # Ask user what they want to do
        console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        console.print("1. Save code to file")
        console.print("2. View full JSON data")
        console.print("3. Exit")
        
        choice = console.input("\n[cyan]Enter your choice (1-3): [/cyan]")
        
        if choice == "1":
            filename = console.input("[cyan]Enter filename (or press Enter for default): [/cyan]")
            if not filename:
                filename = None
            save_code_to_file(task_data, filename)
        
        elif choice == "2":
            console.print("\n[bold yellow]Full JSON Data:[/bold yellow]")
            console.print(Panel(
                Text(json.dumps(task_data, indent=2), style="yellow"),
                title="[bold]Complete Task Data[/bold]",
                border_style="yellow"
            ))
        
        console.print("\n[bold green]✅ Saved task execution complete![/bold green]")
        
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python run_saved_task.py <saved_task_file.json>")
        print("Example: python run_saved_task.py caclapp.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    run_saved_task(json_file)


if __name__ == "__main__":
    main() 