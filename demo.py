#!/usr/bin/env python3
"""
AgentMesh Demo - Shows the system workflow without requiring API keys
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from agents.base_agent import Message
from datetime import datetime
import json


def demo_workflow():
    """Demonstrate the agent workflow with mock data"""
    console = Console()
    
    # Display banner
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    AgentMesh Demo                            ║
    ║              Cooperative Multi-Agent System                   ║
    ║                                                              ║
    ║  🤖 Planner Agent  →  💻 Coder Agent  →  🐛 Debugger Agent  ║
    ║                                                              ║
    ║                    ↓                                        ║
    ║                📋 Reviewer Agent                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="cyan"))
    
    # Mock user task
    user_task = "Create a basic calculator app with GUI"
    console.print(f"\n[bold cyan]User Task:[/bold cyan] {user_task}\n")
    
    # Phase 1: Planning
    console.print("[bold blue]Phase 1: Planning[/bold blue]")
    planner_output = {
        "subtasks": [
            {
                "id": "task_1",
                "title": "Create GUI Layout",
                "description": "Design the calculator interface with buttons and display",
                "dependencies": [],
                "complexity": "Medium",
                "acceptance_criteria": ["GUI displays correctly", "All buttons are visible"]
            },
            {
                "id": "task_2", 
                "title": "Implement Basic Operations",
                "description": "Add functionality for addition, subtraction, multiplication, division",
                "dependencies": ["task_1"],
                "complexity": "Medium",
                "acceptance_criteria": ["All operations work correctly", "Error handling for division by zero"]
            },
            {
                "id": "task_3",
                "title": "Add Advanced Features",
                "description": "Include square root, power, and clear functionality",
                "dependencies": ["task_2"],
                "complexity": "Low",
                "acceptance_criteria": ["Advanced operations work", "Clear button resets calculator"]
            }
        ],
        "overall_approach": "Build a tkinter-based calculator with a clean interface and comprehensive functionality"
    }
    
    console.print(Panel(
        Text(json.dumps(planner_output, indent=2), style="blue"),
        title="[bold]PLANNER AGENT[/bold]",
        border_style="blue"
    ))
    
    # Phase 2: Coding
    console.print("\n[bold green]Phase 2: Coding[/bold green]")
    
    coder_outputs = [
        {
            "subtask": "Create GUI Layout",
            "code": '''import tkinter as tk
from tkinter import ttk

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        
        # Display
        self.display = tk.Entry(root, font=('Arial', 20), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        
        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(root, text=button, font=('Arial', 16), command=cmd).grid(
                row=row, column=col, padx=2, pady=2, sticky='nsew'
            )
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)'''
        },
        {
            "subtask": "Implement Basic Operations",
            "code": '''    def click(self, key):
        if key == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, key)
    
    def clear(self):
        self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()'''
        }
    ]
    
    for i, output in enumerate(coder_outputs):
        console.print(f"\n[green]Subtask {i+1}:[/green] {output['subtask']}")
        console.print(Panel(
            Text(output['code'], style="green"),
            title="[bold]CODER AGENT[/bold]",
            border_style="green"
        ))
    
    # Phase 3: Debugging
    console.print("\n[bold yellow]Phase 3: Debugging[/bold yellow]")
    
    debugger_output = """## Code Review Results

### Issues Found:
1. **Critical**: No error handling for division by zero
2. **High**: Missing clear button functionality
3. **Medium**: No input validation for invalid expressions
4. **Low**: No keyboard support

### Suggested Fixes:
```python
def click(self, key):
    if key == '=':
        try:
            # Add input validation
            expression = self.display.get()
            if not expression:
                return
                
            result = eval(expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Cannot divide by zero")
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Invalid expression")
    elif key == 'C':
        self.clear()
    else:
        self.display.insert(tk.END, key)
```

### Overall Assessment:
- Code structure is good
- Basic functionality works
- Needs better error handling
- Missing some features from requirements"""
    
    console.print(Panel(
        Text(debugger_output, style="yellow"),
        title="[bold]DEBUGGER AGENT[/bold]",
        border_style="yellow"
    ))
    
    # Phase 4: Final Review
    console.print("\n[bold purple]Phase 4: Final Review[/bold purple]")
    
    reviewer_output = """## Final Assessment

### Completion Status: Partial (70% Complete)

### Quality Score: 7/10

### Key Strengths:
- Clean GUI implementation using tkinter
- Proper grid layout and button arrangement
- Basic arithmetic operations functional
- Good code structure and organization

### Critical Issues:
- Missing error handling for edge cases
- Incomplete feature set (no advanced operations)
- No input validation
- Missing clear functionality

### Recommendations:
1. Implement comprehensive error handling
2. Add missing features (clear, advanced operations)
3. Add input validation
4. Include keyboard support
5. Add unit tests

### Production Readiness: Not Ready
- Requires bug fixes and feature completion
- Needs testing before deployment
- Should add documentation

### Final Approval: Conditional
- Approve with fixes for critical issues
- Recommend additional development iteration"""
    
    console.print(Panel(
        Text(reviewer_output, style="purple"),
        title="[bold]REVIEWER AGENT[/bold]",
        border_style="purple"
    ))
    
    # Summary
    console.print("\n[bold green]Development Pipeline Complete![/bold green]")
    
    # Show conversation flow
    console.print("\n[bold cyan]Agent Conversation Flow:[/bold cyan]")
    
    table = Table(title="Message Exchange")
    table.add_column("From", style="cyan")
    table.add_column("To", style="cyan")
    table.add_column("Message Type", style="magenta")
    table.add_column("Content Preview", style="green")
    
    messages = [
        ("User", "Planner", "Task Request", user_task),
        ("Planner", "Coder", "Subtask 1", "Create GUI Layout..."),
        ("Coder", "Debugger", "Code Review", "Calculator GUI implementation..."),
        ("Debugger", "Reviewer", "Debug Report", "Issues found: division by zero..."),
        ("Reviewer", "User", "Final Assessment", "Completion: 70%, Quality: 7/10...")
    ]
    
    for msg in messages:
        table.add_row(msg[0], msg[1], msg[2], msg[3][:50] + "...")
    
    console.print(table)
    
    console.print("\n[bold yellow]Demo Complete![/bold yellow]")
    console.print("This demonstrates the cooperative workflow between agents.")
    console.print("To run the actual system, set your OpenAI API key and run:")
    console.print("[cyan]python main.py --interactive[/cyan]")


if __name__ == "__main__":
    demo_workflow() 