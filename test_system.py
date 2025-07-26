#!/usr/bin/env python3
"""
Test script for AgentMesh system
Tests basic functionality without requiring API calls
"""

import sys
import os
from unittest.mock import Mock, patch
from agents.base_agent import Message
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.debugger_agent import DebuggerAgent
from agents.reviewer_agent import ReviewerAgent
from coordinator import AgentCoordinator
from datetime import datetime


def test_base_agent():
    """Test the base agent functionality"""
    print("Testing BaseAgent...")
    
    # Create a mock agent that inherits from BaseAgent
    with patch('agents.planner_agent.ChatOpenAI') as mock_openai:
        mock_openai.return_value.invoke.return_value.content = '{"subtasks": [{"id": "test", "title": "Test Task"}]}'
        
        class MockAgent(PlannerAgent):
            def __init__(self):
                super().__init__()
                # Mock the LLM to avoid API calls
                self.llm = Mock()
                self.llm.invoke.return_value.content = '{"subtasks": [{"id": "test", "title": "Test Task"}]}'
        
        agent = MockAgent()
        
        # Test message creation
        message = agent.send_message("TestRecipient", "Test content")
        assert message.sender == "Planner"
        assert message.recipient == "TestRecipient"
        assert message.content == "Test content"
        assert len(agent.message_history) == 1
        
        print("✅ BaseAgent tests passed")


def test_agent_coordinator():
    """Test the coordinator functionality"""
    print("Testing AgentCoordinator...")
    
    # Mock all the agents to avoid API calls
    with patch('agents.planner_agent.ChatOpenAI'), \
         patch('agents.coder_agent.ChatOpenAI'), \
         patch('agents.debugger_agent.ChatOpenAI'), \
         patch('agents.reviewer_agent.ChatOpenAI'):
        
        coordinator = AgentCoordinator()
        
        # Test coordinator initialization
        assert coordinator.planner is not None
        assert coordinator.coder is not None
        assert coordinator.debugger is not None
        assert coordinator.reviewer is not None
        
        print("✅ AgentCoordinator tests passed")


def test_message_system():
    """Test the message passing system"""
    print("Testing Message system...")
    
    # Create a test message
    message = Message(
        sender="TestSender",
        recipient="TestRecipient",
        content="Test message content",
        timestamp=datetime.now()
    )
    
    # Test message properties
    assert message.sender == "TestSender"
    assert message.recipient == "TestRecipient"
    assert message.content == "Test message content"
    assert message.metadata == {}
    
    print("✅ Message system tests passed")


def test_agent_prompts():
    """Test that all agents have system prompts"""
    print("Testing agent system prompts...")
    
    # Test each agent has a system prompt
    with patch('agents.planner_agent.ChatOpenAI'), \
         patch('agents.coder_agent.ChatOpenAI'), \
         patch('agents.debugger_agent.ChatOpenAI'), \
         patch('agents.reviewer_agent.ChatOpenAI'):
        
        agents = [
            PlannerAgent(),
            CoderAgent(),
            DebuggerAgent(),
            ReviewerAgent()
        ]
        
        for agent in agents:
            prompt = agent.get_system_prompt()
            assert isinstance(prompt, str)
            assert len(prompt) > 0
            print(f"✅ {agent.name} system prompt: {len(prompt)} characters")
        
        print("✅ All agent system prompts are valid")


def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        "requirements.txt",
        "main.py",
        "coordinator.py",
        "agents/__init__.py",
        "agents/base_agent.py",
        "agents/planner_agent.py",
        "agents/coder_agent.py",
        "agents/debugger_agent.py",
        "agents/reviewer_agent.py",
        "README.md"
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing file: {file_path}"
        print(f"✅ {file_path} exists")
    
    print("✅ All required files present")


def main():
    """Run all tests"""
    print("🧪 Running AgentMesh System Tests\n")
    
    try:
        test_file_structure()
        test_message_system()
        test_base_agent()
        test_agent_prompts()
        test_agent_coordinator()
        
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\nTo run the system:")
        print("1. Set your OpenAI API key in a .env file")
        print("2. Run: python main.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 