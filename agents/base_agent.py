"""
Base Agent implementation for InsightAI.

This module defines the base agent interface and common functionality
for all specialized agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import uuid

class BaseAgent(ABC):
    """
    Base class for all agents.
    """
    
    def __init__(self, name: str = None):
        """
        Initialize the agent.
        
        Args:
            name: Optional agent name
        """
        self.id = str(uuid.uuid4())
        self.name = name or f"Agent-{self.id[:8]}"
        self.messages = []
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """
        Get the type of this agent.
        
        Returns:
            Agent type as string
        """
        pass
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task assigned to this agent.
        
        Args:
            task: Task description and parameters
            
        Returns:
            Task results
        """
        pass
    
    async def send_message(self, recipient_id: str, message: Dict[str, Any]) -> bool:
        """
        Send a message to another agent.
        
        Args:
            recipient_id: ID of the recipient agent
            message: Message content
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        # TODO: Implement message passing between agents
        # This is a placeholder for future agent-to-agent communication
        self.messages.append({
            "sender_id": self.id,
            "recipient_id": recipient_id,
            "content": message,
            "status": "pending"
        })
        return True
    
    async def receive_message(self, message: Dict[str, Any]) -> None:
        """
        Receive a message from another agent.
        
        Args:
            message: Message content
        """
        # TODO: Implement message handling
        self.messages.append(message)
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the agent.
        
        Returns:
            Dictionary with agent state
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.agent_type,
            "message_count": len(self.messages)
        }