from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel
import logging
from datetime import datetime


class Message(BaseModel):
    """Represents a message between agents"""
    sender: str
    recipient: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, model_name: str = "gpt-4"):
        self.name = name
        self.model_name = model_name
        self.logger = logging.getLogger(f"agent.{name}")
        self.message_history: List[Message] = []
        
    def log_message(self, message: Message):
        """Log a message to the agent's history"""
        self.message_history.append(message)
        self.logger.info(f"Message from {message.sender} to {message.recipient}: {message.content[:100]}...")
        
    def send_message(self, recipient: str, content: str, metadata: Dict[str, Any] = None) -> Message:
        """Send a message to another agent"""
        message = Message(
            sender=self.name,
            recipient=recipient,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.log_message(message)
        return message
        
    @abstractmethod
    def process_message(self, message: Message) -> Message:
        """Process an incoming message and return a response"""
        pass
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass 